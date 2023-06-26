# Creating HTML forms with classes from flask_wtf

from flask_wtf import FlaskForm				# Provides form validation functionality
from flask_wtf.file import FileField, FileAllowed	# Provides ability for the form to manage files/images
from flask_login import current_user				
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from boostly.models import User, Company



class RegistrationForm(FlaskForm):

	companyName = StringField('Company Name', validators=[DataRequired()])	# At this stage there is no company validation check. 
	userFirstName = StringField('First Name', validators=[DataRequired()])
	userLastName = StringField('Last Name', validators=[DataRequired()])
	userEmail = StringField('Email (This will also be your username)', validators=[DataRequired(), Email()])
	userPassword = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
	confirmPassword = PasswordField('Confirm your password', validators=[DataRequired(), EqualTo('userPassword', message='Password must match')])
	timelyBookingURL = StringField('Enter your Timely Booking URL', validators=[DataRequired()])
	submit = SubmitField('Create account')

	def validate_userEmail(self, userEmail):
		user = User.query.filter_by(user_email=userEmail.data).first()
		# If the user query is none, nothing happens. Otherwise if the query returns data, throw validation error message
		if user:
			raise ValidationError("That email already exists. Please register with another email address")


class LoginForm(FlaskForm):
	userEmail = StringField('Email address', validators=[DataRequired(), Email()])
	userPassword = PasswordField('Password', validators=[DataRequired()])

	# Remembers user's information so that they do not need to re-login if they close their browser
	# using a secure cookie
	userRemember = BooleanField('Remember Me')

	submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
	companyName = StringField('Company Name', validators=[DataRequired()])
	userFirstName = StringField('First Name', validators=[DataRequired()])
	userLastName = StringField('Last Name', validators=[DataRequired()])
	userEmail = StringField('Email (This will also be your username)', validators=[DataRequired(), Email()])
	timelyBookingURL = StringField('Enter your Timely Booking URL', validators=[DataRequired()])
	uploadImage = FileField('Update your profile picture', validators=[FileAllowed(['jpg', 'png'])])

	submit = SubmitField('Update')

	def validate_userEmail(self, userEmail):
		if userEmail.data != current_user.user_email:
			user = User.query.filter_by(user_email=userEmail.data).first()
			# If the user query is none, nothing happens. Otherwise if the query returns data, throw validation error message
			if user:
				raise ValidationError("That email already exists. Please register with another email address")