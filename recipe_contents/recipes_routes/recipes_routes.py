from flask import render_template, request, redirect, url_for, Blueprint
from flask_login import current_user

from recipe_contents import db
from recipe_contents.forms import RecipeForm
from recipe_contents.models import Recipe
from recipe_contents.recipes_routes.db_queries import get_all_recipes, get_recipe_by_id, get_my_recipes, \
    get_recipes_by_category
from recipe_contents.user_routes.user_routes import user_logged


recipes_blueprint = Blueprint("recipes", __name__, template_folder="../templates")


@recipes_blueprint.route("/")
def home():
    recipes = db.session.execute(db.select(Recipe)).scalars().all()
    # recipes = get_all_recipes()
    return render_template("index.html", all_recipes=recipes, current_user=current_user)


# -------- Show a recipe --------
@recipes_blueprint.route("/show-recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    # requested_post = db.session.execute(db.select(Recipe).where(Recipe.id == recipe_id)).scalar()
    requested_post = get_recipe_by_id(recipe_id)
    return render_template("recipe.html", show_recipe=requested_post)


# -------- Show my recipes --------
@recipes_blueprint.route("/my-recipes")
@user_logged
def my_recipes():
    # user_recipes_only = db.session.execute(db.select(Recipe).where(Recipe.user_id == current_user.id)).scalars().all()
    user_recipes_only = get_my_recipes(current_user.id)
    return render_template("index.html", all_recipes=user_recipes_only, current_user=current_user)


# -------- Search by category --------
@recipes_blueprint.route("/show-category/<category_name>")
def show_category(category_name):
    # requested_category = db.session.execute(db.select(Recipe).where(Recipe.category == category_name)).scalars().all()
    requested_category = get_recipes_by_category(category_name)
    return render_template("index.html", all_recipes=requested_category)


# -------- Add new recipe --------
@recipes_blueprint.route("/new-recipe", methods=["GET", "POST"])
@user_logged
def add_new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        new_recipe = Recipe(
            title=request.form.get("title"),
            img_url=request.form.get("img_url"),
            ingredients=request.form.get("ingredients"),
            instructions=request.form.get("instructions"),
            category=request.form.get("category"),
            user_id=current_user.id,
        )
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for("recipes.home"))
    return render_template("post_recipe.html", form=form)


# -------- Modify recipe --------
@recipes_blueprint.route("/edit-recipe/<int:recipe_id>", methods=["GET", "POST"])
@user_logged
def edit_recipe(recipe_id):
    # recipe_to_edit = db.get_or_404(Recipe, recipe_id)
    recipe_to_edit = get_recipe_by_id(recipe_id)
    modify_recipe = RecipeForm(
        title=recipe_to_edit.title,
        img_url=recipe_to_edit.img_url,
        ingredients=recipe_to_edit.ingredients,
        instructions=recipe_to_edit.instructions,
        category=recipe_to_edit.category,
    )
    if modify_recipe.validate_on_submit():
        recipe_to_edit.title = modify_recipe.title.data
        recipe_to_edit.img_url = modify_recipe.img_url.data
        recipe_to_edit.ingredients = modify_recipe.ingredients.data
        recipe_to_edit.instructions = modify_recipe.instructions.data
        recipe_to_edit.category = modify_recipe.category.data
        db.session.commit()
        return redirect(url_for("recipes.home"))
    return render_template("post_recipe.html", form=modify_recipe, edit=True, current_user=current_user)


# -------- Delete recipe --------
@recipes_blueprint.route("/delete-recipe/<int:recipe_id>")
@user_logged
def delete_recipe(recipe_id):
    # recipe_to_delete = db.get_or_404(Recipe, recipe_id)
    recipe_to_delete = get_recipe_by_id(recipe_id)
    db.session.delete(recipe_to_delete)
    db.session.commit()
    return redirect(url_for("recipes.home"))
