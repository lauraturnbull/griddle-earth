from engine.core import types
from engine.core.resources import items


def make_recipe_book() -> types.RecipeBook:
    return types.RecipeBook(
        recipes=[
            # generics
            types.Recipe(
                name="Vegetable Stew",
                description="A stew made from any vegetables",
                required_types=[types.ItemType.vegetable],
                boost=2,
            ),
            types.Recipe(
                name="Meat and Veg Stew",
                description="A stew made from any meats and vegetables",
                required_types=[
                    types.ItemType.vegetable,
                    types.ItemType.protein,
                ],
                boost=2,
            ),
            types.Recipe(
                name="Meat Skewer",
                description="A skewer of any meats",
                required_types=[types.ItemType.protein],
                boost=2,
            ),
            types.Recipe(
                name="Poached Fruits",
                description="Any fruits poached until tender",
                required_types=[types.ItemType.fruit],
                boost=2,
            ),
            # specifics
            types.Recipe(
                name="Salted Pork",
                description="It's particularly good",
                required_items=[items.pork],
                boost=4,
            ),
            types.Recipe(
                name="Apple Pie",
                description="A hot pie made with apples",
                required_items=[items.wheat, items.apple],
                boost=4,
            ),
        ]
    )
