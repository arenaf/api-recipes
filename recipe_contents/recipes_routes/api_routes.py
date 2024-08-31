from flask import jsonify, request, Blueprint, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_login import current_user

from recipe_contents import db
from recipe_contents.models import Recipe, User
from recipe_contents.recipes_routes.db_queries import get_all_recipes, get_recipe_by_id, api_get_recipe_by_id, \
    get_my_recipes, get_recipes_by_category

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


# Create token
@api_blueprint.route("/token", methods=["GET"])
def create_token():
    if not current_user.is_authenticated:
        return jsonify(response={"msg": "Bad username or password"}), 401
    if current_user.is_authenticated:
        user = User.query.filter_by(email=current_user.email).first()
        access_token = create_access_token(identity=user.id)
        return jsonify(response={"token": access_token, "user_id": user.id})
    return jsonify(error={"Not found": "No existe email"})


@api_blueprint.route("/api")
def api():
    return render_template("api.html")


# Todas la recetas
@api_blueprint.route("/api-get-all")
def api_get_all():
    # recipes = db.session.execute(db.select(Recipe)).scalars().all()
    recipes = get_all_recipes()
    recipe_list = convert_dict(recipes)
    return jsonify(all_recipes=recipe_list)


@api_blueprint.route("/api-show-recipe", methods=["GET"])
def api_show_recipe():
    recipe_id = request.args.get("recipe_id")
    # requested_post = db.session.execute(db.select(Recipe).where(Recipe.id == recipe_id)).scalars()
    requested_post = api_get_recipe_by_id(recipe_id)
    recipe_list = convert_dict(requested_post)
    if recipe_list == []:
        return jsonify(error={"Not found": "Sorry, we don't have this recipe."})
    return jsonify(all_recipes=recipe_list)


# Mostrar mis recetas
@api_blueprint.route("/api-my-recipes")
@jwt_required()
def api_my_recipes():
    user_id = get_jwt_identity()
    # user_recipes_only = db.session.execute(db.select(Recipe).where(Recipe.user_id == user_id)).scalars().all()
    user_recipes_only = get_my_recipes(user_id)
    recipe_list = convert_dict(user_recipes_only)
    if recipe_list == []:
        return jsonify(error={"Not found": "Sorry, we don't have this recipe."})
    return jsonify(recipe=recipe_list)


# Búsqueda por categoría
@api_blueprint.route("/api-show-category")
def api_show_category():
    category_name = request.args.get("cat")
    # response = db.session.execute(db.select(Recipe).where(Recipe.category == cat)).scalars().all()
    requested_category = get_recipes_by_category(category_name)
    recipe_list = convert_dict(requested_category)
    if recipe_list == []:
        return jsonify(error={"Not found": "Sorry, we don't have this recipe."})
    return jsonify(recipe=recipe_list)
    # URL pruebas: http://127.0.0.1:5000/api-show-category?cat=Plato+principal


# HTTP POST - Create Record
# Se añade a través de postman, rellenar los datos y send.
@api_blueprint.route("/api-new-recipe", methods=["POST"])
@jwt_required()
def api_add_new_recipe():
    user_id = get_jwt_identity()
    if user_id:
        new_recipe = Recipe(
            title=request.args.get("title"),
            img_url=request.args.get("img_url"),
            ingredients=request.args.get("ingredients"),
            instructions=request.args.get("instructions"),
            category=request.args.get("category"),
            user_id=user_id,
        )
        db.session.add(new_recipe)
        db.session.commit()
        return jsonify(response={"Success": "Successfully added the new recipe."})
    else:
        return jsonify(response={"Forbidden": "Make sure you have the correct api_key."})


# HTTP PUT/PATCH - Update Record
@api_blueprint.route("/api-edit-recipe/<int:recipe_id>", methods=["PUT"])
@jwt_required()
def api_edit_recipe(recipe_id):
    user_id = get_jwt_identity()
    # recipe_to_edit = db.get_or_404(Recipe, recipe_id)
    recipe_to_edit = get_recipe_by_id(recipe_id)
    print(recipe_to_edit.id, recipe_id, user_id)
    if user_id == recipe_to_edit.user_id:
        recipe_to_edit.title = request.args.get("title")
        recipe_to_edit.img_url = request.args.get("img_url")
        recipe_to_edit.ingredients = request.args.get("ingredients")
        recipe_to_edit.instructions = request.args.get("instructions")
        recipe_to_edit.category = request.args.get("category")
        db.session.commit()
        return jsonify(response={"Success": "Successfully modified the recipe."})
    else:
        return jsonify(error={"Not found": "You can't modify the recipe, you are not the author."})


@api_blueprint.route("/api-delete-recipe/<int:recipe_id>", methods=["DELETE"])
@jwt_required()
def api_delete_recipe(recipe_id):
    user_id = get_jwt_identity()
    # recipe_to_delete = db.get_or_404(Recipe, recipe_id)
    recipe_to_delete = get_recipe_by_id(recipe_id)
    if user_id == recipe_to_delete.user_id:
        db.session.delete(recipe_to_delete)
        db.session.commit()
        return jsonify(response={"Success": "Successfully deleted the recipe."})
    if user_id != recipe_to_delete.user_id:
        return jsonify(response={"Forbidden": "You can't delete the recipe, you are not the author."})
    else:
        return jsonify(response={"Forbidden": "Make sure you have the correct api_key."})
