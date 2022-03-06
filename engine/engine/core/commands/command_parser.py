from typing import Callable, List, Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from engine.core import types

from . import cook, drop, eat, enter, look, move, start, take, trap


class Action(BaseModel):
    name: str
    aliases: List[str]
    handler: Callable[..., types.Response]
    # description: a helpful string for the output


class Actions(BaseModel):
    actions: List[Action]


Cook = Action(name="cook", aliases=["cook"], handler=cook.handle_command)
Drop = Action(
    name="drop", aliases=["drop", "remove"], handler=drop.handle_command
)
Eat = Action(name="eat", aliases=["eat"], handler=eat.handle_command)
Enter = Action(
    name="enter",
    aliases=["enter", "step through", "step into"],
    handler=enter.handle_command,
)
Look = Action(name="look", aliases=["look"], handler=look.handle_command)
Move = Action(name="move", aliases=["move", "go"], handler=move.handle_command)
Start = Action(name="start", aliases=["start"], handler=start.handle_command)
Take = Action(
    name="take", aliases=["take", "grab"], handler=take.handle_command
)
Trap = Action(
    name="trap", aliases=["set trap", "make trap"], handler=trap.handle_command
)

actions = Actions(
    actions=[Cook, Drop, Eat, Enter, Look, Move, Start, Take, Trap]
)

null_words = ["the", "a", "an", "at"]


class CommandParser:
    def __init__(self, session, command):
        self.command = " ".join(
            i.lower() for i in command.split() if i not in null_words
        )
        self.action: Optional[Action] = self.get_action()
        self.session: Session = session

    def get_action(self) -> Optional[Action]:
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
            raise Exception("expected action to be set by now")

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
