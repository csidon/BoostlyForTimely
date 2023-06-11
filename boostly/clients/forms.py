# Creating HTML forms with classes from flask_wtf

from flask_wtf import FlaskForm				# Provides form validation functionality				
from wtforms import StringField, SubmitField, IntegerField, RadioField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, Email, NumberRange


class ClientForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email (used for notification purposes only)', validators=[DataRequired(), Email()])
    mobile = IntegerField('Mobile (used for notification purposes only)')

    delete = SubmitField(label="Delete", render_kw={'formnovalidate': True})
    submit = SubmitField('Update')



class QuerySelectMultipleFieldWithCheckbox(QuerySelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class ClientPrefForm(FlaskForm):
    minDuration = IntegerField('Minimum timeslot (You will not be notified for anything less than this timeslot)', default=60, 
        validators=[DataRequired(), NumberRange(min=15)])
    availall = RadioField('Notify for all timeslots that become available?', choices=[(0, "No"),(1,"Yes")])
    availtimes = QuerySelectMultipleFieldWithCheckbox("Select timeslots that you want to be notified for", allow_blank=True)
    
    delete = SubmitField(label="Delete", render_kw={'formnovalidate': True})
    submit = SubmitField('Update')

