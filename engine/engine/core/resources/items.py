from engine.core.types import ItemCollectionMethod, ItemType, NewItem

# fruit
apple = NewItem(
    name="apple",
    item_type=ItemType.fruit,
    health_points=30,
    collection_method=ItemCollectionMethod.forage,
)

# vegetables
potato = NewItem(
    name="potato",
    item_type=ItemType.vegetable,
    health_points=50,
    collection_method=ItemCollectionMethod.forage,
)
carrot = NewItem(
    name="carrot",
    item_type=ItemType.vegetable,
    health_points=50,
    collection_method=ItemCollectionMethod.forage,
)

spotted_mushroom = NewItem(
    name="spotted mushroom",
    item_type=ItemType.vegetable,
    health_points=-30,
    collection_method=ItemCollectionMethod.forage,
)

# proteins
egg = NewItem(
    name="egg",
    item_type=ItemType.protein,
    health_points=40,
    collection_method=ItemCollectionMethod.forage,
)
rabbit = NewItem(
    name="rabbit",
    item_type=ItemType.protein,
    health_points=150,
    collection_method=ItemCollectionMethod.hunt,
)
pork = NewItem(
    name="pork",
    item_type=ItemType.protein,
    health_points=150,
    collection_method=ItemCollectionMethod.hunt,
)

# grains
wheat = NewItem(
    name="wheat",
    item_type=ItemType.grain,
    health_points=50,
    collection_method=ItemCollectionMethod.forage,
)

# herbs

chives = NewItem(
    name="chives",
    item_type=ItemType.herb,
    health_points=5,
    collection_method=ItemCollectionMethod.forage,
)
