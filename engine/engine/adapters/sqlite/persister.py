from sqlalchemy.orm import Session
from engine.core import types
from datetime import datetime, timezone

from . import model


def get_now() -> datetime:
    return datetime.now(timezone.utc)


# app to db

def state_app_to_db(state: types.GameState) -> model.GameState:
    return model.GameState(
        **state.dict()
    )


def game_app_to_db(game: types.Game) -> model.Game:
    return model.Game(
        game_states=[state_app_to_db(s) for s in game.game_states]
    )


# db to app

def state_db_to_app(state: model.GameState) -> types.GameState:
    return types.GameState(
        health_points=state.health_points,
        scene=state.scene,
        x_coordinate=state.x_coordinate,
        y_coordinate=state.y_coordinate,
        created=state.created
    )


def game_db_to_app(game: model.Game) -> types.Game:
    return types.Game(
        id=game.id,
        game_states=[state_db_to_app(s) for s in game.game_states]
    )


def create_game(session: Session) -> types.Game:
    new_game = model.Game(
        game_states=[
            model.GameState(
                health_points=1000,
                scene="Hungry Beginnings",
                x_coordinate=0,
                y_coordinate=0,
                created=get_now()
            )
        ]
    )

    session.add(new_game)
    session.commit()

    return game_db_to_app(new_game)


def get_most_recent_game_state(session, game_id: int) -> types.GameState:
    qry = (
        session.query(model.GameState)
        .filter(model.GameState.game_id==game_id)
        .order_by(model.GameState.id.desc())
        .limit(1)
    )

    game_state_db = qry.one_or_none()
    #todo if game_state_db is None, raise...

    return state_db_to_app(game_state_db)


def append_game_state(
    session, game_id: int, game_state: types.GameState
) -> types.GameState:
    game_db = (
        session.query(model.Game)
        .filter(model.Game.id == game_id)
        .one_or_none()
    )
    # todo - raise or smth
    game_state_db = state_app_to_db(game_state)
    game_db.game_states.append(game_state_db)
    session.commit()

    return state_db_to_app(game_state_db)