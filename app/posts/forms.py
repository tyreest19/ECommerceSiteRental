from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ItemForm(FlaskForm):
    """
    Form for users to post items
    """
    name = StringField('Item\'s Name', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    cost = FloatField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post Item')