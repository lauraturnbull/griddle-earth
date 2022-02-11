from fastapi.testclient import TestClient
from tests.factories import core
from freezegun import freeze_time
from datetime import datetime
from unittest.mock import patch
from fastapi.encoders import jsonable_encoder

frozen_time=datetime(2022, 2, 2)


@freeze_time(frozen_time)
def test_create_new_game(client: TestClient):
    resp = client.post("v1/game")
    assert resp.json() == jsonable_encoder(core.make_game())
    # maybe want to check map, inventory have been made


@freeze_time(frozen_time)
def test_get_game_by_id(client: TestClient):
    game_1 = core.make_game(id=1)
    game_2 = core.make_game(id=2)

    resp = client.post("v1/game")
    assert resp.json() == jsonable_encoder(game_1)

    resp = client.post("v1/game")
    assert resp.json() == jsonable_encoder(game_2)

    resp = client.get(f"v1/game/{game_2.id}")
    assert resp.json() == jsonable_encoder(game_2)


@freeze_time(frozen_time)
@patch('engine.core.resources.base.map.make_base_map')
def test_get_map_by_game_id(patched_map, client: TestClient):
    map = core.make_map()
    patched_map.return_value = map

    game = core.make_game(id=1)
    resp = client.post("v1/game")
    assert resp.json() == jsonable_encoder(game)

    resp = client.get(f"v1/game/{game.id}/map")
    assert resp.json() == jsonable_encoder(map)


@freeze_time(frozen_time)
@patch('engine.core.resources.base.map.make_base_map')
def test_get_map_by_game_id(patched_map, client: TestClient):
    # todo - this should have a different response type in future
    map = core.make_map()
    patched_map.return_value = map

    adventure_log = core.make_adventure_log()
    game = core.make_game(id=1)
    resp = client.post("v1/game")
    assert resp.json() == jsonable_encoder(game)

    resp = client.get(f"v1/game/{game.id}/adventure-log")
    assert resp.json() == jsonable_encoder(adventure_log)
