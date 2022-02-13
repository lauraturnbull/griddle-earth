from typing import Optional

from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import types

from . import core


def make_game_in_map_location(
    session: Session,
    new_game: Optional[types.NewGame] = None,
    new_map: Optional[types.NewMap] = None,
    coordinates: types.Coordinates = types.Coordinates(
        x_coordinate=0, y_coordinate=0
    ),
) -> types.Game:
    if not new_game:
        new_game = core.make_new_game()
    if not new_map:
        new_map = core.make_new_map()
    game = persister.create_new_game(
        session,
        game=new_game,
        map=new_map,
        adventure_log=core.make_new_adventure_log(),
    )

    loc = persister.get_map_location_by_coordinates(
        session,
        game.id,
        coordinates=coordinates,
    )
    assert loc is not None
    game.location = loc
    persister.update_game(session, game_id=game.id, new_game_state=game)
    return game
