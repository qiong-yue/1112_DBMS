from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models import User
import wtforms

wtforms.BooleanField

class RegisterForm(FlaskForm):
    fname = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    pwd = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    bdate = StringField('Birth Date', validators=[DataRequired()])
    phone = StringField('Cellphone', validators=[DataRequired(), Length(10)])
    adr = StringField('Address(Country)', validators=[DataRequired(), Length(min=4, max=30)])
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already token, please choose another one. ')
class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    pwd = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Submit')

