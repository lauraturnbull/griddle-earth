from engine.core.types import ItemCollectionMethod, ItemType, NewItem

# forage
apple = NewItem(
    name="apples",
    item_type=ItemType.fruit,
    health_points=30,
    collection_method=ItemCollectionMethod.forage,
)
bamboo = NewItem(
    name="bamboo",
    item_type=ItemType.vegetable,
    health_points=50,
    collection_method=ItemCollectionMethod.forage,
)
carrot = NewItem(
    name="carrots",
    item_type=ItemType.vegetable,
    health_points=50,
    collection_method=ItemCollectionMethod.forage,
)
chives = NewItem(
    name="chives",
    item_type=ItemType.herb,
    health_points=5,
    collection_method=ItemCollectionMethod.forage,
)
garlic = NewItem(
    name="garlic",
    item_type=ItemType.vegetable,
    health_points=50,
    collection_method=ItemCollectionMethod.forage,
)
pear = NewItem(
    name="pears",
    item_type=ItemType.vegetable,
    health_points=50,
    collection_method=ItemCollectionMethod.forage,
)
potato = NewItem(
    name="potatoes",
    item_type=ItemType.vegetable,
    health_points=50,
    collection_method=ItemCollectionMethod.forage,
)
pumpkin = NewItem(
    name="pumpkins",
    item_type=ItemType.vegetable,
    health_points=50,
    collection_method=ItemCollectionMethod.forage,
)
rhubarb = NewItem(
    name="rhubarb",
    item_type=ItemType.fruit,
    health_points=40,
    collection_method=ItemCollectionMethod.forage,
)
spotted_mushroom = NewItem(
    name="spotted mushrooms",
    item_type=ItemType.vegetable,
    health_points=-30,
    collection_method=ItemCollectionMethod.forage,
)
strawberry = NewItem(
    name="strawberries",
    item_type=ItemType.fruit,
    health_points=20,
    collection_method=ItemCollectionMethod.forage,
)


# hunt
egg = NewItem(
    name="eggs",
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
