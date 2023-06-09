# Contains all the routes specific to clients and client preferences
#****** To change task to createUpdateTask


from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, jsonify
from boostly import db
from boostly.models import User, TempWaitAlert, Client, ClientPref, AvailTimes
from boostly.clients.forms import ClientForm, ClientPrefForm
from flask_login import current_user, login_required
from werkzeug.datastructures import ImmutableMultiDict  # To allow data input to request.form
from datetime import datetime


clients = Blueprint('clients', __name__)


@clients.route("/client/new", methods=['GET','POST'])
@login_required             # Needed for routes that can only be accessed after login
def newClient():
	form = ClientForm()
	if form.validate_on_submit():
		client = Client(
			firstName=form.firstName.data, 
			lastName=form.lastName.data, 
			email=form.email.data,
			mobile=form.mobile.data,
			status = "active",
			staffid = current_user.staffers.id)
		db.session.add(client)
		db.session.commit()
		flash("You have created a new client", 'success')
		return redirect(url_for('main.dashboard'))
	btnCreateUpdate = "Create"
	return render_template('createClient.html', title='Create a New Client', form=form, legend="Create a New Client", btnCreateUpdate=btnCreateUpdate)


@clients.route("/client/<int:clientID>/update", methods=['GET','POST'])
@login_required 
def updateClient(clientID):
	client = Client.query.get_or_404(clientID)
	current_staff_clientlist = current_user.staffers.clients
	print("The current_staff_clientlist is: " + str(current_staff_clientlist) + "\n with a datatype of: " + str(type(current_staff_clientlist)))

	# Checking to see if the client belongs to the staff
	not_staffers_client = True
	for client in current_staff_clientlist:
		print("Looping through clients: "+ str(client) + " With clientid of : " + str(client.id))
		if client.id == current_user.staffers.id:
			not_staffers_client = False
	if not_staffers_client:
		abort(403)

	form = ClientForm()
	if form.validate_on_submit():
		client.firstName = form.firstName.data
		client.lastName = form.lastName.data
		client.email = form.email.data
		client.mobile = form.mobile.data
		client.status = "active"
		db.session.commit()
		flash("Your client's details have been updated", 'success')
		return redirect(url_for('client', clientID = current_user.staffers.id))

	elif request.method == 'GET':
		form.firstName.data = client.firstName
		form.lastName.data = client.lastName
		form.email.data = client.email
		form.mobile.data = client.mobile
	btnCreateUpdate = "Update"
	return render_template('createClient.html', title='Update Client Details', form=form, client=client, legend="Update Client Details", btnCreateUpdate=btnCreateUpdate)


@clients.route("/client/<int:clientID>/delete", methods=['POST'])
@login_required 
def deleteClient(clientID):
	client = Client.query.get_or_404(clientID)
	# Checking to see if the client belongs to the staff
	not_staffers_client = True
	for client in current_staff_clientlist:
		if client == current_user.staffers.id:
			not_staffers_client = False
	if not_staffers_client:
		abort(403)
	client.status = "archived"
	db.session.commit()
	flash("We've archived your client information. You can still view it in your Recycle Bin for the next 90 days!", 'success')
	return redirect(url_for('main.dashboard'))


#### ROUTES TO SET CLIENT PREFERENCES #####



@clients.route("/client/pref/<int:clientID>", methods=['GET','POST'])
@login_required             # Needed for routes that can only be accessed after login
def newClientPref(clientID):
	cpref = ClientPref.query.get(clientID)
	# client = Client.query.filter(Client.id==clientID)
	# print("What is my Client? "+ str(client.id))
	form = ClientPrefForm(data={'avtimes': cpref.avtimes})
	form.avtimes.query = AvailTimes.query.all()
	if form.validate_on_submit():
		cpref.avtimes.clear()
		cpref.avtimes.extend(form.avtimes.data)
		db.session.commit()
	relclientid = cpref.clientid
	relclient = Client.query.filter(Client.id==relclientid).first()
	clientname = relclient.firstName + " " + relclient.lastName
	legend = clientname + "'s Preferences"
	print("selecting preferences for " + str(clientname))
	
	return render_template('createClientPref.html', title='Create a New Client', form=form, legend=legend)


# @clients.route("/clientpref/<int:clientID>/update", methods=['GET','POST'])
# @login_required 
# def updateClientPref(clientID):
# 	# Checking that the client exists
# 	client = Client.query.get_or_404(clientID)
# 	# Need to create custom error message.. If clientID not found, prompt create new client
# 	print("Checking what ClientPref.id gets: " + str(ClientPref.id))
# 	cpref = ClientPref.query.filter(ClientPref.id == clientID)
# 	print("Checking what cpref gets: " + str(type(cpref)))
# 	print("so what is cpref.firstName? " + cpref.firstName)
# 	current_staff_clientlist = current_user.staffers.clients


# 	# Checking to see if the client belongs to the staff 
# 	not_staffers_client = True
# 	for client in current_staff_clientlist:
# 		print("Looping through clients: "+ str(client) + " With clientid of : " + str(client.id))
# 		if client.id == current_user.staffers.id:
# 			not_staffers_client = False
# 	if not_staffers_client:
# 		abort(403)

# 	form = ClientPrefForm()
# 	if form.validate_on_submit():
# 		# if form.availall.data == 1:		# Client wants to be notified for all timeslots
# 		cpref.minDuration = form.minDuration.data
# 		cpref.timeavail = 0
# 		# else:
# 		form.timesAvail.data = AvailTimes.query.all()

# 		# client.lastName = form.lastName.data
# 		# client.email = form.email.data
# 		# client.mobile = form.mobile.data
# 		# client.status = "active"
# 		# db.session.commit()
# 		# flash("Your client's details have been updated", 'success')
# 		# return redirect(url_for('client', clientID = current_user.staffers.id))

# 	# elif request.method == 'GET':
# 		# form.firstName.data = client.firstName
# 		# form.lastName.data = client.lastName
# 		# form.email.data = client.email
# 		# form.mobile.data = client.mobile
# 	# btnCreateUpdate = "Update"

# 	legend = "Update " + client.firstName + "'s Preferences"
# 	return render_template('createClientPref.html', title='Update Client Preferences', form=form, client=client, legend=legend)


