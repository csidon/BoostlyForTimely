# Creating HTML forms with classes from flask_wtf

from flask_wtf import FlaskForm				# Provides form validation functionality				
from wtforms import StringField, SubmitField, TextAreaField, SelectField, RadioField, DateField, SelectMultipleField, TimeField, IntegerField
from wtforms.validators import DataRequired


class WaitAlertForm(FlaskForm):
	alertSubject = StringField('Subject', validators=[DataRequired()], default = 'A new slot has opened up!')
	alertBody = TextAreaField('Alert Message', validators=[DataRequired()])		# Default message is created upon instantiation in route.
	slotStartDate = DateField('Date of available appointment slot', format="%Y-%m-%d")
	slotStartTime = TimeField('Appointment Start Time', validators=[DataRequired()])
	slotLength =  IntegerField('Slot availability length', validators=)
	taskDue = DateField('Task Due', format="%Y-%m-%d")
	# choices = [ ("To do", "todo"), ("Doing", "doing"), ("Done!", "done")]
	# choices = ["To do", "Doing", "Done"]
	# taskStatus = SelectField('Task Status', validators=[DataRequired()], choices=choices )
	# taskStatus = SelectField('Task Status', validators=[DataRequired()], choices=[ "To do", "Doing", "Done!"] )
	taskPriority = RadioField(u'Task Priority', validators=[DataRequired()], choices=[ ("normal", u"Normal"), ("high", u"High"), ("urgent", u"Urgent") ], default="normal")

	delete = SubmitField(label="Delete", render_kw={'formnovalidate': True})
	submit = SubmitField(label='Create New Task')






class Alert(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    alertTitle = db.Column(db.String(180), nullable=False)
    alertDescription = db.Column(db.Text, nullable=False)
    slotStartDateTime = db.Column(db.DateTime, nullable=False)      # Set upon instantiation
    slotLength = db.Column(db.Integer, nullable=False)

    alertStatus = db.Column(db.String, nullable=True, default='pending')       # Pending, Sent, Archived
    alertSentOn = db.Column(db.DateTime)                                        # Default is empty, filled only when alert is sent
    # alertRecipientID = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False) 
    # ownerID = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)       # Attached to employee instead of main user 

    def __repr__(self):
        return f"Alerts('{self.alertTitle}', '{self.alertDescription}', '{self.slotStartDateTime}','{self.slotStartLength}','{self.alertStatus}')"

