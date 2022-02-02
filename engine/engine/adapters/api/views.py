from engine.core import types
from engine.core.commands import command_parser
from engine.core.commands import move
from sqlalchemy.orm import Session
from engine.adapters.sqlite import persister
from . import dependencies

from fastapi import FastAPI, Depends, APIRouter

v1 = APIRouter()


@v1.get("/")
def root():
    return {"message": "Hello World"}


@v1.post("/game")
def create_new_game(
    session: Session = Depends(dependencies.session)
) -> types.Game:
    # todo - need to make map too
    new_game = persister.create_game(session)
    return new_game


@v1.get("/game/{game_id}")
def get_game(
    game_id: int,
    session: Session = Depends(dependencies.session)
) -> types.Game:
    """
    Returns the current state of the player including:
    - location
    - direction
    - description of the current scene
    - list of items available to access in scene
    """
    game = persister.get_game_by_id(
        session, game_id=game_id
    )
    return game


@v1.post("/{game_id}/command")
def handle_command(
    game_id: int,
    input: str,
    session: Session = Depends(dependencies.session)
) -> types.Game:
    """
    Handles interaction with a scene
    validates

    """
    parser = command_parser.CommandParser(session, input)
    current_state = persister.get_game_by_id(session, game_id)
    new_state = parser.handle_command(current_state)
    return new_state

