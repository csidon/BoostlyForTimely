# Creating HTML forms with classes from flask_wtf

from flask_wtf import FlaskForm				# Provides form validation functionality
from wtforms.widgets import ListWidget, CheckboxInput				
from wtforms import StringField, SubmitField, DateField, SelectMultipleField, TimeField, IntegerField, HiddenField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired



class QuerySelectMultipleFieldWithCheckbox(QuerySelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class WaitAlertForm(FlaskForm):
	# staff = QuerySelectField		# additional functionality to create ability to change
	slotStartDate = DateField('Date of available appointment slot', format="%Y-%m-%d", id="dateInput")
	slotStartTime = TimeField('Appointment Start Time', validators=[DataRequired()], id="timeInput")
	slotLength =  IntegerField('Slot availability length (in mins)', validators=[DataRequired()], id="availabilityInputInput")


    # To get the date that is selected, check what day of the week <<isoweekday()>> it is, 
    ## then search all availtime_ids that match the isoweekday() of slotStartDate and display the clients
    # [(clientpref_id, availtimes_id)]

    # clients = []

    # availtimes = 


	submit = SubmitField(label='Send Alert')

class SelectAlerteesForm(FlaskForm):
    selectedClients = HiddenField('Selected clients to notify')



    # id = db.Column(db.Integer, primary_key = True)
    # slotStartDateTime = db.Column(db.DateTime, nullable=False)
    # slotLength = db.Column(db.Integer, nullable=False)
    # sendStatus = db.Column(db.String(30))
    # sendFlag = db.Column(db.Integer)
    # lastUpdated = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # msgTmpl = db.Column(db.Integer, db.ForeignKey('msgtmpl.id'), nullable=False)
    # staff = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    # client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

