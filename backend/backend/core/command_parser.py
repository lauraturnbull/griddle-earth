from . import types, exceptions
from fastapi import HTTPException

# pop list of common fluff words
# or just grab from known list of items?
# there should only be one item per list
null_words = ["the", "a", "an"]

# take? map to same action as grab
actions = ["grab", "look", "move", "use"]


class CommandParser:

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
    def normalise_context(command) -> str:
        # remove the action and flatten (todo- what about leading spaces)
        context = command.lower().split(' ', 1)[1]
        filtered_context = [w for w in context.split() if w not in null_words]
        return "".join(filtered_context)

    def parse(self, command: str) -> types.CommandOut:
        # need to check action exists, raise custom error
        action = self.normalise_action(command)
        self.validate_command(action)
        return types.CommandOut(
            action=action,
            context=self.normalise_context(command)
        )