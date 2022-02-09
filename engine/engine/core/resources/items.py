from engine.core.types import Item, ItemType, ItemCollectionMethod

# fruit
apple = Item(
    name="apple",
    item_type=ItemType.fruit,
    health_points=30,
    collection_method=ItemCollectionMethod.forage
)

# vegetables
potato = Item(
    name="potato",
    item_type=ItemType.vegetable,
    health_points=50,
    collection_method=ItemCollectionMethod.forage
)
carrot = Item(
    name="carrot",
    item_type=ItemType.vegetable,
    health_points=50,
    collection_method=ItemCollectionMethod.forage
)

spotted_mushroom = Item(
    name="spotted mushroom",
    item_type=ItemType.vegetable,
    health_points=-30,
    collection_method=ItemCollectionMethod.forage
)

# proteins
egg = Item(
    name="egg",
    item_type=ItemType.protein,
    health_points=40,
    collection_method=ItemCollectionMethod.forage
)

# grains

# herbs

chives = Item(
    name="chives",
    item_type=ItemType.herb,
    health_points=5,
    collection_method=ItemCollectionMethod.forage
)

