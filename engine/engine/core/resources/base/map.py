from engine.core import types
from engine.core.resources import items


def make_base_map() -> types.NewMap:
    return types.NewMap(
        locations=[
            types.NewLocation(
                coordinates=types.Coordinates(
                    x_coordinate=0,
                    y_coordinate=0,
                ),
                name="No Place Like Home",
                description="You're at home, the best kitchen in all Griddle "
                "Earth. Where better to prepare meals from "
                "ingredients around the world.",
                region=types.Region.home_plains,
                components=[],
            ),
            types.NewLocation(
                coordinates=types.Coordinates(
                    x_coordinate=1,
                    y_coordinate=0,
                ),
                name="Farmer Tam's Place",
                description="You're at Farmer Tam's place, the largest"
                "orchards in the Home Plains.",
                region=types.Region.home_plains,
                components=[
                    types.NewComponent(
                        name="Trees",
                        description="The trees are bursting with apples. There"
                        " are also a few birds nests.",
                        items=[
                            types.NewItems(
                                item=items.apple,
                                quantity=3,
                            ),
                            types.NewItems(item=items.egg, quantity=1),
                        ],
                    )
                ],
            ),
        ]
    )
