from typing import Union

from fastapi import HTTPException
from sqlalchemy.orm import Session

from engine.core import types

from .helpers import move_item_to_inventory


def handle_command(
    session: Session, game: types.Game, command: types.Command
) -> Union[types.Items, types.NewItems]:

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
                "You must provide the location when taking items, i.e: "
                "take [[all] item] from [place]"
            ),
        )

    item_name = " ".join(context[:delimiter_index])
    component_name = " ".join(context[delimiter_index + 1 :])
    # todo need to check that the collection method is forage

    return move_item_to_inventory(
        session,
        game=game,
        item_name=item_name,
        component_name=component_name,
        take_all=take_all,
    )
