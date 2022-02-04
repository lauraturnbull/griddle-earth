from engine.core import types
from typing import Union


def handle_command(
    location: types.Location, command: types.Command
) -> Union[types.ComponentNameList, types.ComponentDescription]:
    if "around" in command.context:
        return types.ComponentNameList(
            names=[c.name for c in location.components]
        )

    component_name = " ".join(command.context)
    component = next(
        (c for c in location.components if c.name.lower() == component_name),
        None
    )
    if component is None:
        # todo - handle
        pass
    return types.ComponentDescription(description=component.description)
