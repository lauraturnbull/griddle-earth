from engine.core import types


def make_adventure_log_response(
    adventure_log: types.AdventureLog,
) -> types.AdventureLogOut:
    discovered_locations_by_region = [
        types.DiscoveredLocationsByRegion(
            region=r,
            discovered=len(
                [
                    i
                    for i in adventure_log.discovered_locations
                    if i.region == r
                ]
            ),
            discoverable=len(
                [
                    i
                    for i in adventure_log.discoverable_locations
                    if i.region == r
                ]
            ),
        )
        for r in types.Region
    ]
    discovered_items_by_type = [
        types.DiscoveredItemsByType(
            item_type=t,
            discovered=len(
                [i for i in adventure_log.discovered_items if i.item_type == t]
            ),
            discoverable=len(
                [
                    i
                    for i in adventure_log.discoverable_items
                    if i.item_type == t
                ]
            ),
        )
        for t in types.ItemType
    ]
    adventure_log_out = types.AdventureLogOut(
        locations_discovered=discovered_locations_by_region,
        items_discovered=discovered_items_by_type,
    )
    return adventure_log_out
