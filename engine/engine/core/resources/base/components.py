from engine.core import constants, types


def make_discard_pile(items: types.NewItems) -> types.NewComponent:
    return types.NewComponent(
        name=constants.DISCARD_PILE,
        description="This is a mound of your discarded items.",
        items=[items],
    )
