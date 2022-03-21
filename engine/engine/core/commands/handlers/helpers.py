from typing import List, Optional, Union

from fastapi import HTTPException
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import constants, types


def get_noun_variants(noun: str) -> List[str]:
    return [noun, noun + "s", noun[:-1], noun[:-3] + "y", noun[:-1] + "ies"]


def get_component(
    components: List[types.Component], component_name: str
) -> Optional[types.Component]:
    component_name_variants = get_noun_variants(component_name)
    component = next(
        (c for c in components if c.name.lower() in component_name_variants),
        None,
    )
    return component


def get_items(
    items_list: List[types.Items], item_name: str
) -> Optional[types.Items]:
    items_name_variants = get_noun_variants(item_name)
    items = next(
        (i for i in items_list if i.item.name.lower() in items_name_variants),
        None,
    )
    return items


def move_item_to_inventory(
    session: Session,
    game: types.Game,
    component_name: str,
    item_name: str,
    collection_method: List[types.ItemCollectionMethod],
    take_all: bool = False,
) -> types.Response:

    if game.location is None:
        raise HTTPException(
            status_code=422,
            detail=("No location - game not started"),
        )
    map_location = persister.get_map_location_by_coordinates(
        session=session, game_id=game.id, coordinates=game.location.coordinates
    )
    if map_location is None:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Could not find location at "
                f"x={game.location.coordinates.x_coordinate}, "
                f"y={game.location.coordinates.y_coordinate}"
            ),
        )

    map_component = get_component(
        components=map_location.components, component_name=component_name
    )
    if map_component is None:
        return types.Response(
            message=constants.MISSING_COMPONENT.format(
                component=component_name
            )
        )
    map_items = get_items(items_list=map_component.items, item_name=item_name)

    if map_items is None:
        return types.Response(
            message=constants.MISSING_ITEM_IN_COMPONENT.format(
                item=item_name, component=component_name
            )
        )
    if map_items.item.collection_method not in collection_method:
        # todo fix this
        return types.Response(
            message=constants.FORBIDDEN_ACTION_ITEM.format(
                action=collection_method.value, item=item_name
            )
        )
    if (
        sum(i.quantity for i in game.inventory.items) + map_items.quantity
        > constants.MAX_INVENTORY_SIZE  # noqa W503
    ):
        return types.Response(message=constants.EXCEEDED_MAX_INVENTORY)
    inventory_items: Optional[Union[types.Items, types.NewItems]]
    inventory_items = next(
        (
            i
            for i in game.inventory.items
            if i.item.name == map_items.item.name
            and i.item.health_points == map_items.item.health_points
        ),
        None,
    )

    if inventory_items is None:
        inventory_items = types.NewItems(
            quantity=0, item=types.NewItem(**map_items.item.dict())
        )
        # shouts when adding for the first time
        game.inventory.items.append(inventory_items)  # type: ignore
    quantity_taken = 1
    if take_all:
        inventory_items.quantity += map_items.quantity
        quantity_taken = map_items.quantity
        map_items.quantity = 0
    else:
        inventory_items.quantity += 1
        map_items.quantity -= 1

    if map_items.quantity == 0:
        map_component.items.remove(map_items)
    game.location = map_location

    persister.update_map_location(
        session, game_id=game.id, new_location_state=map_location
    )
    persister.update_game(session, game_id=game.id, new_game_state=game)

    persister.update_adventure_log_discovered_items(
        session, game_id=game.id, item=inventory_items.item
    )
    return types.Response(
        message=constants.TOOK_ITEM.format(
            quantity=quantity_taken, item=item_name
        )
    )


def get_verb(items: List[types.Items]) -> str:
    if len(items) > 1 or any(i.quantity > 1 for i in items):
        return "are"
    return "is"


def sentence_from_list_of_names(
    collection: Union[
        List[types.Component], List[types.Items], List[types.NewItems]
    ]
) -> str:
    use_plural = False
    if all(isinstance(n, types.Component) for n in collection):
        names = [i.name for i in collection]
    else:
        names = [i.item.name for i in collection]
        if len(collection) > 1 or any(i.quantity > 1 for i in collection):
            use_plural = True

    if not use_plural:
        updated_names = []
        for n in names:
            if n[0].lower() in ["a", "e", "i", "o", "u"] and n[-1] != "s":
                updated_names.append("an " + n)
            elif n[-1] != "s":
                updated_names.append("a " + n)
            else:
                updated_names.append(n)
        names = updated_names

    if len(names) == 1:
        return f"{names[0]}."

    else:
        msg = ""
        for n in names[:-1]:
            msg += f"{n}, "
        if msg == "":
            return f"{names[-1]}"
        return f"{msg[:-2]} and {names[-1]}."


def get_location_description(location: types.Location) -> str:
    components_str = sentence_from_list_of_names(location.components)
    return constants.LOCATION_DESCRIPTION.format(
        location=location.description, components=components_str
    )
