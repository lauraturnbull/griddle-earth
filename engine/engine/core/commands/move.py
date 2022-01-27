from engine.core import types
from engine.adapters.sqlite import persister, model

# n,e,s,w?, change to dict that takes in the current value and returns the new coordinate obj
DIRECTIONS = ["north", "east", "south", "west"]


def handle_command(current_state: types.GameState, command: types.Command):
    direction = command.context
    # deep copy?
    if direction in DIRECTIONS:
        if direction == "north":
            current_state.y_coordinate += 1
        elif direction == "east":
            current_state.x_coordinate += 1
        elif direction == "south":
            current_state.y_coordinate -= 1
        elif direction == "west":
            current_state.x_coordinate -= 1
    else:
        pass
        # todo - raise something

    # todo - current_state.created = get_now()
    new_state =types.GameState(
        **current_state.dict()
    )

    return new_state
