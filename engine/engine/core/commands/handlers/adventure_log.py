from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import types


def handle_command(
    session: Session, game: types.Game, context: str
) -> types.AdventureLogResponse:
    adventure_log = persister.get_adventure_log_by_game_id(session, game.id)
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
    adventure_log_out = types.AdventureLogResponse(
        locations_discovered=discovered_locations_by_region,
        items_discovered=discovered_items_by_type,
    )
    return adventure_log_out


action = types.Action(
    name="adventure log",
    handler=handle_command,
    aliases=["adventure log", "log", "journal"],
    description="A breakdown of the items and locations you've discovered",
)
