from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from engine.adapters.postgres import persister
from engine.core import types
from engine.core.resources.base import recipe_book

from . import helpers


def get_recipe(ingredients: List[types.Item]) -> types.Recipe:
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
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Could not find recipe for {item_types}"
                    "item types in recipe book."
                ),
            )
    return recipe


def handle_command(
    session: Session, game: types.Game, command: types.Command
) -> types.ItemsOut:
    # first we check that the items are in the inventory
    ingredients: List[types.Item] = []
    flattened_items = list(set(command.context))
    for item_name in flattened_items:
        name_variants = helpers.get_noun_variants(item_name)
        item = next(
            (
                i.item
                for i in game.inventory.items
                if i.item.name in name_variants
            ),
            None,
        )
        if item is None:
            raise HTTPException(
                status_code=422,
                detail=f"No {item_name} in inventory found to cook with",
            )
        ingredients.append(item)

    recipe = get_recipe(ingredients)

    new_meal = types.NewItems(
        quantity=1,
        item=types.NewItem(
            name=recipe.name,
            item_type=types.ItemType.meal,
            health_points=recipe.boost
            * sum(i.health_points for i in ingredients),  # noqa W503
            collection_method=types.ItemCollectionMethod.cook,
        ),
    )

    # remove ingredients from inventory
    for i in game.inventory.items:
        if i.item in ingredients:
            i.quantity -= 1
    game.inventory.items = [i for i in game.inventory.items if i.quantity > 0]

    # add meal to inventory
    game.inventory.items.append(new_meal)  # type: ignore
    persister.update_game(session, game.id, game)

    # update adventure log
    persister.update_adventure_log_discovered_items(
        session, game.id, item=new_meal.item
    )

    return types.ItemsOut(
        quantity=1,
        name=new_meal.item.name,
        health_points=new_meal.item.health_points,
    )
