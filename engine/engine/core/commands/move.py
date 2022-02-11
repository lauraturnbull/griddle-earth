from engine.adapters.postgres import persister
from engine.core import types

# n,e,s,w?
DIRECTIONS = ["north", "east", "south", "west"]


def handle_command(
    session, game: types.Game, command: types.Command
) -> types.Location:
    if game.location is None:
        return persister.get_map_location_by_coordinates(
            session,
            game_id=game.id,
            coordinates=types.Coordinates(x_coordinate=0, y_coordinate=0),
        )
    coordinates = game.location.coordinates
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

    new_location = persister.get_map_location_by_coordinates(
        session, game_id=game.id, coordinates=coordinates
    )

    # update the game state
    game.location = new_location
    game.health_points -= 50

    persister.update_game(session, game_id=game.id, new_game_state=game)

    persister.update_adventure_log_discovered_locations(
        session, game_id=game.id, location=game.location
    )

    return new_location
