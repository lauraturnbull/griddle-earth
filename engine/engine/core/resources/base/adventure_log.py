from engine.core import types


def make_base_adventure_log(map: types.Map) -> types.AdventureLog:
    discoverable_locations = map.locations
    discoverable_items = list()
    for loc in discoverable_locations:
        for c in loc.components:
            for i in c.items:
                if i.item not in discoverable_items:
                    discoverable_items.append(i.item)

    return types.AdventureLog(
        discoverable_locations=discoverable_locations,
        discoverable_items=discoverable_items,
    )
