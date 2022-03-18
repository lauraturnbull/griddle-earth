from sqlalchemy.orm import Session

from engine.core import types
from engine.core.commands.handlers import ALL_ACTIONS


def handle_command(
    session: Session, game: types.Game, context: str
) -> types.HelpResponse:
    return types.HelpResponse(
        actions=[types.ActionOut(**a.dict()) for a in ALL_ACTIONS]
    )


action = types.Action(
    name="help",
    aliases=["help"],
    handler=handle_command,
    description="You're doing it!",
)
