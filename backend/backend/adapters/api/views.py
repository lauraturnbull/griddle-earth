from backend.core import types, command_parser

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/{id}/state")
def get_player_state():
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


@app.post("/{id}/command")
def post_player_command(command: str) -> types.CommandOut:
    """
    Handles interaction with a scene
    validates

    """
    parser = command_parser.CommandParser()
    return parser.parse(command)
