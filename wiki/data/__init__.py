from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    #__tablename__ = 'table_name_here'
    id = db.Column(db.Integer, primary_key=True)


class Ingredient(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey(Recipe.id), primary_key=True)
    ingredient = db.Column(db.String(32), primary_key=True)
    quantity = db.Column(db.String(16), primary_key=True)

    recipe = db.relationship('Recipe', foreign_keys='Recipe.id')