"""
The map details are stored in a csv as that was the easiest way to edit the content in bulk to begin with.
A cool task for the future would be to build a nice interface/drag and drop type thing.
"""

import csv
from enum import IntEnum
from pathlib import Path
from typing import Any, List, Optional

from engine.core import types


class CSVColumn(IntEnum):
    x_coordinate = 0
    y_coordinate = 1
    location_name = 2
    description = 3
    region = 4
    component_name = 5
    component_description = 6
    is_gateway = 7
    transports_to_x = 8
    transports_to_y = 9
    quantity = 10
    item_name = 11
    item_type = 12
    health_points = 13
    collection_method = 14


file_path = str(Path(__file__).parent.absolute()) + "/griddle_earth_map.csv"


def item_from_row(row: List[Any]) -> Optional[types.NewItems]:
    return (
        types.NewItems(
            quantity=row[CSVColumn.quantity.value],
            item=types.NewItem(
                name=row[CSVColumn.item_name.value],
                item_type=types.ItemType(row[CSVColumn.item_type.value]),
                health_points=row[CSVColumn.health_points.value],
                collection_method=types.ItemCollectionMethod(
                    row[CSVColumn.collection_method.value]
                ),
            ),
        )
        if row[CSVColumn.quantity.value]
        else None
    )


def component_from_row(row: List[Any]) -> Optional[types.NewComponent]:
    return (
        types.NewComponent(
            name=row[CSVColumn.component_name.value],
            description=row[CSVColumn.component_description.value],
            is_gateway=row[CSVColumn.is_gateway.value],
            transports_to=types.Coordinates(
                x_coordinate=int(row[CSVColumn.transports_to_x.value]),
                y_coordinate=int(row[CSVColumn.transports_to_y.value]),
            )
            if (
                row[CSVColumn.transports_to_x.value]
                and row[CSVColumn.transports_to_y.value]
            )
            else None,
            items=list(filter(None, [item_from_row(row)])),
        )
        if row[CSVColumn.component_name.value]
        else None
    )


def base_map() -> types.NewMap:
    new_map = types.NewMap()
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        # skip header
        next(reader)
        for row in reader:
            if all(v == "" for v in row[: CSVColumn.quantity.value]):
                # it's another item for the previous component
                item = item_from_row(row)
                if item:
                    new_map.locations[-1].components[-1].items.append(item)
            if all(v == "" for v in row[: CSVColumn.component_name.value]):
                # it's another component for the previous location
                component = component_from_row(row)
                if component:
                    new_map.locations[-1].components.append(component)
            else:
                # it's a full location row
                location = types.NewLocation(
                    coordinates=types.Coordinates(
                        x_coordinate=int(row[CSVColumn.x_coordinate.value]),
                        y_coordinate=int(row[CSVColumn.y_coordinate.value]),
                    ),
                    name=row[CSVColumn.location_name.value],
                    description=row[CSVColumn.description.value],
                    region=types.Region(row[CSVColumn.region.value]),
                    components=list(filter(None, [component_from_row(row)])),
                )
                new_map.locations.append(location)
    return new_map
