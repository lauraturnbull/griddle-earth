from datetime import datetime, timezone
from typing import Optional, Union

from fastapi import HTTPException
from sqlalchemy.orm import Session

from engine.core import types

from . import model


def get_now() -> datetime:
    return datetime.now(timezone.utc)


# app to db
def item_app_to_db(item: Union[types.Item, types.NewItem]) -> model.Item:
    return model.Item(
        item_type=item.item_type.value,
        collection_method=item.collection_method.value,
        **item.dict(exclude={"item_type", "collection_method"}),
    )


def items_app_to_db(items: Union[types.Items, types.NewItems]) -> model.Items:
    return model.Items(
        item=item_app_to_db(items.item), **items.dict(exclude={"item"})
    )


def component_app_to_db(
    component: Union[types.Component, types.NewComponent]
) -> model.Component:
    return model.Component(
        items=[items_app_to_db(i) for i in component.items],
        transports_to_x_coordinate=component.transports_to.x_coordinate
        if component.transports_to
        else None,
        transports_to_y_coordinate=component.transports_to.y_coordinate
        if component.transports_to
        else None,
        **component.dict(exclude={"items", "transports_to"}),
    )


def location_app_to_db(
    location: Union[types.Location, types.NewLocation]
) -> model.Location:
    return model.Location(
        x_coordinate=location.coordinates.x_coordinate,
        y_coordinate=location.coordinates.y_coordinate,
        components=[component_app_to_db(c) for c in location.components],
        **location.dict(exclude={"coordinates", "components"}),
    )


def inventory_app_to_db(
    inventory: Union[types.Inventory, types.NewInventory]
) -> model.Inventory:
    return model.Inventory(
        items=[items_app_to_db(i) for i in inventory.items],
        **inventory.dict(exclude={"items"}),
    )


def game_app_to_db(game: types.Game) -> model.Game:
    return model.Game(
        location=location_app_to_db(game.location) if game.location else None,
        inventory=inventory_app_to_db(game.inventory),
        **game.dict(exclude={"location", "inventory"}),
    )


def new_game_app_to_db(game: types.NewGame) -> model.Game:
    return model.Game(
        inventory=inventory_app_to_db(game.inventory),
        **game.dict(exclude={"location", "inventory"}),
    )


def map_app_to_db(map: Union[types.Map, types.NewMap]) -> model.Map:
    return model.Map(
        locations=[location_app_to_db(i) for i in map.locations],
        **map.dict(exclude={"locations"}),
    )


def adventure_log_app_to_db(
    adventure_log: Union[types.AdventureLog, types.NewAdventureLog]
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
        ],
    )


# db to app


def item_db_to_app(item: model.Item) -> types.Item:
    return types.Item(
        id=item.id,
        name=item.name,
        item_type=types.ItemType(item.item_type),
        health_points=item.health_points,
        collection_method=types.ItemCollectionMethod(item.collection_method),
    )


def items_db_to_app(items: model.Items) -> types.Items:
    return types.Items(
        id=items.id, quantity=items.quantity, item=item_db_to_app(items.item)
    )


def component_db_to_app(component: model.Component) -> types.Component:
    return types.Component(
        id=component.id,
        name=component.name,
        description=component.description,
        is_gateway=component.is_gateway,
        transports_to=types.Coordinates(
            x_coordinate=component.transports_to_x_coordinate,
            y_coordinate=component.transports_to_y_coordinate,
        )
        if component.transports_to_x_coordinate is not None
        and component.transports_to_y_coordinate is not None
        else None,
        items=[items_db_to_app(i) for i in component.items],
    )


def location_db_to_app(location: model.Location) -> types.Location:
    return types.Location(
        id=location.id,
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
        id=inventory.id, items=[items_db_to_app(i) for i in inventory.items]
    )


def game_db_to_app(game: model.Game) -> types.Game:
    return types.Game(
        id=game.id,
        health_points=game.health_points,
        created=game.created,
        location=location_db_to_app(game.location) if game.location else None,
        inventory=inventory_db_to_app(game.inventory),
    )


def map_db_to_app(map: model.Map) -> types.Map:
    return types.Map(
        id=map.id, locations=[location_db_to_app(i) for i in map.locations]
    )


def adventure_log_db_to_app(
    adventure_log: Union[model.AdventureLog],
) -> types.AdventureLog:
    return types.AdventureLog(
        id=adventure_log.id,
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
        ],
    )


def create_new_game(
    session: Session,
    game: types.NewGame,
    map: types.NewMap,
    adventure_log: types.NewAdventureLog,
) -> types.Game:
    # create the game
    game_db = new_game_app_to_db(game)
    session.add(game_db)
    session.commit()
    session.flush()

    # store the map used for this game
    map_db = map_app_to_db(map)
    map_db.game_id = game_db.id
    session.merge(map_db)
    session.commit()

    # store discoverable locations and items based on map
    adventure_log_db = adventure_log_app_to_db(adventure_log)
    adventure_log_db.game_id = game_db.id
    session.add(adventure_log_db)
    session.flush()
    session.commit()

    return game_db_to_app(game_db)


def get_game_by_id(session: Session, game_id: int) -> Optional[types.Game]:
    qry = session.query(model.Game).filter(model.Game.id == game_id)
    game_db = qry.one_or_none()
    if game_db is None:
        return None
    return game_db_to_app(game_db)


def update_game(
    session: Session, game_id: int, new_game_state: types.Game
) -> None:
    new_game_db = game_app_to_db(new_game_state)
    new_game_db.id = game_id
    session.merge(new_game_db)
    session.commit()
    session.flush()
    return


def get_map_by_game_id(
    session: Session,
    game_id: int,
) -> Optional[types.Map]:
    qry = (
        session.query(model.Map).filter(model.Map.game_id == game_id).limit(1)
    )
    map_db = qry.one_or_none()
    if map_db is None:
        return None
    return map_db_to_app(map_db)


def get_adventure_log_by_game_id(
    session: Session,
    game_id: int,
) -> Optional[types.AdventureLog]:
    qry = session.query(model.AdventureLog).filter(
        model.AdventureLog.game_id == game_id
    )
    adventure_log_db = qry.one_or_none()
    if adventure_log_db is None:
        return None
    return adventure_log_db_to_app(adventure_log_db)


def update_adventure_log_discovered_locations(
    session: Session,
    game_id: int,
    location: types.Location,
) -> None:
    qry = session.query(model.AdventureLog).filter(
        model.AdventureLog.game_id == game_id
    )
    adventure_log_db = qry.one_or_none()
    if adventure_log_db is None:
        raise HTTPException(
            status_code=422,
            detail=("No adventure log to update"),
        )
    adventure_log = adventure_log_db_to_app(adventure_log_db)
    existing_location = next(
        (
            loc
            for loc in adventure_log.discovered_locations
            if loc.coordinates == location.coordinates
        ),
        None,
    )
    if not existing_location:
        adventure_log_db.discovered_locations.append(
            location_app_to_db(types.NewLocation(**location.dict()))
        )
        session.commit()
        session.flush()


def update_adventure_log_discovered_items(
    session: Session, game_id: int, item: Union[types.Item, types.NewItem]
) -> None:
    qry = session.query(model.AdventureLog).filter(
        model.AdventureLog.game_id == game_id
    )
    adventure_log_db = qry.one_or_none()
    if adventure_log_db is None:
        raise HTTPException(
            status_code=422,
            detail=("No adventure log to update"),
        )
    adventure_log = adventure_log_db_to_app(adventure_log_db)
    existing_item = next(
        (i for i in adventure_log.discovered_items if i.name == item.name),
        None,
    )
    if not existing_item:
        adventure_log_db.discovered_items.append(
            item_app_to_db(types.NewItem(**item.dict()))
        )
        session.commit()
        session.flush()


def get_map_location_by_coordinates(
    session: Session, game_id: int, coordinates: types.Coordinates
) -> Optional[types.Location]:

    qry = (
        session.query(model.Location)
        .join(model.Map)
        .filter(model.Map.game_id == game_id)
        .filter(model.Location.x_coordinate == coordinates.x_coordinate)
        .filter(model.Location.y_coordinate == coordinates.y_coordinate)
    )

    location_db = qry.one_or_none()
    if location_db is None:
        return None
    return location_db_to_app(location_db)


def update_map_location(
    session: Session, game_id: int, new_location_state: types.Location
) -> None:

    # existing
    qry = (
        session.query(model.Location)
        .join(model.Map)
        .filter(model.Map.game_id == game_id)
        .filter(
            model.Location.x_coordinate
            == new_location_state.coordinates.x_coordinate  # noqa W504
        )
        .filter(
            model.Location.y_coordinate
            == new_location_state.coordinates.y_coordinate  # noqa W504
        )
    )
    location_db = qry.one_or_none()
    # merge with new state
    new_location_db = location_app_to_db(new_location_state)
    new_location_db.id = location_db.id
    session.merge(new_location_db)
    session.commit()
    session.flush()

    return
