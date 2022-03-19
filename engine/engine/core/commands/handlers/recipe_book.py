from sqlalchemy.orm import Session

from engine.core import types
from engine.core.resources import recipe_book


def handle_command(
    session: Session, game: types.Game, context: str
) -> types.RecipeBookResponse:
    recipes = recipe_book.make_recipe_book().recipes
    recipes_out = [types.RecipeOut(**r.dict()) for r in recipes]
    return types.RecipeBookResponse(recipes=recipes_out)


action = types.Action(
    name="recipe book",
    handler=handle_command,
    aliases=["recipe book", "recipes", "cook book"],
    description="Recipes for cooking ingredients.",
)
