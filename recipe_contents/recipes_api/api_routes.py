from flask import jsonify, request, Blueprint, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_login import current_user
from werkzeug.security import check_password_hash
# from flask_jwt_extended import create_access_token
from recipe_contents import db
from recipe_contents.models import Recipe, User
import jwt


api_blueprint = Blueprint("api", __name__, template_folder="../templates")

secret_jwt = "1234"
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


# HTTP POST - Create Record
# Se añade a través de postman, rellenar los datos y send.
@api_blueprint.route("/api-new-recipe", methods=["POST"])
@jwt_required()
def api_add_new_recipe():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user:
        new_recipe = Recipe(
            title=request.args.get("title"),
            img_url=request.args.get("img_url"),
            ingredients=request.args.get("ingredients"),
            instructions=request.args.get("instructions"),
            category=request.args.get("category"),
            user_id=user.id,
        )
        db.session.add(new_recipe)
        db.session.commit()
        return jsonify(response={"Success": "Successfully added the new recipe."})
    else:
        return jsonify(response={"Forbidden": "Make sure you have the correct api_key."})


@api_blueprint.route("/api-delete-recipe/<int:recipe_id>", methods=["DELETE"])
@jwt_required()
def api_delete_recipe(recipe_id):
    user_id = get_jwt_identity()
    recipe_to_delete = db.get_or_404(Recipe, recipe_id)
    if user_id == recipe_to_delete.user_id:
        db.session.delete(recipe_to_delete)
        db.session.commit()
        return jsonify(response={"Success": "Successfully deleted the recipe."})
    if user_id != recipe_to_delete.user_id:
        return jsonify(response={"Forbidden": "You can't delete the recipe, you are not the author."})
    else:
        return jsonify(response={"Forbidden": "Make sure you have the correct api_key."})




