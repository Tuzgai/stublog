from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email
from app.models import User

class InviteUserForm(FlaskForm):
    email = StringField('Username', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email is already being used.')