from recipe_contents import db
from recipe_contents.models import Recipe


# All recipes
def get_all_recipes():
    all_recipes = db.session.execute(db.select(Recipe)).scalars().all()
    return all_recipes


def get_recipe_by_id(recipe_id):
    recipe = db.session.execute(db.select(Recipe).where(Recipe.id == recipe_id)).scalar()
    return recipe


def api_get_recipe_by_id(recipe_id):
    recipe = db.session.execute(db.select(Recipe).where(Recipe.id == recipe_id)).scalars()
    return recipe


def get_my_recipes(user_id):
    my_recipes = db.session.execute(db.select(Recipe).where(Recipe.user_id == user_id)).scalars().all()
    return my_recipes


def get_recipes_by_category(category_name):
    recipes_by_category = db.session.execute(db.select(Recipe).where(Recipe.category == category_name)).scalars().all()
    return recipes_by_category
