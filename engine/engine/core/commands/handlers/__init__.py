from .adventure_log import action as adventure_log
from .cook import action as cook
from .drop import action as drop
from .eat import action as eat
from .enter import action as enter
from .inventory import action as inventory
from .look import action as look
from .move import action as move
from .start import action as start
from .take import action as take
from .trap import action as trap

ALL_ACTIONS = [
    adventure_log,
    cook,
    drop,
    eat,
    enter,
    inventory,
    look,
    move,
    start,
    take,
    trap,
]
