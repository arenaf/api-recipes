from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL, InputRequired


class RecipeForm(FlaskForm):
    title = StringField("Nombre de la receta ", validators=[DataRequired()])
    img_url = StringField("URL de la imagen", validators=[DataRequired(), URL()])
    ingredients = TextAreaField("Ingredientes", validators=[InputRequired()],
                                render_kw={"rows": 4, 'data-char-count-max': 250})
    instructions = TextAreaField("Instrucciones", validators=[InputRequired()],
                                 render_kw={"rows": 6, 'data-char-count-max': 500})
    category = SelectField("Categoría",
                           choices=[("Desayuno"), ("Entrante"), ("Plato principal"), ("Merienda"), ("Cena")])
    submit = SubmitField("Publicar Receta")


# class IngredientForm(FlaskForm):
#     ingredient = StringField("Ingrediente ", validators=[DataRequired()])
