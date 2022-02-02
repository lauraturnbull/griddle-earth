from sqlalchemy.orm import Session
from engine.core import types
from datetime import datetime, timezone

from . import model


def get_now() -> datetime:
    return datetime.now(timezone.utc)


# app to db
def item_app_to_db(item: types.Item) -> model.Item:
    return model.Item(
        item_type=item.item_type.value,
        **item.dict(exclude={"item_type"})
    )


def items_app_to_db(items: types.Items) -> model.Items:
    return model.Items(
        item=item_app_to_db(items.item),
        quantity=items.quantity
    )


def location_app_to_db(location: types.Location) -> model.Location:
    return model.Location(
        x_coordinate=location.coordinates.x_coordinate,
        y_coordinate=location.coordinates.y_coordinate,
        items=[items_app_to_db(i) for i in location.items],
        **location.dict(exclude={"coordinates", "items"})
    )


def inventory_app_to_db(inventory: types.Inventory) -> model.Inventory:
    return model.Inventory(
        items=[items_app_to_db(i) for i in inventory.items]
    )


def game_app_to_db(game: types.Game) -> model.Game:
    return model.Game(
        location=location_app_to_db(game.location),
        inventory=inventory_app_to_db(game.inventory),
        **game.dict(exclude={"location", "inventory"})
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
        coordinates=types.Coordinates(
            x_coordinate=location.x_coordinate,
            y_coordinate=location.y_coordinate,
        ),
        name=location.name,
        description=location.description,
        region=types.Region(location.region),
        items=[items_db_to_app(i) for i in location.items]
    )


def inventory_db_to_app(inventory: model.Inventory) -> types.Inventory:
    return types.Inventory(
        items=[items_db_to_app(i) for i in inventory.items]
    )


def game_db_to_app(game: model.Game) -> types.Game:
    return types.Game(
        id=game.id,
        health_points=game.health_points,
        created=game.created,
        location=location_db_to_app(game.location),
        inventory=inventory_db_to_app(game.inventory)
    )


def create_game(session: Session) -> types.Game:
    new_game = model.Game(
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
        inventory=model.Inventory()
    )

    session.add(new_game)
    session.commit()

    return game_db_to_app(new_game)


def get_game_by_id(session, game_id: int) -> types.Game:
    qry = (
        session.query(model.Game)
        .filter(model.Game.id == game_id)
    )
    game_db = qry.one_or_none()
    return game_db_to_app(game_db)


def update_game(
    session,
    game_id: int,
    new_game_state: types.Game
) -> types.Game:
    new_game_db = game_app_to_db(new_game_state)
    new_game_db.id = game_id
    session.merge(new_game_db)
    session.flush()
    session.commit()
    return game_db_to_app(new_game_db)


def get_map_location_by_coordinates(
    session,
    game_id: int,
    coordinates: types.Coordinates
) -> types.Location:
    qry = (
        session.query(model.Location)
        .filter(model.Location.map.game_id == game_id)
        .filter(model.Location.x_coordinate == coordinates.x_coordinate)
        .filter(model.Location.y_coordinate == coordinates.y_coordinate)
        .limit(1)
    )
    # todo - handle none scenario
    location_db = qry.one_or_none()
    return location_db_to_app(location_db)
