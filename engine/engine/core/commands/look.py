from typing import Union

from fastapi import HTTPException
from sqlalchemy.orm import Session

from engine.core import types

from .helpers import get_component


def handle_command(
    session: Session, game: types.Game, command: types.Command
) -> Union[types.LookAroundResponse, types.LookAtResponse]:
    if game.location is None:
        raise HTTPException(
            status_code=422,
            detail=("No location - game not started"),
        )
    if "around" in command.context:
        return types.LookAroundResponse(
            names=[c.name for c in game.location.components]
        )

    component_name = " ".join(command.context).lower()
    component = get_component(game.location.components, component_name)
    return types.LookAtResponse(
        description=component.description,
        # List forageable items and cooked items that were dropped.
        # Components with hunted items will only have the component description
        visible_items=[
            types.ItemsOut(
                quantity=i.quantity,
                name=i.item.name,
                health_points=i.item.health_points,
            )
            for i in component.items
            if i.item.collection_method
            in (
                types.ItemCollectionMethod.forage,
                types.ItemCollectionMethod.cook,
            )
        ],
    )
