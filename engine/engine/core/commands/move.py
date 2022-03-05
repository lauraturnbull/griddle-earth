from fastapi import HTTPException
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import constants, types

from .helpers import get_location_description


def handle_command(
    session: Session, game: types.Game, command: types.Command
) -> types.Response:
    if game.location is None:
        raise HTTPException(
            status_code=422,
            detail="No location - game not started",
        )
    if not command.context:
        return types.Response(message=constants.MISSING_DIRECTION)
    coordinates = game.location.coordinates
    directions = [types.Ordinal(d) for d in command.context]
    for direction in directions:
        if direction is types.Ordinal.north:
            coordinates.y_coordinate += 1
        if direction is types.Ordinal.east:
            coordinates.x_coordinate += 1
        if direction is types.Ordinal.south:
            coordinates.y_coordinate -= 1
        if direction is types.Ordinal.west:
            coordinates.x_coordinate -= 1

    new_location = persister.get_map_location_by_coordinates(
        session, game_id=game.id, coordinates=coordinates
    )
    if new_location is None:
        return types.Response(message=constants.FORBIDDEN_DIRECTION)

    # update the game state
    game.location = new_location
    game.health_points -= constants.MOVE_LOCATION_HP

    persister.update_game(session, game_id=game.id, new_game_state=game)

    persister.update_adventure_log_discovered_locations(
        session, game_id=game.id, location=game.location
    )

    return types.Response(
        health_points=game.health_points,
        location=types.LocationOut(**game.location.dict()),
        message=get_location_description(game.location),
    )
