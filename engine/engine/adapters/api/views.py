from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import responses, types
from engine.core.commands import command_parser
from engine.core.resources.base import adventure_log, map

from . import dependencies

v1 = APIRouter()


def get_now() -> datetime:
    return datetime.now(timezone.utc)


@v1.get("/")
def root():
    return {"message": "Hello World"}


@v1.post("/game")
def create_new_game(
    session: Session = Depends(dependencies.session),
) -> types.Game:
    base_game = types.NewGame(
        health_points=1000,
        inventory=types.NewInventory(),
        created=get_now(),
    )
    base_map = map.make_base_map()
    base_adventure_log = adventure_log.make_base_adventure_log(map=base_map)
    new_game = persister.create_new_game(
        session, game=base_game, map=base_map, adventure_log=base_adventure_log
    )
    return new_game


# todo - handle missing resources


@v1.get("/game/{game_id}")
def get_game(
    game_id: int, session: Session = Depends(dependencies.session)
) -> Optional[types.Game]:
    """
    Returns the current state of the player including:
    - location
    - direction
    - description of the current scene
    - list of items available to access in scene
    """
    game = persister.get_game_by_id(session, game_id=game_id)
    return game


@v1.get("/game/{game_id}/map")
def get_game_map(
    game_id: int, session: Session = Depends(dependencies.session)
) -> Optional[types.Map]:
    map = persister.get_map_by_game_id(session, game_id=game_id)
    return map


@v1.get("/game/{game_id}/adventure-log")
def get_game_adventure_log(
    game_id: int, session: Session = Depends(dependencies.session)
) -> Optional[types.AdventureLogOut]:
    adventure_log = persister.get_adventure_log_by_game_id(
        session, game_id=game_id
    )
    if adventure_log is None:
        raise HTTPException(
            status_code=422,
            detail=f"no adventure log found for game {game_id}",
        )
    return responses.make_adventure_log_response(adventure_log=adventure_log)


@v1.post("/game/{game_id}/command")
def handle_command(
    game_id: int, input: str, session: Session = Depends(dependencies.session)
) -> Any:
    """
    Handles interaction with a scene
    validates

    """
    parser = command_parser.CommandParser(session, input)
    current_state = persister.get_game_by_id(session, game_id)
    if current_state is None:
        raise HTTPException(
            status_code=422, detail=f"game {game_id} not found"
        )
    new_state = parser.handle_command(current_state)
    return new_state
