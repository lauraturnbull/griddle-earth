from typing import Union

from fastapi import HTTPException

from engine.core import types

from .helpers import get_component


def handle_command(
    game: types.Game, command: types.Command
) -> Union[types.ComponentNameList, types.ComponentDescription]:
    if game.location is None:
        raise HTTPException(
            status_code=422,
            detail=("No location - game not started"),
        )
    if "around" in command.context:
        return types.ComponentNameList(
            names=[c.name for c in game.location.components]
        )

    component_name = " ".join(command.context).lower()
    component = get_component(game.location.components, component_name)
    return types.ComponentDescription(description=component.description)
