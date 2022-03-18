from fastapi import HTTPException
from sqlalchemy.orm import Session

from engine.core import constants, types
from engine.core.commands.handlers.helpers import (
    get_component,
    get_location_description,
    get_verb,
    sentence_from_list_of_names,
)


def handle_command(
    session: Session, game: types.Game, context: str
) -> types.Response:
    if game.location is None:
        raise HTTPException(
            status_code=422,
            detail=("No location - game not started"),
        )
    if len(context) == 0 or "around" in context:
        return types.Response(message=get_location_description(game.location))

    # looking at a specific component
    component = get_component(game.location.components, context)
    if component is None:
        return types.Response(
            message=constants.MISSING_COMPONENT.format(component=context)
        )

    # items we can forage or were dropped
    collectable_items = [
        i
        for i in component.items
        if i.item.collection_method
        in (types.ItemCollectionMethod.forage, types.ItemCollectionMethod.cook)
    ]

    msg = component.description
    if collectable_items:
        verb = get_verb(collectable_items)
        items_str = sentence_from_list_of_names(collectable_items)
        msg = constants.COMPONENT_DESCRIPTION.format(
            component=component.description, verb=verb, items=items_str
        )

    return types.Response(message=msg)


action = types.Action(
    name="look",
    aliases=["look"],
    handler=handle_command,
    description="Describes the location and it's contents. You can also look at things within a location.",
    examples=["look around", "look at the tiny tree"],
)
