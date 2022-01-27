from engine.core import types, command_parser
from engine.core.commands import move
from sqlalchemy.orm import sessionmaker
from engine.adapters.sqlite import core, persister

from fastapi import FastAPI

app = FastAPI()

Session = sessionmaker(bind=core.engine)
session = Session()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/game")
def create_new_game() -> types.Game:
    new_game = persister.create_game(session)
    return new_game


@app.get("/{game_id}/state")
def get_game_state(game_id: int) -> types.GameState:
    """
    Returns the current state of the player including:
    - location
    - direction
    - description of the current scene
    - list of items available to access in scene
    """
    game_state = persister.get_most_recent_game_state(
        session, game_id=game_id
    )
    return game_state


@app.get("/{id}/inventory")
def get_player_inventory():
    """
    Returns the player's inventory
    """
    return


@app.post("/{game_id}/command")
def handle_command(game_id: int, input: str) -> types.GameState:
    """
    Handles interaction with a scene
    validates

    """
    parser = command_parser.CommandParser()
    command = parser.parse(input)
    current_state = persister.get_most_recent_game_state(session, game_id)
    if command.action == "move":
        new_state = move.handle_command(current_state, command)
        state=persister.append_game_state(session, game_id, new_state)
    return state
