from flask import jsonify, request, Blueprint, render_template
from werkzeug.security import check_password_hash

from recipe_contents import db
from recipe_contents.models import Recipe, User

api_blueprint = Blueprint("api", __name__, template_folder="../templates")

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

def check_user(email, password):
    user = User.query.filter_by(email=email).first()
    print(user)
    if check_password_hash(user.password, password):
        print(user.id)
        return user
    return False


@api_blueprint.route("/api")
def api():
    return render_template("api.html")


# Todas la recetas
@api_blueprint.route("/api-get-all")
def api_get_all():
    recipes = db.session.execute(db.select(Recipe)).scalars().all()
    recipe_list = convert_dict(recipes)
    return jsonify(all_recipes=recipe_list)

# Búsqueda por categoría
@api_blueprint.route("/api-show-category")
def api_show_category():
    cat = request.args.get("cat")
    response = db.session.execute(db.select(Recipe).where(Recipe.category == cat)).scalars().all()
    recipe_list = convert_dict(response)
    if recipe_list == []:
        return jsonify(error={"Not found": "Sorry, we don't have this recipe."})
    return jsonify(recipe=recipe_list)
    # URL pruebas: http://127.0.0.1:5000/api-show-category?cat=Plato+principal



