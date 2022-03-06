from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import constants, types

from .helpers import get_component, get_location_description


def handle_command(
    session: Session, game: types.Game, context: List[str]
) -> types.Response:
    if game.location is None:
        raise HTTPException(
            status_code=422,
            detail="No location - game not started",
        )

    if not context:
        return types.Response(message="Where do you want enter?")

    component_name = " ".join(context)
    component = get_component(game.location.components, component_name)
    if component is None:
        return types.Response(
            message=constants.MISSING_COMPONENT.format(
                component=component_name
            )
        )
    print(component.is_gateway)
    print(component.transports_to)
    if (not component.is_gateway) or (component.transports_to is None):
        return types.Response(
            message=constants.NOT_A_GATEWAY.format(component=component.name)
        )

    new_location = persister.get_map_location_by_coordinates(
        session, game_id=game.id, coordinates=component.transports_to
    )

    if new_location is None:
        raise Exception("Gateway location should exist.")

    # update the game state
    old_location = game.location
    game.location = new_location
    persister.update_game(session, game_id=game.id, new_game_state=game)

    persister.update_adventure_log_discovered_locations(
        session, game_id=game.id, location=game.location
    )

    return types.Response(
        health_points=game.health_points,
        location=types.LocationOut(**game.location.dict()),
        message=constants.GATEWAY_DESCRIPTION.format(
            component=component_name, location=old_location.name
        )
        + " "
        + get_location_description(game.location),
    )
