from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField
from wtforms.fields import choices
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_case_study.models import User
from flask_login import current_user
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SelectClass(FlaskForm):
    classVal = SelectField('Select Class',choices=[(8,8),(9,9),(10,10)])
    submit = SubmitField('Submit')

class AdminEntry(FlaskForm):
    email=StringField('Email', validators=[DataRequired(),Email()])
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Enter and Send Mail')

class RegistrationForm(FlaskForm):
	email=StringField('School Email ID',
		        validators=[DataRequired(),Email()])
	name=StringField('Name',
		        validators=[DataRequired()])
	fname=StringField('Father-Name',
		        validators=[DataRequired()])
	mname=StringField('Mother-Name',
		        validators=[DataRequired()])
	classs=SelectField('Class',
		        validators=[DataRequired()],default="Please enter the class",choices=[('1'),('2'),('3'),('4'),('5'),('6'),('7'),('8'),('9'),('10')])
	addr=StringField('Address',
		        validators=[DataRequired()])
	phno=StringField('Phone-No',
		        validators=[DataRequired()])
	person_email=StringField('Personal Email ID',validators=[Email()])
	submit=SubmitField('Enroll-Student')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class ClassDetails(FlaskForm):
	classs=SelectField('Class',
		        validators=[DataRequired()] ,choices=[('1'),('2'),('3'),('4'),('5'),('6'),('7'),('8'),('9'),('10')])
	submit=SubmitField('Get-Class Details')

class EventForm(FlaskForm):
    EventName = StringField('Event Name',validators=[DataRequired(),Length(min=2,max=20)])
    EventDescription = StringField('Description', validators=[DataRequired(),Length(min=10,max=100)],widget=TextArea())
    EventDate = DateField('Date', format='%Y-%m-%d')
    submit = SubmitField('Submit')