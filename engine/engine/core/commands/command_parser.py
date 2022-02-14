from typing import Any, Callable, Dict, List, Union

from fastapi import HTTPException
from sqlalchemy.orm import Session

from engine.core import types

from . import cook, look, move, start, take, trap

null_words = ["the", "a", "an", "at", "with"]


class CommandParser:
    def __init__(self, session, command):
        self.action: types.Action = self.normalise_action(command)
        self.context: List[str] = self.normalise_context(command)
        self.session: Session = session

    @staticmethod
    def normalise_action(command: str) -> types.Action:
        # maybe need to pop out null_words before getting action
        # e.g. set a trap
        action = next(
            (types.Action(a) for a in types.Action.values() if a in command),
            None,
        )
        if action is None:
            # todo give proper list of actions
            raise HTTPException(
                status_code=422,
                detail=f"{action} is not a valid action. Please choose from:"
                f" {', '.join(types.Action.values())}",
            )

        return action

    def normalise_context(self, command: str) -> List[str]:
        try:
            context = command.lower().split(self.action.value, 1)[1].lstrip()
            return [
                w
                for w in context.replace(",", "").split()
                if w not in null_words
            ]
        except IndexError:
            return []

    def handle_command(self, game: types.Game) -> Any:
        command = types.Command(action=self.action, context=self.context)
        # todo - super gross but will be cleaned up
        command_map: Dict[
            Any,
            Callable[
                [Session, types.Game, types.Command],
                Union[
                    types.LocationOut,
                    types.ComponentNameList,
                    types.ComponentDescription,
                    types.ItemsOut,
                    None,
                ],
            ],
        ]
        command_map = {
            types.Action.start: start.handle_command,
            types.Action.move: move.handle_command,
            types.Action.look: look.handle_command,
            types.Action.take: take.handle_command,
            types.Action.set_trap: trap.handle_command,
            types.Action.cook: cook.handle_command,
        }
        return command_map[self.action](self.session, game, command)
