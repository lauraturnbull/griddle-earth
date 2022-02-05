from engine.core import types
from engine.adapters.postgres import persister
from fastapi import HTTPException
from typing import List


def get_noun_variants(noun: str) -> List[str]:
    return [
        noun,
        noun + "s",
        noun[:-1]
    ]


def get_component(
    components: List[types.Component], component_name: str
) -> types.Component:
    component_name_variants = get_noun_variants(component_name)

    component = next(
        (c for c in components if c.name.lower() in component_name_variants),
        None
    )

    if component is None:
        raise HTTPException(
            status_code=422,
            detail=f"Cannot find location {component_name}"
        )

    return component


def get_items(items_list: List[types.Items], item_name: str) -> types.Items:
    items_name_variants = get_noun_variants(item_name)

    items = next(
        (i for i in items_list if i.item.name.lower() in items_name_variants),
        None
    )

    if items is None:
        raise HTTPException(
            status_code=422,
            detail=f"Cannot find any {item_name} to take"
        )
    return items


def handle_command(
    session, game: types.Game, command: types.Command
) -> types.Items:

    """
    Input pattern is like:
    take <item name> from <component name>
    or
    take all <item names>s from <component name>

    command.action == take
    command.context == [all] <item name>[s] from <component name>
    """

    take_all = False
    context = command.context
    if command.context[0] == "all":
        take_all = True
        context = context[1:]

    delimiter = "from"
    try:
        delimiter_index = context.index(delimiter)
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=(
                f"You must provide the location when taking items, i.e: "
                f"take {' '.join(command.context)} from ___"
            )
        )

    item_name = " ".join(context[:delimiter_index])
    component_name = " ".join(context[delimiter_index+1:])

    map_component = get_component(
        components=game.location.components, component_name=component_name
    )
    map_items = get_items(
        items_list=map_component.items, item_name=item_name
    )

    inventory_items = next(
        (i for i in game.inventory.items if i.item.name == map_items.item.name),
        None
    )

    if inventory_items is None:
        inventory_items = types.Items(
            quantity=0,
            item=map_items.item
        )
        game.inventory.items.append(inventory_items)

    if take_all:
        inventory_items.quantity += map_items.quantity
        map_items.quantity = 0
    else:
        inventory_items.quantity += 1
        map_items.quantity -= 1

    if map_items.quantity == 0:
        map_component.items.remove(map_items)

    persister.update_game(session, game_id=game.id, new_game_state=game)

    return inventory_items
