# Creating HTML forms with classes from flask_wtf

from flask_wtf import FlaskForm				# Provides form validation functionality				
from wtforms import StringField, SubmitField, TextAreaField, SelectField, RadioField, DateField, SelectMultipleField
from wtforms.validators import DataRequired



class TaskForm(FlaskForm):
	taskTitle = StringField('Title', validators=[DataRequired()])
	taskDescription = TextAreaField('Description', validators=[DataRequired()])
	taskDue = DateField('Task Due', format="%Y-%m-%d")
	# choices = [ ("To do", "todo"), ("Doing", "doing"), ("Done!", "done")]
	# choices = ["To do", "Doing", "Done"]
	# taskStatus = SelectField('Task Status', validators=[DataRequired()], choices=choices )
	# taskStatus = SelectField('Task Status', validators=[DataRequired()], choices=[ "To do", "Doing", "Done!"] )
	taskStatus = RadioField(u'Task Status', validators=[DataRequired()], choices=[ ("todo", u"To do"), ("doing", u"Doing"), ("done", u"Done") ], default="")
	taskPriority = RadioField(u'Task Priority', validators=[DataRequired()], choices=[ ("normal", u"Normal"), ("high", u"High"), ("urgent", u"Urgent") ], default="normal")

	delete = SubmitField(label="Delete", render_kw={'formnovalidate': True})
	submit = SubmitField(label='Create New Task')



