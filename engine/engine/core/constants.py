# todo - in future hp can be determined based on easy/hard mode
MAX_HP = 1000
MOVE_LOCATION_HP: int = 300
MAX_INVENTORY_SIZE: int = 10
DISCARD_PILE = "discarded items"

FORBIDDEN_ACTION_ITEM = "You are not able to {action} {item}."
FORBIDDEN_DIRECTION = "You cannot go that way."
EXCEEDED_MAX_INVENTORY = (
    f"Cannot exceed maximum inventory size of "
    f"{MAX_INVENTORY_SIZE}. Cook, consume, or drop "
    f"items to reduce the size of your inventory."
)
# todo - maybe randomise these sentences?
ATE_ITEM = "You ate {item} (+{health_points}hp)."
DROPPED_ITEM = "You have dropped 1x {item} into a discarded pile."
TOOK_ITEM = "You have taken {quantity}x {item}."
LOCATION_DESCRIPTION = "{location} Looking around you see {components}"
COMPONENT_DESCRIPTION = (
    "{component} Looking closer you see that there are {items}"
)
MISSING_COMPONENT = "Could not find any {component}."
MISSING_DIRECTION = "Which direction do you want to move?"
MISSING_INVENTORY_ITEM = "You don't have any {item} in your inventory."
MISSING_ITEM_IN_COMPONENT = "There aren't any {item} in the {component}."
MISSING_RECIPE = "Could not find a recipe for {ingredients}."
NEW_MEAL = "Added {meal_name} ({health_points}hp) to your inventory."
NOTHING_TO_HUNT = "It doesn't seem like there's anything worthwhile to hunt in the {component}."
FAILED_TRAP = (
    "You set a trap in the {component} using one of your {bait} "
    "and settle down to wait. After a time a flash of movement "
    "catches your eye. It’s your escaped prey, and it’s taken "
    "your bait with it (-1x {bait})."
)
SUCCESSFUL_TRAP = (
    "You set a trap in the {component} using one of your "
    "{bait} and settle down to wait. Your patience is been "
    "rewarded with a {prey} (1x {prey} added to inventory)."
)
