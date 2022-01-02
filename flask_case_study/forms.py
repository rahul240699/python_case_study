from flask_wtf import FlaskForm
from sqlalchemy.orm import subqueryload
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_case_study.models import User

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class dataEntry(FlaskForm):
    email=StringField('Email', validators=[DataRequired(),Email()])
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    user_type=StringField('User Type',validators=[DataRequired()])
    submit=SubmitField('Enter and Send Mail')