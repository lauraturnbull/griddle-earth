from fastapi import HTTPException
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import types

from . import helpers


def handle_command(
    session: Session, game: types.Game, command: types.Command
) -> types.EatResponse:
    item_name = " ".join(command.context)
    name_variants = helpers.get_noun_variants(item_name)
    items = next(
        (i for i in game.inventory.items if i.item.name in name_variants), None
    )

    if items is None:
        raise HTTPException(
            status_code=422,
            detail=f"Could not find any {item_name} in your inventory",
        )

    # update hp and remove item from inventory
    game.health_points += items.item.health_points
    items.quantity -= 1
    if items.quantity == 0:
        game.inventory.items.remove(items)

    persister.update_game(session, game.id, game)

    return types.EatResponse(
        health_points=game.health_points,
        consumed_item=types.ItemsOut(
            quantity=1,
            name=items.item.name,
            health_points=items.item.health_points,
        ),
    )
