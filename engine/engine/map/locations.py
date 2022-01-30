from engine.core import types
from .import items

Map = types.Map(
    locations=[
        types.Location(
            x_coordinate=0,
            y_coordinate=0,
            name="No Place Like Home",
            description="You're at home, the best kitchen in all Griddle Earth. Where better to prepare meals from ingredients around the world.",
            region=types.Region.home_plains,
            items=[],
        ),
        types.Location(
            x_coordinate=1,
            y_coordinate=0,
            name="Farmer Tam's Place",
            description="You're at Farmer Tam's place, the largest orchards in the Home Plains.",
            region=types.Region.home_plains,
            items=[
                types.Items(
                    item=items.apple,
                    count=3,
                )
            ],
        ),
    ]
)