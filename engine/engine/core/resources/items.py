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

# proteins
egg = Item(
    name="egg",
    item_type=ItemType.protein,
    health_points=40,
)

# grains

# herbs

chives = Item(
    name="chives",
    item_type=ItemType.herb,
    health_points=5,
)

