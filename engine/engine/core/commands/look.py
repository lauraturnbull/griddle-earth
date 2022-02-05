from engine.core import types
from typing import Union, List, Optional
from fastapi import HTTPException


def get_component(
    components: List[types.Component], component_name: str
) -> types.Component:
    component_name_variants = [
        component_name,
        component_name + "s",
        component_name[:-1]
    ]

    component = next(
        (c for c in components if c.name.lower() in component_name_variants),
        None
    )

    if component is None:
        raise HTTPException(
            status_code=422,
            detail=f"Cannot find location {component_name} to look at"
        )

    return component


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
