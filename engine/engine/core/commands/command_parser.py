from typing import Any, List

from fastapi import HTTPException

from engine.adapters.postgres import persister
from engine.core import types

from . import look, move, take, trap

# pop list of common fluff words
# or just grab from known list of items?
# there should only be one item per list
null_words = ["the", "a", "an", "at"]

# take? map to same action as grab
actions = ["take", "look", "move", "use", "start", "set trap"]


class CommandParser:
    def __init__(self, session, command):
        self.action = self.normalise_action(command)
        self.context = self.normalise_context(command)
        self.session = session

    @staticmethod
    def normalise_action(command: str) -> str:
        # maybe need to pop out null_words before getting action
        # e.g. set a trap
        action = next((a for a in actions if a in command), None)
        if action is None:
            raise HTTPException(
                status_code=422,
                detail=f"{action} is not a valid action. Please choose from:"
                f" {', '.join(actions)}",
            )

        return action

    def normalise_context(self, command: str) -> List[str]:
        try:
            context = command.lower().split(self.action, 1)[1].lstrip()
            return [w for w in context.split() if w not in null_words]
        except IndexError:
            return []

    def handle_command(self, game: types.Game) -> Any:
        command = types.Command(action=self.action, context=self.context)

        if self.action == "start":
            location = persister.get_map_location_by_coordinates(
                self.session,
                game_id=game.id,
                coordinates=types.Coordinates(x_coordinate=0, y_coordinate=0),
            )
            game.location = location
        if self.action == "move":
            return move.handle_command(
                session=self.session, game=game, command=command
            )
        if self.action == "look":
            # read only, no update
            return look.handle_command(game=game, command=command)
        if self.action == "take":
            return take.handle_command(
                session=self.session, game=game, command=command
            )
        if self.action == "set trap":
            return trap.handle_command(
                session=self.session, game=game, command=command
            )
        return persister.update_game(
            self.session, game_id=game.id, new_game_state=game
        )
