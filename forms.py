from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateField

class EventForm(FlaskForm):
    EventName = StringField('EventName',validators=[DataRequired(),Length(min=2,max=20)])
    EventDescription = StringField('description', validators=[DataRequired(),Length(min=10,max=100)])
    EventDate = DateField('Date', format='%Y-%m-%d')
    submit = SubmitField('Submit')