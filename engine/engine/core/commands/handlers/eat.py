from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import constants, types
from engine.core.commands.handlers import helpers


def handle_command(
    session: Session, game: types.Game, item_name: str
) -> types.Response:
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
            item=helpers.sentence_from_list_of_names([items]),
            health_points=items.item.health_points,
        ),
    )


action = types.Action(
    name="eat",
    aliases=["eat", "drink"],
    handler=handle_command,
    description="Consume an item (individual or meal) from your inventory.",
)
