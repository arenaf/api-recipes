from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from flask_bootstrap import Bootstrap5

from recipe_contents.models import Recipe, User
from recipe_contents.forms import RecipeForm
from flask_login import UserMixin, LoginManager
from recipe_contents import app, db
from recipe_contents.recipes_view.recipes_routes import recipes_blueprint
from recipe_contents.user_routes.user_routes import user_blueprint


# Connect to Database
db.init_app(app)


with app.app_context():
    db.create_all()

app.register_blueprint(recipes_blueprint)
app.register_blueprint(user_blueprint)


def convert_dict(response):
    recipe_list = []
    for recipe_data in response:
        recipe_list.append(
            {
                "id": recipe_data.id,
                "title": recipe_data.title,
                "img_url": recipe_data.img_url,
                "ingredients": recipe_data.ingredients,
                "instructions": recipe_data.instructions,
                "category": recipe_data.category,
            }
        )
    return recipe_list




# -------- API --------
@app.route("/api_search")
def api_search():
    cat = request.args.get("cat")
    response = db.session.execute(db.select(Recipe).where(Recipe.category == cat)).scalars().all()
    recipe_list = convert_dict(response)
    if recipe_list == []:
        return jsonify(error={"Not found": "Sorry, we don't have this recipe."})
    return jsonify(recipe=recipe_list)
    # URL pruebas: http://127.0.0.1:5000/api_search?cat=Plato+principal


# HTTP POST - Create Record
# Se añade a través de postman, rellenar los datos y send
@app.route("/api_add", methods=["POST"])
def api_add_new_recipe():
    new_recipe = Recipe(
        title=request.form.get("title"),
        img_url=request.form.get("img_url"),
        ingredients=request.form.get("ingredients"),
        instructions=request.form.get("instructions"),
        category=request.form.get("category"),
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify(response={"Success": "Successfully added the new recipe."})



# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:recipe_id>", methods=["PATCH"])
def update_price(recipe_id):
    # cafe = db.get_or_404(Cafe, cafe_id)
    recipe = Recipe.query.get(recipe_id)
    if recipe:
        new_price = request.args.get("new_price")  # request.form.get para formularios html
        recipe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"Success": "Successfully added the new recipe."})
    else:
        return jsonify(error={"Not found": "Sorry a recipe with that id was not found in the database."})



