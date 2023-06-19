# Contains all the routes specific to alerts - waitlistAlert
#****** To change task to createUpdateTask


from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, jsonify
from flask_cors import CORS
from boostly import db
from boostly.alerts.forms import WaitAlertForm, SelectAlerteesForm
from boostly.alerts.emailAlert import sendEmail
from boostly.models import User, TempWaitAlert, MsgTmpl, AvailTimes, PrefTimes, ClientPref, Client, ClientCompany, Company
from flask_login import current_user, login_required
from werkzeug.datastructures import ImmutableMultiDict  # To allow data input to request.form
from datetime import datetime


alerts = Blueprint('alerts', __name__)
# CORS(alerts)




@alerts.route("/waitalert/<int:tempalertid>/<string:owneremail>", methods=['GET','POST'])
# @login_required             # Needed for routes that can only be accessed after login
def newWaitAlert(tempalertid, owneremail):
	
	# if owneremail != current_user.userEmail:                               # ** Put in if id=0 and string="" conditions, then ENABLE LATER
	#     abort(403)
	# If check is successful, then the alert belongs to current_user

	form = WaitAlertForm()
	print(" What does current_user get...?" + str(current_user) + " with datatype: " + str(type(current_user)))
	# getcurrentuser = User.query.get(current_user)
	# The form displays the message template information interspersed with dynamic notification information
	msg = MsgTmpl.query.get(1)
	print("Message retrieved: " + str(msg))

	context = dict()
	alert=TempWaitAlert()
	if tempalertid==0 and owneremail=="new":
		alert = TempWaitAlert(slotLength=0, slotStartDateTime=datetime.now())
	else:
		alert = TempWaitAlert.query.get_or_404(tempalertid)

	context['alertSubject1'] =  msg.subj1
	context['companyName'] =  current_user.coyowner.companyName
	context['alertSubject2'] =  msg.subj2
	context['alertBody1'] = msg.part1                                                   # Hi + [clientName]
	context['alertBody2'] = msg.part2                                                   # I’m contacting everyone on my waitlist as a
	context['slotLength'] = alert.slotLength                                            #slotLength
	context['alertBody3'] = msg.part3                                                   # min 
	context['bizType'] = ""                                                             #massage  
	context['slotDay'] = alert.slotStartDateTime.strftime("%w")                         # appointment is now available on
	context['slotDate'] = datetime.strptime(str(alert.slotStartDateTime.strftime("%d/%m/%y")),("%d/%m/%y"))
	context['alertBody4'] = msg.part4                                                   # starting at 
	context['slotStartTime'] = alert.slotStartDateTime.strftime("%H:%M")                # 
	context['alertBody5'] = msg.part5                                                   # \nIf you would like to book in please do so on this link
	context['alertBody6'] = msg.part6                                                   # Look forward to seeing you
	context['alertBody7'] = msg.part7
	context['alertBody8'] = msg.part8

	# context['alertBody2'] = ',  I’m contacting everyone on my waitlist as a '           #slotLength
	# context['alertBody3'] = 'min massage appointment is now available on '              #slotDay + slotDate
	# context['alertBody4'] = ' starting at '                                             #slotTime   
	# context['alertBody5'] = ' \nIf you would like to book in please do so on this link' #[staffs booking link].
	# context['alertBody6'] = '. Look forward to seeing you, '                            #[Staff name]

	# 'alertReceiver' : 
	# context['alertBody1'] = 'Hi '                                                       #[clientName]
	# context['alertBody2'] = ',  I’m contacting everyone on my waitlist as a '           #slotLength
	# context['alertBody3'] = 'min massage appointment is now available on '              #slotDay + slotDate
	# context['alertBody4'] = ' starting at '                                             #slotTime   
	# context['alertBody5'] = ' \nIf you would like to book in please do so on this link' #[staffs booking link].
	# context['alertBody6'] = '. Look forward to seeing you, '                            #[Staff name]

	context['clientName'] = '[BobTheClient]'

	context['bookingURL'] = '[staff.bookURL]'

	if form.validate_on_submit():
		# Collect data from form and update TempWaitAlert
		# Combine start date and time to startDateTime
  
		alert.slotStartDateTime = datetime.combine(form.slotStartDate.data, form.slotStartTime.data)
		alert.slotLength = form.slotLength.data
		# Attach current_user.id to userid
		alert.userid = current_user.id
		alert.status = "draft"
		alert.msgTmpl = msg.id
		lastUpdated = datetime.now()

		if tempalertid==0 and owneremail=="new":
			# This will be a new entry, so add to database and get new alertID
			db.session.add(alert)
			db.session.commit()
			db.session.refresh(alert)     # Allows me to get the companyID
			tempalertid = alert.id        # can i successfully get the id?
			print("The Alert id retrieved is : " + str(tempalertid))
		else:
			# Just update the existing alert entry
			db.session.commit()

		flash('Please select the alert recipients', 'success')
		return redirect(url_for('alerts.selectAlertees', tempalertid=tempalertid))

	elif request.method == 'GET':
		dbSlotDT = alert.slotStartDateTime

		context['slotDay'] = dbSlotDT.strftime("%A")
		context['slotDate'] = dbSlotDT.strftime("%d %b %Y")
		context['slotTime'] = dbSlotDT.strftime("%H:%M")
		context['slotLength'] = alert.slotLength

		form.slotStartDate.data = dbSlotDT
		form.slotStartTime.data = dbSlotDT
		form.slotLength.data = alert.slotLength


	return render_template('createAlert.html', title='Send a new waitlist notification', form=form, context=context, legend="New Waitlist Alert", alert=alert)


#########################################################################################################
##  Routes for selecting clients that we want to alert/notify
##----------------------------------------------------------------------------------------------------

# @alerts.route('/save_clients', methods=['POST'])
# def save_clients():
# 	if request.method == 'OPTIONS':
# 		# Handle CORS preflight request
# 		return build_preflight_response()
# 	data = request.json
# 	checked_clients = data['checkedClients']
# 	print("The clients are: " + checked_clients)
# 	# Perform the necessary operations to store the checked clients in the database
# 	# ...
#
# 	# Return a response to the frontend
# 	return jsonify({testing})
# def build_preflight_response():
#     response = make_response()
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#     response.headers.add('Access-Control-Allow-Methods', 'POST')
#     return response
@alerts.route("/waitalert/<int:tempalertid>/alertees", methods=['GET','POST'])
@login_required             # Needed for routes that can only be accessed after login
def selectAlertees(tempalertid):
	alert = TempWaitAlert.query.get_or_404(tempalertid)
	alertDayOfWeek = alert.slotStartDateTime.strftime("%A")  
	# Filter preftimes table to get all clientpref_ids of clients matching those days
	curr_companyid = current_user.companyid
	print("The current company is " + str(curr_companyid))
	clients = Client.query.join(ClientCompany).join(Company).filter(Company.id==curr_companyid)
	print("The clients are: " + str(clients))
	print("alertDayOfWeek is " + str(alertDayOfWeek) + " with type " + str(type(alertDayOfWeek)))

	availhumans = []
	availhumannames = []

	alertid = tempalertid
	#-- Now we present the data in the UI table
	print("The avail human names are: " + str(availhumans))
	form = SelectAlerteesForm()
	context = dict()
	# context['name'] =  msg.subj1
	context['slotAvailDay'] =  alert.slotStartDateTime.strftime("%A")  
	# context['lastAlerted'] =  		# To add last alerted
	# context['alertyesno'] = msg.part1
	if form.validate_on_submit():
		selectedClients = form.selectedClients.data.split(',')
		# We need to process the selected client ids here but for now let's just print it
		companyname =  current_user.coyowner.companyName
		# sendEmail(alertid, companyname, clientid, staffname)
		for client in selectedClients:
			print("Checking that this is a clientid" + str(client) + " with the right datatype " + str(type(client)))
			sendEmail(tempalertid, companyname, int(client), current_user.userFirstName)
		print("The selected clients are" + str(selectedClients))

		return jsonify({'message': 'Selected clients received successfully'})
	# elif:
	# 	return jsonify({'message': 'Form validation failed'})

	elif request.method == 'GET':
		for client in clients:
			inloop = ClientPref.query.join(PrefTimes).join(AvailTimes)\
						.filter(AvailTimes.timeUnit==alertDayOfWeek)\
						.filter(ClientPref.clientid==client.id).all()
			if len(inloop) > 0:
				# availhumans.append(client.id) 
				# availhumannames.append(client.firstName + " " + client.lastName) 
				availhumans.append(client)

			print("Available humans inloop pulled are: " + str(availhumans))


	return render_template('selectAlertees.html', availhumans=availhumans, alertid=alertid, alertDayOfWeek=alertDayOfWeek, clients=clients, title='Select the recipents of the alert', form=form, context=context, legend="Select the recipents of the alert", alert=alert)


# @alerts.route("/waitalert/all", methods=['GET','POST'])
# @login_required             # Needed for routes that can only be accessed after login
# def allAlerts(tempalertid):