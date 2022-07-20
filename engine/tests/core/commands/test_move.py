from datetime import datetime

import pytest
from fastapi import HTTPException
from freezegun import freeze_time
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import types
from engine.core.commands.handlers import move
from tests.factories import core, helpers

frozen_time = datetime(2022, 2, 2)


@freeze_time(frozen_time)
def test_move(session: Session) -> None:
    # make game and map and add to db
    new_game = helpers.make_game_in_map_location(
        session=session,
        new_map=core.make_new_map(
            locations=[
                core.make_new_location(
                    coordinates=types.Coordinates(
                        x_coordinate=0, y_coordinate=0
                    )
                ),
                core.make_new_location(
                    coordinates=types.Coordinates(
                        x_coordinate=0, y_coordinate=1
                    )
                ),
                core.make_new_location(
                    coordinates=types.Coordinates(
                        x_coordinate=1, y_coordinate=1
                    )
                ),
            ]
        ),
    )

    # move
    resp = move.handle_command(
        session=session,
        game=new_game,
        context=["north", "east"],
    )
    assert resp == types.Response(
        health_points=700,
        location=core.make_location_out(),
        message="A descriptive description Looking around you see trees.",
    )
    game = persister.get_game_by_id(session, new_game.id)
    assert game is not None
    assert game.location is not None
    assert game.location.coordinates == types.Coordinates(
        x_coordinate=1, y_coordinate=1
    )

    # check adventure log has been updated
    adventure_log = persister.get_adventure_log_by_game_id(
        session, new_game.id
    )
    assert adventure_log is not None
    assert len(adventure_log.discovered_locations) == 1
    assert adventure_log.discovered_locations[
        0
    ].coordinates == types.Coordinates(x_coordinate=1, y_coordinate=1)

    # check hp has dropped
    assert game.health_points == 700


@freeze_time(frozen_time)
@pytest.mark.parametrize("direction", ["n", "north"])
def test_handles_variants(session: Session, direction: str) -> None:
    """
    note - command context is .lower()ed before this function
    so we only have to handle the lower case variants
    """

    # make game and map and add to db
    new_game = helpers.make_game_in_map_location(
        session=session,
        new_map=core.make_new_map(
            locations=[
                core.make_new_location(
                    coordinates=types.Coordinates(
                        x_coordinate=0, y_coordinate=0
                    )
                ),
                core.make_new_location(
                    coordinates=types.Coordinates(
                        x_coordinate=0, y_coordinate=1
                    )
                ),
            ]
        ),
    )

    # move
    resp = move.handle_command(
        session=session,
        game=new_game,
        context=[direction],
    )
    assert resp == types.Response(
        health_points=700,
        location=core.make_location_out(),
        message="A descriptive description Looking around you see trees.",
    )
    game = persister.get_game_by_id(session, new_game.id)
    assert game is not None
    assert game.location is not None
    assert game.location.coordinates == types.Coordinates(
        x_coordinate=0, y_coordinate=1
    )


@freeze_time(frozen_time)
def unknown_direction(session: Session) -> None:
    # make game and map and add to db
    game = helpers.make_game_in_map_location(session)
    # in future will be a different exception/response
    # todo fix me
    with pytest.raises(HTTPException):
        move.handle_command(
            session=session,
            game=game,
            context=["morth"],
        )


@freeze_time(frozen_time)
def test_move_no_location(session: Session) -> None:
    # make game and map and add to db
    game = helpers.make_game_in_map_location(session)
    resp = move.handle_command(
        session=session,
        game=game,
        context=["north"],
    )
    assert resp == types.Response(message="You cannot go that way.")
