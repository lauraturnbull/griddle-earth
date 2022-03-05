from fastapi import HTTPException
from sqlalchemy.orm import Session

from engine.core import constants, types

from .helpers import (
    get_component,
    get_location_description,
    sentence_from_list_of_names,
)


def handle_command(
    session: Session, game: types.Game, command: types.Command
) -> types.Response:
    if game.location is None:
        raise HTTPException(
            status_code=422,
            detail=("No location - game not started"),
        )
    if len(command.context) == 0 or "around" in command.context:
        return types.Response(message=get_location_description(game.location))

    # looking at a specific component
    component_name = " ".join(command.context).lower()
    component = get_component(game.location.components, component_name)
    if component is None:
        return types.Response(
            message=constants.MISSING_COMPONENT.format(
                component=component_name
            )
        )

    # items we can forage or were dropped
    collectable_items = [
        i.item.name
        for i in component.items
        if i.item.collection_method
        in (types.ItemCollectionMethod.forage, types.ItemCollectionMethod.cook)
    ]

    msg = component.description
    if collectable_items:
        items_str = sentence_from_list_of_names(collectable_items)
        msg = constants.COMPONENT_DESCRIPTION.format(
            component=component.description, items=items_str
        )

    return types.Response(message=msg)
