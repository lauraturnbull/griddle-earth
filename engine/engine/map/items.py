from engine.core.types import Item, ItemType

# fruit
apple = Item(
    name="apple",
    item_type=ItemType.fruit,
    health_points=30,
)

# vegetables
potato = Item(
    name="potato",
    item_type=ItemType.vegetable,
    health_points=50,
)
carrot = Item(
    name="carrot",
    item_type=ItemType.vegetable,
    health_points=50,
)

spotted_mushroom = Item(
    name="spotted mushroom",
    item_type=ItemType.vegetable,
    health_points=-30,
)

# meat

# fish

# grains

# herbs

chives = Item(
    name="chives",
    item_type=ItemType.herb,
    health_points=5,
)

