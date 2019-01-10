from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_login import current_user
from app.models import User

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=32)])
    bio = TextAreaField('Bio', validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('Submit')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None and user.username is not current_user.username:
            raise ValidationError('Please use a different username.')