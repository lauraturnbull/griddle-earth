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
                name="Southern Plains",
                description="You are on a grassy plain. The land stretches out around you in all directions. To the east you can see some sparse trees.",
                region=types.Region.home_plains,
                components=[
                    types.NewComponent(
                        name="small plant",
                        description="It is a short bushy plant with green leaves and white flowers.",
                        items=[
                            types.NewItems(item=items.strawberry, quantity=3)
                        ],
                    ),
                    types.NewComponent(
                        name="murky window",
                        description="A misty window hangs in the air, apparently with no support. You feel like you can almost see through it, but what you see doesn't look like the landscape behind.",
                        is_gateway=True,
                        transports_to=types.Coordinates(
                            x_coordinate=1, y_coordinate=0
                        ),
                    ),
                ],
            ),
            types.NewLocation(
                coordinates=types.Coordinates(
                    x_coordinate=1,
                    y_coordinate=0,
                ),
                name="Farmer Tam's Place",
                description="You're at Farmer Tam's place, the largest "
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
