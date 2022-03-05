from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import constants, types

from . import helpers


def handle_command(
    session: Session, game: types.Game, command: types.Command
) -> types.Response:
    item_name = " ".join(command.context)
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
            message=constants.MISSING_INVENTORY_ITEM.format(item_name)
        )

    # todo - cannot exceed max hp

    # update hp and remove item from inventory
    game.health_points += items.item.health_points
    items.quantity -= 1
    if items.quantity == 0:
        game.inventory.items.remove(items)

    persister.update_game(session, game.id, game)

    return types.Response(
        health_points=game.health_points,
        message=constants.ATE_ITEM.format(
            item=items.item.name, health_points=items.item.health_points
        ),
    )
