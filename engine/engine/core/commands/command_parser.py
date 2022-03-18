from typing import Optional, Union

from sqlalchemy.orm import Session

from engine.core import constants, types
from engine.core.commands.handlers import ALL_ACTIONS
from engine.core.commands.handlers.help import action as help

# todo - inventory, adventure log, (map?)

null_words = ["the", "a", "an", "at"]


class CommandParser:
    def __init__(self, session, command):
        self.command = " ".join(
            i.lower() for i in command.split() if i not in null_words
        )
        self.action: Optional[types.Action] = self.get_action()
        self.session: Session = session

    def get_action(self) -> Optional[types.Action]:
        # help appended separately to avoid circular import
        actions = types.Actions(actions=[*ALL_ACTIONS, help])
        action = next(
            (
                a
                for a in actions.actions
                for alias in a.aliases
                if alias in self.command
            ),
            None,
        )
        return action

    def normalise_context(self) -> str:
        if self.action is None:
            raise Exception("expected action to be set by now")

        action = next(a for a in self.action.aliases if a in self.command)
        try:
            context = self.command.split(action, 1)[1].lstrip()
            return context
        except IndexError:
            return ""

    def handle_command(
        self, game: types.Game
    ) -> Union[types.Response, types.HelpResponse]:
        if self.action is None:
            return types.Response(
                message=constants.INVALID_ACTION,
            )
        context = self.normalise_context()
        return self.action.handler(self.session, game, context)
