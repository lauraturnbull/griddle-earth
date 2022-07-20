from datetime import datetime

from freezegun import freeze_time
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import types
from engine.core.commands.handlers import take
from tests.factories import core, helpers

frozen_time = datetime(2022, 2, 2)


@freeze_time(frozen_time)
def test_take_item(session: Session) -> None:
    # make game and map and add to db
    new_game = helpers.make_game_in_map_location(
        session=session,
        new_map=core.make_new_map(
            locations=[
                core.make_new_location(
                    coordinates=types.Coordinates(
                        x_coordinate=0, y_coordinate=0
                    ),
                    components=[
                        core.make_new_component(
                            name="trees",
                            items=[
                                core.make_new_items(
                                    item=core.make_new_item(), quantity=5
                                )
                            ],
                        )
                    ],
                ),
            ]
        ),
    )

    # take the item
    resp = take.handle_command(
        session=session,
        game=new_game,
        # note - "the"/"a" is stripped before this function call
        context=["apples", "from", "trees"],
    )
    assert resp == types.Response(message="You have taken 1x apples.")

    # check inventory has been updated
    game = persister.get_game_by_id(session, game_id=new_game.id)
    assert game is not None
    assert len(game.inventory.items) == 1
    assert game.inventory.items[0].quantity == 1
    assert game.inventory.items[0].item.name == "apple"

    # check item removed from game location state
    assert game.location is not None
    assert game.location.components[0].items[0].quantity == 4

    # check item removed from map
    map = persister.get_map_by_game_id(session, game.id)
    assert map is not None
    assert map.locations[0].components[0].items[0].quantity == 4

    # check adventure log has been updated
    adventure_log = persister.get_adventure_log_by_game_id(session, game.id)
    assert adventure_log is not None
    assert len(adventure_log.discovered_items) == 1
    assert adventure_log.discovered_items[0].name == "apple"

    # take again

    take.handle_command(
        session=session, game=game, context=["apples", "from", "trees"]
    )
    # check inventory has been updated
    assert len(game.inventory.items) == 1
    assert game.inventory.items[0].quantity == 2
    assert game.inventory.items[0].item.name == "apple"

    # check item removed from game location state
    assert game.location.components[0].items[0].quantity == 3

    # check item removed from map
    map = persister.get_map_by_game_id(session, game.id)
    assert map is not None
    assert map.locations[0].components[0].items[0].quantity == 3

    # check adventure log has *not* been updated
    adventure_log = persister.get_adventure_log_by_game_id(session, game.id)
    assert adventure_log is not None
    assert len(adventure_log.discovered_items) == 1
    assert adventure_log.discovered_items[0].name == "apple"


@freeze_time(frozen_time)
def test_take_item_full_inventory(session: Session) -> None:
    # make game and map and add to db
    new_game = helpers.make_game_in_map_location(
        session=session,
    )
    # add some items to the inventory
    new_game.inventory.items = [
        core.make_new_items(
            item=core.make_new_item(  # type: ignore
                name="apple", health_points=30
            ),
            quantity=9,
        ),
        core.make_new_items(
            item=core.make_new_item(  # type: ignore
                name="wheat", health_points=20, item_type=types.ItemType.grain
            ),
            quantity=1,
        ),
    ]
    persister.update_game(session, new_game.id, new_game)
    game = persister.get_game_by_id(session, new_game.id)
    assert game is not None
    assert len(game.inventory.items) == 2

    resp = take.handle_command(
        session, game, context=["apples", "from", "trees"]
    )
    assert resp == types.Response(
        message="Cannot exceed maximum inventory size of 10. Cook, consume, or drop items to reduce the size of your inventory."
    )
