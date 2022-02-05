from engine.core import types
from engine.adapters.postgres import persister
from fastapi import HTTPException


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
    # Drop s from end of the item name to make it singular.
    # There must be a lib out there for this...
    if take_all:
        item_name = item_name[:-1]
    component_name = " ".join(context[delimiter_index+1:])
    # def get items from map

    component = next(
        (
            c for c in game.location.components
            if c.name.lower() == component_name
        ),
        None
    )

    # todo - try searching with an s on the end
    if component is None:
        raise HTTPException(
            status_code=422,
            detail=f"Cannot find location {component_name}"
        )

    map_items = next(
        (i for i in component.items if i.item.name.lower() == item_name),
        None
    )
    if map_items is None or map_items.quantity == 0:
        raise HTTPException(
            status_code=422,
            detail=f"No {item_name}s found in {component_name}"
        )

    inventory_items = next(
        (i for i in game.inventory.items if i.item.name == item_name),
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

    persister.update_game(session, game_id=game.id, new_game_state=game)

    # if map_items.quantity ==0:
    #     component.items.remove(map_items)

    return inventory_items
