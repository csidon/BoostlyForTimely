# Creating HTML forms with classes from flask_wtf

from flask_wtf import FlaskForm				# Provides form validation functionality				
from wtforms import StringField, SubmitField, TextAreaField, SelectField, RadioField, DateField, SelectMultipleField, TimeField, IntegerField
from wtforms.validators import DataRequired


# class WaitAlertForm(FlaskForm):
# 	# staff = QuerySelectField		# additional functionality to create ability to change
# 	slotStartDate = DateField('Date of available appointment slot', format="%Y-%m-%d")
# 	slotStartTime = TimeField('Appointment Start Time', validators=[DataRequired()])
# 	slotLength =  IntegerField('Slot availability length (in mins)', validators=[DataRequired()])
# 	submit = SubmitField(label='Send Alert')





    # id = db.Column(db.Integer, primary_key = True)
    # slotStartDateTime = db.Column(db.DateTime, nullable=False)
    # slotLength = db.Column(db.Integer, nullable=False)
    # sendStatus = db.Column(db.String(30))
    # sendFlag = db.Column(db.Integer)
    # lastUpdated = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # msgTmpl = db.Column(db.Integer, db.ForeignKey('msgtmpl.id'), nullable=False)
    # staff = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    # client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
