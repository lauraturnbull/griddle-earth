from datetime import datetime

from freezegun import freeze_time
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import types
from engine.core.commands import eat
from tests.factories import core, helpers

frozen_time = datetime(2022, 2, 2)


@freeze_time(frozen_time)
def test_eat_item(session: Session) -> None:
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
    assert game.health_points == 1000

    resp = eat.handle_command(
        session,
        game,
        context=["apples"],
    )
    assert resp == types.Response(
        health_points=1030, message="You ate apple (+30hp)."
    )

    game = persister.get_game_by_id(session, game.id)
    assert game is not None
    assert len(game.inventory.items) == 2
    assert game.inventory.items == [
        core.make_items(
            id=4,
            item=core.make_item(
                id=5,
                health_points=20,
                name="wheat",
                item_type=types.ItemType.grain,
            ),
            quantity=1,
        ),
        core.make_items(
            id=3, item=core.make_item(id=4, health_points=30), quantity=1
        ),
    ]


@freeze_time(frozen_time)
def test_eat_last_item(session: Session) -> None:
    # make game and map and add to db
    new_game = helpers.make_game_in_map_location(
        session=session,
    )
    # add some items to the inventory
    new_game.inventory.items = [
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
    assert len(game.inventory.items) == 1
    assert game.health_points == 1000

    resp = eat.handle_command(
        session,
        game,
        context=["wheat"],
    )
    assert resp == types.Response(
        health_points=1020, message="You ate wheat (+20hp)."
    )

    game = persister.get_game_by_id(session, game.id)
    assert game is not None
    assert game.inventory.items == []
