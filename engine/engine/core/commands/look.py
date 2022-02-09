from engine.core import types
from typing import Union
from .helpers import get_component


def handle_command(
    location: types.Location, command: types.Command
) -> Union[types.ComponentNameList, types.ComponentDescription]:
    if "around" in command.context:
        return types.ComponentNameList(
            names=[c.name for c in location.components]
        )

    component_name = " ".join(command.context).lower()
    component = get_component(location.components, component_name)
    return types.ComponentDescription(description=component.description)
