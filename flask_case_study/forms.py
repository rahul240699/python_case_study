from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields import choices
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_case_study.models import User

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SelectClass(FlaskForm):
    classVal = SelectField('Select Class',choices=[(8,8),(9,9),(10,10)])
    submit = SubmitField('Submit')