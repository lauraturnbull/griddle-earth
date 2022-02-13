from datetime import datetime
from typing import Any
from unittest.mock import patch

from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from freezegun import freeze_time

from tests.factories import core

frozen_time = datetime(2022, 2, 2)


@freeze_time(frozen_time)
def test_create_new_game(client: TestClient) -> None:
    resp = client.post("v1/game")
    assert resp.json() == jsonable_encoder(core.make_game())
    # maybe want to check map, inventory have been made


@freeze_time(frozen_time)
def test_get_game_by_id(client: TestClient) -> None:
    game_1 = core.make_game(id=1)
    game_2 = core.make_game(id=2, inventory=core.make_inventory(id=2))

    resp = client.post("v1/game")
    assert resp.json() == jsonable_encoder(game_1)

    resp = client.post("v1/game")
    assert resp.json() == jsonable_encoder(game_2)

    resp = client.get(f"v1/game/{game_2.id}")
    assert resp.json() == jsonable_encoder(game_2)


@freeze_time(frozen_time)
@patch("engine.core.resources.base.map.make_base_map")
def test_get_map_by_game_id(patched_map: Any, client: TestClient) -> None:
    new_map = core.make_new_map()
    patched_map.return_value = new_map

    game = core.make_game(id=1)
    resp = client.post("v1/game")
    assert resp.json() == jsonable_encoder(game)

    resp = client.get(f"v1/game/{game.id}/map")
    assert resp.json() == jsonable_encoder(core.make_map())


@freeze_time(frozen_time)
@patch("engine.core.resources.base.map.make_base_map")
def test_get_adventure_log_by_game_id(
    patched_map: Any, client: TestClient
) -> None:
    # todo - this should have a different response type in future
    new_map = core.make_new_map()
    patched_map.return_value = new_map

    game = core.make_game(id=1)
    resp = client.post("v1/game")
    assert resp.json() == jsonable_encoder(game)

    resp = client.get(f"v1/game/{game.id}/adventure-log")
    # ids aren't one due to map/game being inserted first.
    adventure_log = core.make_adventure_log(
        discoverable_items=[core.make_item(id=3)],
        discoverable_locations=[
            core.make_location(
                id=2,
                components=[
                    core.make_component(
                        id=2,
                        items=[
                            core.make_items(id=2, item=core.make_item(id=2))
                        ],
                    )
                ],
            )
        ],
    )
    assert resp.json() == jsonable_encoder(adventure_log)
