from sqlalchemy.orm import Session
from engine.core import types
from . import model


def state_app_to_db(state: types.GameState) -> model.GameState:
    return model.GameState(
        health_points=state.health_points,
        scene=state.scene,
        x_coordinate=state.coordinates.x,
        y_coordinate=state.coordinates.y
    )


def state_db_to_app(state: model.GameState) -> types.GameState:
    return types.GameState(
        health_points=state.health_points,
        scene=state.scene,
        coordinates=types.Coordinates(
            x=state.x_coordinate,
            y=state.y_coordinate
        )
    )


def create_game(session: Session):
    state = types.GameState(scene="Hungry Beginnings")
    session.add(state_app_to_db(state))

    session.commit()

    query = session.query(model.GameState)
    return query.first()