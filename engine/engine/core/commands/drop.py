from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import constants, types
from engine.core.resources.base import components

from . import helpers


def handle_command(
    session: Session, game: types.Game, context: List[str]
) -> types.Response:
    # find item in inventory
    item_name = " ".join(context)
    name_variants = helpers.get_noun_variants(item_name)

    items = next(
        (
            i
            for i in game.inventory.items
            if i.item.name.lower() in name_variants
        ),
        None,
    )
    if items is None:
        return types.Response(
            message=constants.MISSING_INVENTORY_ITEM.format(item=item_name)
        )

    assert game.location is not None

    # check to see if we have abandoned items in this location before
    map_location = persister.get_map_location_by_coordinates(
        session, game.id, game.location.coordinates
    )
    if map_location is None:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Could not find location at "
                f"x={game.location.coordinates.x_coordinate}, "
                f"y={game.location.coordinates.y_coordinate}"
            ),
        )
    discard_pile = next(
        (
            c
            for c in map_location.components
            if c.name == constants.DISCARD_PILE
        ),
        None,
    )
    if discard_pile is not None:
        # check if we have abandoned this kind of item before
        discarded_items = next(
            (i for i in discard_pile.items if i.item.name in name_variants),
            None,
        )
        if discarded_items is not None:
            discarded_items.quantity += 1

        else:
            discard_pile.items.append(
                types.NewItems(  # type: ignore
                    quantity=1, item=types.NewItem(**items.item.dict())
                )
            )
    else:
        new_discard_pile = components.make_discard_pile(
            items=types.NewItems(
                quantity=1, item=types.NewItem(**items.item.dict())
            )
        )
        map_location.components.append(new_discard_pile)  # type: ignore

    # remove the item from the inventory
    items.quantity -= 1
    if items.quantity == 0:
        game.inventory.items.remove(items)

    game.location = map_location
    persister.update_game(session, game.id, game)

    persister.update_map_location(session, game.id, map_location)

    return types.Response(
        message=constants.DROPPED_ITEM.format(item=items.item.name)
    )
