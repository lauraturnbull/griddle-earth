from engine.core import types

# n,e,s,w?, change to dict that takes in the current value and returns the new coordinate obj
DIRECTIONS = ["north", "east", "south", "west"]


def handle_command(coordinates: types.Coordinates, command: types.Command):
    for direction in command.context:
        if direction in DIRECTIONS:
            if direction == "north":
                coordinates.y_coordinate += 1
            if direction == "east":
                coordinates.x_coordinate += 1
            if direction == "south":
                coordinates.y_coordinate -= 1
            if direction == "west":
                coordinates.x_coordinate -= 1
        else:
            pass
            # todo - raise something

    # todo - current_state.created = get_now()

    return coordinates
