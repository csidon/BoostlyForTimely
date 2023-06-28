# Creating HTML forms with classes from flask_wtf

from flask_wtf import FlaskForm				# Provides form validation functionality
from wtforms.widgets import ListWidget, CheckboxInput				
from wtforms import SubmitField, DateField, TimeField, IntegerField, HiddenField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, NumberRange


class QuerySelectMultipleFieldWithCheckbox(QuerySelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class WaitAlertForm(FlaskForm):
    slotStartDate = DateField('Date of available appointment slot', format="%Y-%m-%d", id="dateInput")
    slotStartTime = TimeField('Appointment Start Time', validators=[DataRequired()], id="timeInput")
    slotLength =  IntegerField('Slot availability length (in mins)', validators=[DataRequired()], id="availabilityInputInput")
    slotStartDate = DateField('Date of available appointment slot', format="%Y-%m-%d")
    slotStartTime = TimeField('Appointment Start Time', validators=[DataRequired()])
    slotLength =  IntegerField('Slot availability length (in mins)', validators=[DataRequired(), NumberRange(min=15)])

    submit = SubmitField(label='Send Alert')

class SelectAlerteesForm(FlaskForm):
    selectedClients = HiddenField('Selected clients to notify')


