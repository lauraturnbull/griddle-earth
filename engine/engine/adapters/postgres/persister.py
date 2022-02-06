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


def component_app_to_db(component: types.Component) -> model.Component:
    return model.Component(
        items=[items_app_to_db(i) for i in component.items],
        **component.dict(exclude={"items"})
    )


def location_app_to_db(location: types.Location) -> model.Location:
    return model.Location(
        x_coordinate=location.coordinates.x_coordinate,
        y_coordinate=location.coordinates.y_coordinate,
        components=[component_app_to_db(c) for c in location.components],
        **location.dict(exclude={"coordinates", "components"})
    )


def inventory_app_to_db(inventory: types.Inventory) -> model.Inventory:
    return model.Inventory(
        items=[items_app_to_db(i) for i in inventory.items]
    )


def game_app_to_db(game: types.Game) -> model.Game:
    return model.Game(
        location=location_app_to_db(game.location) if game.location else None,
        inventory=inventory_app_to_db(game.inventory),
        **game.dict(exclude={"location", "inventory"})
    )


def map_app_to_db(map: types.Map) -> model.Map:
    return model.Map(
        locations=[location_app_to_db(i) for i in map.locations]
    )


def adventure_log_app_to_db(
    adventure_log: types.AdventureLog
) -> model.AdventureLog:
    return model.AdventureLog(
        discovered_locations=[
            location_app_to_db(i) for i in adventure_log.discovered_locations
        ],
        discoverable_locations=[
            location_app_to_db(i) for i in adventure_log.discoverable_locations
        ],
        discovered_items=[
            item_app_to_db(i) for i in adventure_log.discovered_items
        ],
        discoverable_items=[
            item_app_to_db(i) for i in adventure_log.discoverable_items
        ]
    )

# db to app


def item_db_to_app(item: model.Item) -> types.Item:
    return types.Item(
        name=item.name,
        item_type=types.ItemType(item.item_type),
        health_points=item.health_points
    )


def items_db_to_app(items: model.Items) -> types.Items:
    return types.Items(
        quantity=items.quantity,
        item=item_db_to_app(items.item)
    )


def component_db_to_app(component: model.Component) -> types.Component:
    return types.Component(
        name=component.name,
        description=component.description,
        items=[items_db_to_app(i) for i in component.items]
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
        components=[component_db_to_app(i) for i in location.components],
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
        location=location_db_to_app(game.location) if game.location else None,
        inventory=inventory_db_to_app(game.inventory)
    )


def map_db_to_app(map: model.Map) -> types.Map:
    return types.Map(
        locations=[location_db_to_app(i) for i in map.locations]
    )


def adventure_log_db_to_app(
    adventure_log: model.AdventureLog
) -> types.AdventureLog:
    return types.AdventureLog(
        discovered_locations=[
            location_db_to_app(i) for i in adventure_log.discovered_locations
        ],
        discoverable_locations=[
            location_db_to_app(i) for i in adventure_log.discoverable_locations
        ],
        discovered_items=[
            item_db_to_app(i) for i in adventure_log.discovered_items
        ],
        discoverable_items=[
            item_db_to_app(i) for i in adventure_log.discoverable_items
        ]
    )


def create_new_game(
    session: Session,
    game: types.NewGame,
    map: types.Map,
    adventure_log: types.AdventureLog
) -> types.Game:
    # create the game
    game_db = game_app_to_db(game)
    session.add(game_db)
    session.commit()

    # store the map used for this game
    map_db = map_app_to_db(map)
    map_db.game_id = game_db.id
    session.add(map_db)
    session.commit()

    # store discoverable locations and items based on map
    adventure_log_db = adventure_log_app_to_db(adventure_log)
    adventure_log_db.game_id = game_db.id
    session.add(adventure_log_db)
    session.commit()

    return game_db_to_app(game_db)


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


def get_map_by_game_id(
    session,
    game_id: int,
) -> types.Map:
    qry = (
        session.query(model.Map)
        .filter(model.Map.game_id == game_id)
        .limit(1)
    )
    map_db = qry.one_or_none()
    return map_db_to_app(map_db)


def get_adventure_log_by_game_id(
    session,
    game_id: int,
) -> types.AdventureLog:
    qry = (
        session.query(model.AdventureLog)
        .filter(model.AdventureLog.game_id == game_id)
        .limit(1)
    )
    adventure_log_db = qry.one_or_none()
    return adventure_log_db_to_app(adventure_log_db)


def get_map_location_by_coordinates(
    session,
    game_id: int,
    coordinates: types.Coordinates
) -> types.Location:

    qry = (
        session.query(model.Location)
        .join(model.Map)
        .filter(model.Map.game_id == game_id)
        .filter(model.Location.x_coordinate == coordinates.x_coordinate)
        .filter(model.Location.y_coordinate == coordinates.y_coordinate)
    )

    # todo - handle none scenario
    location_db = qry.one_or_none()
    return location_db_to_app(location_db)
