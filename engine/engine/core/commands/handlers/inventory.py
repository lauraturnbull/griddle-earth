from collections import defaultdict

from sqlalchemy.orm import Session

from engine.core import types


def handle_command(
    session: Session, game: types.Game, context: str
) -> types.InventoryResponse:
    grouped_inventory = defaultdict(list)
    for i in game.inventory.items:
        grouped_inventory[i.item.item_type].append(
            types.ItemsOut(
                quantity=i.quantity,
                name=i.item.name,
                health_points=i.item.health_points,
            )
        )
    inventory = [
        types.GroupedInventory(item_type=k, items=v)
        for k, v in grouped_inventory.items()
    ]
    return types.InventoryResponse(inventory=inventory)


action = types.Action(
    name="inventory",
    handler=handle_command,
    aliases=["inventory", "backpack"],
    description="Lists the items in your inventory.",
)
