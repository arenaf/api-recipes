from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from flask_bootstrap import Bootstrap5
from forms import RecipeForm

'''

My API documentation:
https://documenter.getpostman.com/view/34666668/2sA3JFCQN2

'''

API_KEY = "ABC"  # Para poder borrar un registro

app = Flask(__name__)
app.config['SECRET_KEY'] = "ui8402Lou802lkKowkS_y720floR97"
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Recipe TABLE Configuration
class Recipe(db.Model):
    __tablename__ = "recipe"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    ingredients: Mapped[str] = mapped_column(String(250), nullable=False)
    instructions: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[str] = mapped_column(String(250), nullable=False)
    # # Relación con los ingredientes
    # ingredients = relationship("Ingredients", back_populates="recipe")


# class Ingredients(db.Model):
#     __tablename__ = "ingredients"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     ingredient: Mapped[str] = mapped_column(String(250), nullable=False)
#     # Relación con la tabla Recipe
#     recipe_id: Mapped[int] = mapped_column(Integer, ForeignKey("recipe.id"))
#     recipe = relationship("Recipe", back_populates="ingredients")


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    recipes = db.session.execute(db.select(Recipe)).scalars().all()
    return render_template("index.html", recipes=recipes)


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


# ver
@app.route("/api_all_recipes")
def api_get_all():
    response = db.session.execute(db.select(Recipe)).scalars().all()
    recipe_list = convert_dict(response)
    return jsonify(recipe=recipe_list)


# Ir una receta
@app.route("/show-recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    requested_post = db.session.execute(db.select(Recipe).where(Recipe.id == recipe_id)).scalar()
    return render_template("recipe.html", recipe=requested_post)

# Mostrar recetas de una categoría
@app.route("/show-category/<category_name>")
def show_category(category_name):
    requested_category = db.session.execute(db.select(Recipe).where(Recipe.category == category_name)).scalars().all()
    return render_template("index.html", recipes=requested_category)


# Añadir una receta
@app.route("/new-recipe", methods=["GET", "POST"])
def add_new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        new_recipe = Recipe(
            title=request.form.get("title"),
            img_url=request.form.get("img_url"),
            ingredients=request.form.get("ingredients"),
            instructions=request.form.get("instructions"),
            category=request.form.get("category"),
        )
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("post_recipe.html", form=form)


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
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    # cafe = db.get_or_404(Cafe, cafe_id)
    recipe = Recipe.query.get(cafe_id)
    if recipe:
        new_price = request.args.get("new_price")  # request.form.get para formularios html
        recipe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"Success": "Successfully added the new cafe."})
    else:
        return jsonify(error={"Not found": "Sorry a cafe with that id was not found in the database."})


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:recipe_id>", methods=["DELETE"])
def report_closed(recipe_id):
    api_key = request.args.get("api-key")
    if API_KEY == api_key:
        recipe = Recipe.query.get(recipe_id)
        if recipe:
            db.session.delete(recipe)
            db.session.commit()
            return jsonify(response={"Success": "Successfully deleted the recipe."})
        else:
            return jsonify(error={"Not found": "Sorry a recipe with that id was not found in the database."})
    else:
        return jsonify({"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."})






if __name__ == '__main__':
    app.run(debug=True)
