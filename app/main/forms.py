from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired

class SubmitPostForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')