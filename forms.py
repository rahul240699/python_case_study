from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateField
from wtforms.widgets import TextArea

class EventForm(FlaskForm):
    EventName = StringField('Event Name',validators=[DataRequired(),Length(min=2,max=20)])
    EventDescription = StringField('Description', validators=[DataRequired(),Length(min=10,max=100)],widget=TextArea())
    EventDate = DateField('Date', format='%Y-%m-%d')
    submit = SubmitField('Submit')