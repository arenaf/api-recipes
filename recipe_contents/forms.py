from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField, EmailField, PasswordField
from wtforms.validators import DataRequired, URL, InputRequired, Email
import email_validator


# Register a new recipe
class RecipeForm(FlaskForm):
    title = StringField("Recipe name ", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    ingredients = TextAreaField("Ingredients", validators=[InputRequired()],
                                render_kw={"rows": 4, 'data-char-count-max': 250})
    instructions = TextAreaField("Instructions", validators=[InputRequired()],
                                 render_kw={"rows": 6, 'data-char-count-max': 500})
    category = SelectField("Category",
                           choices=[("Breakfast"), ("Dinner"), ("Lunch"), ("Snack"), ("Starters")])
    submit = SubmitField("Post Recipe")


# Creation of new users
class RegisterUserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email("Please enter a valid email address.")])
    password = PasswordField("Password", validators=[DataRequired()])
    check_password = PasswordField("Repeat password", validators=[DataRequired()])
    submit = SubmitField("Register")


# Login form for existing users
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email("Please enter a valid email address.")])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


# Forgot password
class ChangePasswordForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email("Please enter a valid email address.")])
    password = PasswordField("Password", validators=[DataRequired()])
    check_password = PasswordField("Repeat password", validators=[DataRequired()])
    submit = SubmitField("Change Password")
