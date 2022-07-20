from datetime import datetime

from freezegun import freeze_time
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core.commands.handlers import drop
from tests.factories import core, helpers

frozen_time = datetime(2022, 2, 2)


@freeze_time(frozen_time)
def test_drop_item(session: Session) -> None:
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
    ]
    persister.update_game(session, new_game.id, new_game)
    game = persister.get_game_by_id(session, new_game.id)
    assert game is not None
    assert len(game.inventory.items) == 1

    # when
    drop.handle_command(session, game, context=["apples"])

    # then
    game = persister.get_game_by_id(session, game.id)
    assert game is not None
    assert len(game.inventory.items) == 1
    assert game.inventory.items[0].quantity == 1
    assert game.inventory.items[0].item.name == "apple"

    assert len(game.location.components) == 2
    assert game.location.components[1].name == "discarded items"
    assert game.location.components[1].items[0].item.name == "apple"
    assert game.location.components[1].items[0].quantity == 1

    map_location = persister.get_map_location_by_coordinates(
        session, game.id, game.location.coordinates
    )
    assert map_location == game.location
