from engine.core import types


def make_recipe_book() -> types.RecipeBook:
    return types.RecipeBook(
        recipes=[
            # generics
            types.Recipe(
                name="Vegetable Stew",
                description="A stew made from any vegetables.",
                required_types=[types.ItemType.vegetable],
                boost=2,
            ),
            types.Recipe(
                name="Meat and Veg Stew",
                description="A stew made from any meats and vegetables.",
                required_types=[
                    types.ItemType.vegetable,
                    types.ItemType.protein,
                ],
                boost=2,
            ),
            types.Recipe(
                name="Meat Skewer",
                description="A skewer of any meats.",
                required_types=[types.ItemType.protein],
                boost=2,
            ),
            types.Recipe(
                name="Poached Fruits",
                description="Any fruits poached until tender.",
                required_types=[types.ItemType.fruit],
                boost=2,
            ),
            types.Recipe(
                name="Elixir",
                description="A herby concoction.",
                required_types=[types.ItemType.herb],
                boost=3,
            ),
        ]
    )
