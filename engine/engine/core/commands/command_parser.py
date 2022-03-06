from typing import Callable, List, Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from engine.core import types

from . import cook, drop, eat, look, move, start, take, trap


class Action(BaseModel):
    name: str
    aliases: List[str]
    handler: Callable[..., types.Response]
    # description: a helpful string for the output


class Actions(BaseModel):
    actions: List[Action]


actions = Actions(
    actions=[
        Action(name="cook", aliases=["cook"], handler=cook.handle_command),
        Action(
            name="drop",
            aliases=["drop", "remove"],
            handler=drop.handle_command,
        ),
        Action(name="eat", aliases=["eat"], handler=eat.handle_command),
        Action(name="look", aliases=["look"], handler=look.handle_command),
        Action(
            name="move", aliases=["move", "go"], handler=move.handle_command
        ),
        Action(name="start", aliases=["start"], handler=start.handle_command),
        Action(
            name="take", aliases=["take", "grab"], handler=take.handle_command
        ),
        Action(
            name="trap",
            aliases=["set trap", "make trap"],
            handler=trap.handle_command,
        ),
    ]
)

null_words = ["the", "a", "an", "at"]


class CommandParser:
    def __init__(self, session, command):
        self.command = " ".join(
            i.lower() for i in command.split() if i not in null_words
        )
        self.action: Optional[Action] = self.get_action()
        self.session: Session = session

    def get_action(self) -> Action:
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

    def normalise_context(self) -> List[str]:
        if self.action is None:
            raise Exception("Expected action to be set by now")

        action = next(a for a in self.action.aliases if a in self.command)
        try:
            context = self.command.split(action, 1)[1].lstrip()
            return context.split()
        except IndexError:
            return []

    def handle_command(self, game: types.Game) -> types.Response:
        if self.action is None:
            return types.Response(
                message=f"Not a valid action. Type 'help' for a list of valid actions.",
            )
        context = self.normalise_context()
        return self.action.handler(self.session, game, context=context)
