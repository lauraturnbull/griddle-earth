from engine.core import types

# n,e,s,w?, change to dict that takes in the current value and returns the new coordinate obj
DIRECTIONS = ["north", "east", "south", "west"]


def handle_command(current_state: types.GameState, command: types.Command):
    direction = command.context
    if direction in DIRECTIONS:
        if direction == "north":
            current_state.coordinates.y += 1
        elif direction == "east":
            current_state.coordinates.x += 1
        elif direction == "south":
            current_state.coordinates.y -= 1
        elif direction == "west":
            current_state.coordinates.x -= 1
    else:
        pass
        # raise something

    # save to db
    return current_state
