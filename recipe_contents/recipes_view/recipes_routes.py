from flask import render_template, request, redirect, url_for, Blueprint
from flask_login import current_user

from recipe_contents import db
from recipe_contents.forms import RecipeForm
from recipe_contents.models import Recipe
from recipe_contents.user_routes.user_routes import user_logged

recipes_blueprint = Blueprint("recipes", __name__, template_folder="../templates")


@recipes_blueprint.route("/")
def home():
    recipes = db.session.execute(db.select(Recipe)).scalars().all()
    return render_template("index.html", all_recipes=recipes, current_user=current_user)


# Ir una receta
@recipes_blueprint.route("/show-recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    requested_post = db.session.execute(db.select(Recipe).where(Recipe.id == recipe_id)).scalar()
    return render_template("recipe.html", show_recipe=requested_post)

# Mostrar recetas de una categoría
@recipes_blueprint.route("/show-category/<category_name>")
def show_category(category_name):
    requested_category = db.session.execute(db.select(Recipe).where(Recipe.category == category_name)).scalars().all()
    return render_template("index.html", all_recipes=requested_category)


# Añadir una receta
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
