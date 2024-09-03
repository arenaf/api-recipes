"""
Document with the routes that are used in the API.
Includes the creation of the token.
"""

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


# -------- Create token --------
@api_blueprint.route("/token", methods=["GET"])
def create_token():
    if not current_user.is_authenticated:
        return jsonify(response={"msg": "Bad username or password"}), 401
    if current_user.is_authenticated:
        user = User.query.filter_by(email=current_user.email).first()
        access_token = create_access_token(identity=user.id)
        return render_template("api.html", access_token=access_token)
    return jsonify(error={"Not found": "The email does not exist"})


@api_blueprint.route("/api")
def api():
    return render_template("api.html", current_user=current_user)


# -------- All recipes ---------
@api_blueprint.route("/api-get-all")
def api_get_all():
    recipes = get_all_recipes()
    recipe_list = convert_dict(recipes)
    return jsonify(all_recipes=recipe_list)


# -------- Show a recipe --------
@api_blueprint.route("/api-show-recipe", methods=["GET"])
def api_show_recipe():
    recipe_id = request.args.get("recipe_id")
    requested_post = api_get_recipe_by_id(recipe_id)
    recipe_list = convert_dict(requested_post)
    if recipe_list == []:
        return jsonify(error={"Not found": "Sorry, we don't have this recipe."})
    return jsonify(all_recipes=recipe_list)


# -------- Show my recipes --------
@api_blueprint.route("/api-my-recipes")
@jwt_required()
def api_my_recipes():
    user_id = get_jwt_identity()
    user_recipes_only = get_my_recipes(user_id)
    recipe_list = convert_dict(user_recipes_only)
    if recipe_list == []:
        return jsonify(error={"Not found": "Sorry, we don't have this recipe."})
    return jsonify(recipe=recipe_list)


# -------- Search by category --------
@api_blueprint.route("/api-show-category")
def api_show_category():
    category_name = request.args.get("cat")
    requested_category = get_recipes_by_category(category_name)
    recipe_list = convert_dict(requested_category)
    if recipe_list == []:
        return jsonify(error={"Not found": "Sorry, we don't have this recipe."})
    return jsonify(recipe=recipe_list)


# -------- Add new recipe --------
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


# -------- Modify recipe --------
@api_blueprint.route("/api-edit-recipe/<int:recipe_id>", methods=["PUT"])
@jwt_required()
def api_edit_recipe(recipe_id):
    user_id = get_jwt_identity()
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


# -------- Delete recipe --------
@api_blueprint.route("/api-delete-recipe/<int:recipe_id>", methods=["DELETE"])
@jwt_required()
def api_delete_recipe(recipe_id):
    user_id = get_jwt_identity()
    recipe_to_delete = get_recipe_by_id(recipe_id)
    if user_id == recipe_to_delete.user_id:
        db.session.delete(recipe_to_delete)
        db.session.commit()
        return jsonify(response={"Success": "Successfully deleted the recipe."})
    if user_id != recipe_to_delete.user_id:
        return jsonify(response={"Forbidden": "You can't delete the recipe, you are not the author."})
    else:
        return jsonify(response={"Forbidden": "Make sure you have the correct api_key."})
