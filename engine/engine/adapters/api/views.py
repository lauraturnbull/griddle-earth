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
def create_new_game():
    # makes game and initial game state
    # saves to db
    # returns game state

    new_state = persister.create_game(session)
    return new_state



@app.get("/{game_id}/state")
def get_game_state():
    """
    Returns the current state of the player including:
    - location
    - direction
    - description of the current scene
    - list of items available to access in scene
    """
    return


@app.get("/{id}/inventory")
def get_player_inventory():
    """
    Returns the player's inventory
    """
    return


@app.post("/{game_id}/command")
def handle_command(input: str) -> types.Command:
    """
    Handles interaction with a scene
    validates

    """
    parser = command_parser.CommandParser()
    command = parser.parse(input)
    current_state = get_game_state(game_id)
    if command.action == "move":
        move.handle_command(current_state, command)
    return command
