from sqlalchemy.orm import Session

from engine.core import types

from .helpers import move_item_to_inventory


def handle_command(
    session: Session, game: types.Game, input: str
) -> types.Response:

    """
    Input pattern is like:
    take <item name> from <component name>
    or
    take all <item names>s from <component name>

    command.action == take
    command.context == [all] <item name>[s] from <component name>
    """

    take_all = False
    context = input.split(" ")
    if context[0] == "all":
        take_all = True
        context = context[1:]

    delimiter = "from"
    try:
        delimiter_index = context.index(delimiter)
    except ValueError:
        return types.Response(message="From where?")

    item_name = " ".join(context[:delimiter_index])
    component_name = " ".join(context[delimiter_index + 1 :])

    return move_item_to_inventory(
        session,
        game=game,
        item_name=item_name,
        component_name=component_name,
        take_all=take_all,
        collection_method=[
            types.ItemCollectionMethod.forage,
            types.ItemCollectionMethod.cook,
        ],
    )
