from datetime import datetime

from freezegun import freeze_time
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import types
from engine.core.commands import take
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
        command=core.make_command(action="take", context="apples from trees"),
    )
    assert resp.quantity == 1
    assert resp.item.name == "apple"

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
        session=session,
        game=game,
        command=core.make_command(action="take", context="apples from trees"),
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
