from engine.core import types
from fastapi import HTTPException
from . import move, look
from typing import List
from engine.adapters.postgres import persister
# pop list of common fluff words
# or just grab from known list of items?
# there should only be one item per list
null_words = ["the", "a", "an", "at"]

# take? map to same action as grab
actions = ["grab", "look", "move", "use", "look"]


class CommandParser:

    def __init__(self, session, command):
        self.action = self.normalise_action(command)
        self.context = self.normalise_context(command)
        self.session = session

    @staticmethod
    def validate_command(action: str):
        if action not in actions:
            raise HTTPException(
                status_code=422,
                detail=f"{action} is not a valid action. Please choose from:"
                       f" {', '.join(actions)}"
            )

    @staticmethod
    def normalise_action(command: str) -> str:
        return command.lower().split()[0]

    @staticmethod
    def normalise_context(command) -> List[str]:
        # remove the action and flatten (todo- what about leading spaces)
        context = command.lower().split(' ', 1)[1]
        filtered_context = [w for w in context.split() if w not in null_words]
        return filtered_context

    def handle_command(self, game: types.Game):
        self.validate_command(self.action)
        command = types.Command(action=self.action,context=self.context)
        new_state = types.Game(**game.dict())

        if self.action == "move":
            new_state.location = move.handle_command(
                session=self.session,
                game=new_state,
                command=command
            )
            new_state.health_points -= 50
        elif self.action == "look":
            # read only, no update
            return look.handle_command(
                location=game.location,
                command=command
            )
        return persister.update_game(
            self.session,
            game_id=game.id,
            new_game_state=new_state
        )
