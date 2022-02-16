from engine.core import constants, types


def make_discard_pile(items: types.NewItems) -> types.NewComponent:
    return types.NewComponent(
        name=constants.DISCARD_PILE,
        description="A mound of discarded items",
        items=[items],
    )
