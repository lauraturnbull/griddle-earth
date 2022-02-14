from datetime import datetime

from freezegun import freeze_time
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import types
from engine.core.commands import cook
from tests.factories import core, helpers

frozen_time = datetime(2022, 2, 2)


@freeze_time(frozen_time)
def test_cook_specific_recipe(session: Session) -> None:
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
            quantity=2,
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

    resp = cook.handle_command(
        session,
        game,
        command=core.make_command(action="cook", context="apples, wheat"),
    )
    assert resp == types.ItemsOut(
        quantity=1, name="Apple Pie", health_points=200
    )
    game = persister.get_game_by_id(session, game.id)
    assert game is not None
    assert len(game.inventory.items) == 2
    assert game.inventory.items == [
        core.make_items(
            id=3, item=core.make_item(id=4, health_points=30), quantity=1
        ),
        core.make_items(
            id=5,
            item=core.make_item(
                id=6,
                name="Apple Pie",
                item_type=types.ItemType.meal,
                health_points=200,
                collection_method=types.ItemCollectionMethod.cook,
            ),
            quantity=1,
        ),
    ]

    adventure_log = persister.get_adventure_log_by_game_id(session, game.id)
    assert adventure_log is not None
    assert len(adventure_log.discovered_items) == 1
