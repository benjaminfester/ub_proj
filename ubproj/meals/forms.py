from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class AddMealForm(FlaskForm):
    title = StringField('What did you eat?', validators=[DataRequired()])
    content = TextAreaField('Description of what you have eaten', validators=[DataRequired()])
    calories = IntegerField('Calories', validators=[DataRequired()])
    submit = SubmitField('Add Meal')

