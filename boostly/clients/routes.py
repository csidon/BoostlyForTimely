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
		# Also create a blank preference at the same time, so get the new clientID
		db.session.refresh(client)                                           
		clientID = client.id        # can i successfully get the id?
		print("The Client's id retrieved is : " + str(clientID))
		newpref = ClientPref(minDuration=0, clientid=clientID)
		db.session.add(newpref)
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

@clients.route("/client/<int:clientID>/pref", methods=['GET','POST'])
@login_required             # Needed for routes that can only be accessed after login
def newClientPref(clientID):
	client = Client.query.get_or_404(clientID)
	cpref = ClientPref.query.get(clientID)
	# cpref = ClientPref.query.first()
	print("What is my cpref? " + str(cpref))
	
	# form = ClientPrefForm()
	form = ClientPrefForm(data={'availtimes': cpref.avtimes})		# Only for updating client prefs
	form.availtimes.query = AvailTimes.query.all()
	if form.validate_on_submit():


		cpref = ClientPref.query.first()
		print("What is my cpref? " + str(cpref))
		cpref.avtimes.clear()
		cpref.avtimes.extend(form.availtimes.data)
		db.session.commit()
	# elif request.method == 'GET':
		# form = ClientPrefForm(data={'avtimes': cpref.avtimes})		# Only for updating client prefs


	clientname = client.firstName + " " + client.lastName
	legend = clientname + "'s Preferences"
	
	return render_template('createClientPref.html', title='Client Preferences', form=form, legend=legend)


@clients.route("/<int:staffID>/clients/overview", methods=['GET','POST'])
@login_required             # Needed for routes that can only be accessed after login
def displayClients(staffID):
	clients = Client.query.filter(Client.staffid==staffID)
	# url = "/api/" + str(staffID) + "/clientdata",

	return render_template('allClients.html', title='Client Overview', clients=clients, legend="Client Overview", staffID=staffID)
