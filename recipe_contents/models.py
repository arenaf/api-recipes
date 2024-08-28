from flask_login import UserMixin
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from recipe_contents import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalar()


class Recipe(db.Model):
    __tablename__ = "recipe"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    ingredients: Mapped[str] = mapped_column(String(250), nullable=False)
    instructions: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[str] = mapped_column(String(250), nullable=False)
    # Relación con los usuarios
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="user_recipe")


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    # Relaciona la tabla usuario con la tabla de tareas
    user_recipe = relationship("Recipe", back_populates="user")