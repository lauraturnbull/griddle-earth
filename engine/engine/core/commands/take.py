from engine.core import types
from fastapi import HTTPException
from .helpers import move_item_to_inventory


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
    # todo need to check that the collection method is forage

    return move_item_to_inventory(
        session,
        game=game,
        item_name=item_name,
        component_name=component_name,
        take_all=take_all
    )
