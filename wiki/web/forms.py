"""
    Forms
    ~~~~~
"""
from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField
from wtforms.fields.html5 import DecimalField
from wtforms.validators import InputRequired, Optional
from wtforms.validators import ValidationError

from wiki.core import clean_url
from wiki.web import current_wiki
from wiki.web import current_users

from urllib.parse import quote


class URLForm(Form):
    url = TextField('', [InputRequired()])

    def validate_url(form, field):
        if current_wiki.exists(field.data):
            raise ValidationError('The URL "%s" exists already.' % field.data)

    def clean_url(self, url):
        return clean_url(url)


class SearchForm(Form):
    term = TextField('', [InputRequired()])
    ignore_case = BooleanField(
        description='Ignore Case',
        # FIXME: default is not correctly populated
        default=True)


class EditorForm(Form):
    title = TextField('', [InputRequired()])
    body = TextAreaField('', [InputRequired()])
    tags = TextField('')


class LoginForm(Form):
    name = TextField('', [InputRequired()])
    password = PasswordField('', [InputRequired()])

    def validate_name(form, field):
        user = current_users.get_user(field.data)
        if not user:
            raise ValidationError('This username does not exist.')

    def validate_password(form, field):
        user = current_users.get_user(form.name.data)
        if not user:
            return
        if not user.check_password(field.data):
            raise ValidationError('Username and password do not match.')


class NewRecipeForm(Form):
    name = TextField(validators=[InputRequired()])

    def validate_name(form, field):
        if current_wiki.exists('recipes/' + quote(field.data)):
            raise ValidationError('Recipe %s already exists.' % field.data)


class RecipeForm(Form):
    # Required Fields
    name = TextField(validators=[InputRequired()])
    ingredients = TextField(validators=[InputRequired()])
    instructions = TextAreaField(validators=[InputRequired()])
    serving_size = DecimalField(validators=[InputRequired()])
    servings = DecimalField(validators=[InputRequired()])

    # Nutitional Information (Optional, not always known)
    fat = DecimalField(validators=[Optional()])  # Grams
    saturated_fat = DecimalField(validators=[Optional()])  # Grams
    trans_fat = DecimalField(validators=[Optional()])  # Grams

    cholesterol = DecimalField(validators=[Optional()])  # Milligrams
    sodium = DecimalField(validators=[Optional()])  # Milligrams

    carbohydrates = DecimalField(validators=[Optional()])  # Grams
    fiber = DecimalField(validators=[Optional()])  # Grams
    sugar = DecimalField(validators=[Optional()])  # Grams
    added_sugar = DecimalField(validators=[Optional()])  # Grams

    protein = DecimalField(validators=[Optional()])  # Grams

    vitamin_d = DecimalField(validators=[Optional()])  # Micrograms
    calcium = DecimalField(validators=[Optional()])  # Milligrams
    iron = DecimalField(validators=[Optional()])  # Milligrams
    potassium = DecimalField(validators=[Optional()])  # Milligrams

