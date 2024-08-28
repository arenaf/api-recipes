from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

app = Flask(__name__)
app.config['SECRET_KEY'] = "ui8402Lou802lkKowkS_y720floR97"
Bootstrap5(app)


login_manager = LoginManager()
login_manager.init_app(app)

class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
db = SQLAlchemy(model_class=Base)



from recipe_contents import main