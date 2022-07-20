from datetime import datetime

import pytest
from freezegun import freeze_time
from sqlalchemy.orm import Session

from engine.core import types
from engine.core.commands.handlers import trap
from tests.factories import core, helpers

frozen_time = datetime(2022, 2, 2)


@freeze_time(frozen_time)
@pytest.mark.parametrize(
    "command,item,response",
    (
        (
            [],
            core.make_new_item(
                name="rabbit",
                collection_method=types.ItemCollectionMethod.hunt,
            ),
            "Where do you want to set the trap?",
        ),
        (
            ["in", "rabbit", "warren"],
            core.make_new_item(
                name="rabbit",
                collection_method=types.ItemCollectionMethod.hunt,
            ),
            "You must provide bait from your inventory to set a trap.",
        ),
        (
            ["in", "rabbit", "warren", "with", "apples"],
            core.make_new_item(
                name="rabbit",
                collection_method=types.ItemCollectionMethod.forage,
            ),
            "It doesn't seem like there's anything worthwhile to hunt in the rabbit warren.",
        ),
        (
            ["in", "rabbit", "warren", "with", "apples"],
            core.make_new_item(
                name="rabbit",
                collection_method=types.ItemCollectionMethod.hunt,
            ),
            "You don't have any apples in your inventory.",
        ),
    ),
)
def test_hunt_item(
    session: Session,
    command,
    item,
    response,
) -> None:
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
                            name="rabbit warren",
                            items=[core.make_new_items(item=item, quantity=1)],
                        )
                    ],
                ),
            ]
        ),
    )

    resp = trap.handle_command(
        session=session,
        game=new_game,
        # note - "the"/"a" is stripped before this function call
        context=command,
    )
    assert type(resp) == types.Response
    assert resp.message == response
