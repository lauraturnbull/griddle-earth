from fastapi import HTTPException
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import types

from .helpers import get_location_description


def handle_command(
    session: Session, game: types.Game, context: str
) -> types.Response:
    """
    Begin the game in location (0,0).
    In future the location could be selected
    """
    location = persister.get_map_location_by_coordinates(
        session,
        game_id=game.id,
        coordinates=types.Coordinates(x_coordinate=0, y_coordinate=0),
    )
    if location is None:
        raise HTTPException(
            status_code=422,
            detail=f"Could not find location (0,0) for game {game.id}",
        )
    game.location = location
    persister.update_game(session, game_id=game.id, new_game_state=game)
    return types.Response(
        health_points=game.health_points,
        location=types.LocationOut(**location.dict()),
        message=get_location_description(location),
    )
