# Creating HTML forms with classes from flask_wtf

from flask_wtf import FlaskForm				# Provides form validation functionality
from flask_wtf.file import FileField, FileAllowed	# Provides ability for the form to manage files/images
from flask_login import current_user				
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from boostly.models import Staff



class UpdateStaffAccountForm(FlaskForm):
	firstName = StringField('First Name', validators=[DataRequired()])
	lastName = StringField('Last Name', validators=[DataRequired()])
	prefName = StringField('Preferred Name (This is the name that will be used to send out your notifications)', validators=[DataRequired()])
	email = StringField('Email (This will also be your username)', validators=[DataRequired(), Email()])
	service = StringField('Services provided')
	bookURL = StringField('Your Timely booking URL', validators=[DataRequired()])

	submit = SubmitField('Update')
