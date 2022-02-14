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
    new_map = core.make_new_map()
    patched_map.return_value = new_map

    game = core.make_game(id=1)
    resp = client.post("v1/game")
    assert resp.json() == jsonable_encoder(game)

    resp = client.get(f"v1/game/{game.id}/adventure-log")
    # todo properly patch this
    assert resp.json() == {
        "items_discovered": [
            {"discoverable": 1, "discovered": 0, "item_type": "fruit"},
            {"discoverable": 0, "discovered": 0, "item_type": "vegetable"},
            {"discoverable": 0, "discovered": 0, "item_type": "protein"},
            {"discoverable": 0, "discovered": 0, "item_type": "grain"},
            {"discoverable": 0, "discovered": 0, "item_type": "herb"},
            {"discoverable": 0, "discovered": 0, "item_type": "meal"},
        ],
        "locations_discovered": [
            {"discoverable": 0, "discovered": 0, "region": "wetlands"},
            {"discoverable": 0, "discovered": 0, "region": "mountains"},
            {"discoverable": 1, "discovered": 0, "region": "forest"},
            {"discoverable": 0, "discovered": 0, "region": "desert"},
            {"discoverable": 0, "discovered": 0, "region": "Home Plains"},
        ],
    }


@freeze_time(frozen_time)
@patch("engine.core.resources.base.map.make_base_map")
def test_start_game(patched_map: Any, client: TestClient) -> None:
    new_map = core.make_new_map()
    patched_map.return_value = new_map

    game = core.make_game(id=1)
    resp = client.post("v1/game")
    assert resp.json() == jsonable_encoder(game)

    resp = client.post(
        f"v1/game/{game.id}/command", params=dict(input="start")
    )
    assert resp.json() == jsonable_encoder(core.make_location_out())
