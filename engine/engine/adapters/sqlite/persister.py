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

def items_db_to_app(items: model.Items) -> types.Items:
    return types.Items(
        quantity=items.quantity,
        item=types.Item(
            name=items.item.name,
            item_type=types.ItemType(items.item.item_type),
            health_points=items.item.health_points
        )
    )


def location_db_to_app(location: model.Location) -> types.Location:
    return types.Location(
        x_coordinate=location.x_coordinate,
        y_coordinate=location.y_coordinate,
        name=location.name,
        description=location.description,
        region=types.Region(location.region),
        items=[items_db_to_app(i) for i in location.items]
    )


def state_db_to_app(state: model.GameState) -> types.GameState:
    return types.GameState(
        health_points=state.health_points,
        created=state.created,
        location=location_db_to_app(state.location)
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
                created=get_now(),
                location=model.Location(
                    x_coordinate=0,
                    y_coordinate=0,
                    name="Hungry Beginnings",
                    description="The very beginning of your journey.",
                    region=types.Region.home_plains.value,
                    items=[
                        model.Items(
                            quantity=3,
                            item=model.Item(
                                name="apple",
                                item_type=types.ItemType.fruit.value,
                                health_points=30,
                            )
                        )
                    ]
                ),
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