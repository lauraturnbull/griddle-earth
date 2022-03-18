from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import constants, types
from engine.core.commands.handlers import helpers
from engine.core.resources import recipe_book


def get_recipe(ingredients: List[types.Item]) -> Optional[types.Recipe]:
    # check for specific meals first
    recipes = recipe_book.make_recipe_book().recipes
    specific_item_recipes = [r for r in recipes if r.required_items]
    recipe = next(
        (
            r
            for r in specific_item_recipes
            if set(x.name for x in r.required_items)
            == set(y.name for y in ingredients)  # noqa: W503
        ),
        None,
    )
    # then check for more generic meals
    if recipe is None:
        item_types = {i.item_type for i in ingredients}
        generic_recipes = [r for r in recipes if r.required_types]
        recipe = next(
            (
                r
                for r in generic_recipes
                if set(r.required_types) == item_types
            ),
            None,
        )

        if recipe is None:
            return None
    return recipe


class Ingredients(BaseModel):
    item: types.Item
    quantity: int


def handle_command(
    session: Session, game: types.Game, input: str
) -> types.Response:
    # first we check that the items are in the inventory
    ingredients: List[Ingredients] = []
    raw_items = input.split(", ")

    for item_name in raw_items:
        # the comma separated items might have a quantity
        quantity = 1
        if any(i.isdigit() for i in item_name):
            q, item_name = item_name.split(" ", 1)
            quantity = int(q)

        name_variants = helpers.get_noun_variants(item_name)
        items = next(
            (
                i
                for i in game.inventory.items
                if i.item.name in name_variants and i not in ingredients
            ),
            None,
        )
        if items is None:
            return types.Response(
                message=constants.MISSING_INVENTORY_ITEM.format(
                    item=item_name
                ),
            )
        if items.quantity < quantity:
            return types.Response(
                message=constants.NOT_ENOUGH_INVENTORY_ITEMS.format(
                    quantity=quantity, item=item_name
                )
            )
        ingredients.append(Ingredients(item=items.item, quantity=quantity))

    # fetch the recipe based on the ingredients so we can apply the boost
    recipe = get_recipe([i.item for i in ingredients])
    if recipe is None:
        ingredient_str = helpers.sentence_from_list_of_names(
            [
                types.NewItems(quantity=i.quantity, item=i.item)
                for i in ingredients
            ]
        )
        return types.Response(
            message=constants.MISSING_RECIPE.format(ingredients=ingredient_str)
        )

    new_meal = types.NewItems(
        quantity=1,
        item=types.NewItem(
            name=recipe.name,
            item_type=types.ItemType.meal,
            health_points=recipe.boost
            * sum(
                i.item.health_points * i.quantity for i in ingredients
            ),  # noqa W503
            collection_method=types.ItemCollectionMethod.cook,
        ),
    )

    # remove ingredients from inventory
    for i in game.inventory.items:
        ingredient = next((x for x in ingredients if x.item == i.item), None)
        if ingredient:
            i.quantity -= ingredient.quantity

    game.inventory.items = [i for i in game.inventory.items if i.quantity > 0]

    # add meal to inventory
    game.inventory.items.append(new_meal)  # type: ignore
    persister.update_game(session, game.id, game)

    # update adventure log
    persister.update_adventure_log_discovered_items(
        session, game.id, item=new_meal.item
    )

    return types.Response(
        message=constants.NEW_MEAL.format(
            meal_name=new_meal.item.name,
            health_points=new_meal.item.health_points,
        )
    )


action = types.Action(
    name="cook",
    aliases=["cook"],
    handler=handle_command,
    description="Combines ingredients from your inventory into meals using the recipe book. Item names must be separated by a comma. The quantity of each item used defaults to 1.",
    examples=[
        "cook apple, strawberry, raspberry",
        "cook 4 mushrooms, 2 onions",
    ],
)
