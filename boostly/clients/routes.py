# Contains all the routes specific to clients and client preferences
#****** To change task to createUpdateTask


from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, jsonify
from boostly import db
from boostly.models import User, TempWaitAlert, Client, ClientPref, AvailTimes, PrefTimes, Company, ClientCompany
from boostly.clients.forms import ClientForm, ClientPrefForm
from flask_login import current_user, login_required
from werkzeug.datastructures import ImmutableMultiDict  # To allow data input to request.form
from datetime import datetime



clients = Blueprint('clients', __name__)


@clients.route("/client/new", methods=['GET','POST'])
@login_required             # Needed for routes that can only be accessed after login
def newClient():
	form = ClientForm()
	current_company=Company.query.get(current_user.companyid)			# Each new client must be registered to the right company
	if form.validate_on_submit():
		client = Client(
			firstName=form.firstName.data, 
			lastName=form.lastName.data, 
			email=form.email.data,
			mobile=form.mobile.data,
			status = "active")
		
		db.session.add(client)
		db.session.commit()
		# After creating a client, form the relationship with the client to the company
		client.companies.append(current_company)
		db.session.commit()

		db.session.refresh(client)                                           
		clientID = client.id        # can i successfully get the id?
		print("The Client's id retrieved is : " + str(clientID))
		# Create a blank client preference
		clientpref = ClientPref(minDuration=0, clientid=clientID)
		db.session.add(clientpref)
		db.session.commit()
		print("A blank client pref has been created and attached to this client")
		flash("You have created a new client! Now let's set their preferences", 'success')
		return redirect(url_for('clients.updateClientPref', clientID=clientID))
	btnCreateUpdate = "Create"
	return render_template('createClient.html', title='Create a New Client', form=form, legend="Create a New Client", btnCreateUpdate=btnCreateUpdate)



@clients.route("/client/<int:clientID>/update", methods=['GET','POST'])
@login_required 
def updateClient(clientID):
	client = Client.query.get_or_404(clientID)
	# current_company=Company.query.get(current_user.companyid)
	# Checks to make sure that the clientID belongs to the logged in user's company
	clients_with_company=Client.query.join(ClientCompany).join(Company).filter(Company.id==current_user.companyid).all()
	if client not in clients_with_company:
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
		return redirect(url_for('clients.updateClient', clientID=client.id))

	elif request.method == 'GET':
		form.firstName.data = client.firstName
		form.lastName.data = client.lastName
		form.email.data = client.email
		form.mobile.data = client.mobile
	btnCreateUpdate = "Update"
	return render_template('createClient.html', title='Update Client Details', form=form, client=client, legend="Update Client Details", btnCreateUpdate=btnCreateUpdate)


@clients.route("/client/<int:clientID>/delete", methods=['GET','POST'])
@login_required 
def deleteClient(clientID):
	print("Do got the clientID? " + str(clientID))
	client = Client.query.get_or_404(clientID)

	# Checks to make sure that the clientID belongs to the logged in user's company
	clients_with_company=Client.query.join(ClientCompany).join(Company).filter(Company.id==current_user.companyid).all()
	if client not in clients_with_company:
		abort(403)
	client.status = "archived"
	db.session.commit()
	flash("We've archived your client information. You can still view it in your Recycle Bin for the next 90 days!", 'success')
	return redirect(url_for('main.dashboard'))

###########################################
#### ROUTES TO SET CLIENT PREFERENCES #####

@clients.route("/clientpref/<int:clientID>/update", methods=['GET','POST'])
@login_required             # Needed for routes that can only be accessed after login
def updateClientPref(clientID):
	# Checks to make sure that the clientID belongs to the logged in user's company
	client = Client.query.get_or_404(clientID)
	clients_with_company=Client.query.join(ClientCompany).join(Company).filter(Company.id==current_user.companyid).all()
	if client not in clients_with_company:
		abort(403)

	print("Existing client preferences found for clientID: " + str(clientID))
	clientpref = ClientPref.query.filter(ClientPref.clientid==clientID).first()
	# clientpref = ClientPref.query.filter(ClientPref.clientid==clientID).all()[0]
	form = ClientPrefForm(data={'minDuration':clientpref.minDuration, 'availtimes':clientpref.avtimes})
	print("Let's just check what's in clientpref.avtimes: "+ str(clientpref.avtimes))
	form.availtimes.query = AvailTimes.query.all()
	if form.validate_on_submit():

		clientpref.minDuration = form.minDuration.data,
		# clientpref.availall = int(form.availall.data),
		# print("Min dur is " + str(type(form.minDuration.data)) + " and availaAll is " + str(type(form.availall.data)))
		db.session.commit()
		# if int(form.availall.data)==0:
		clientpref.avtimes.clear()
		clientpref.avtimes.extend(form.availtimes.data)

		db.session.commit()

		flash("Preferences added!", 'success')
		# Bring the user/staff back to their client overview page

		return redirect(url_for('clients.displayClients', clientID=clientID))

	client = Client.query.get(clientID)
	clientname = client.firstName + " " + client.lastName
	legend = clientname + "'s Preferences"
	
	return render_template('createClientPref.html', title='Client Preferences', form=form, legend=legend)


# To create route for updating client preferences

# @clients.route("/client/<int:clientID>/pref", methods=['GET','POST'])
# @login_required             # Needed for routes that can only be accessed after login
# def updateClientPref(clientID):
# 	client = Client.query.get_or_404(clientID)
# 	cpref = ClientPref.query.get(clientID)
# 	# cpref = ClientPref.query.first()
# 	print("What is my cpref? " + str(cpref))
	
# 	# form = ClientPrefForm()
# 	form = ClientPrefForm(data={'availtimes': cpref.avtimes, 'minDuration':cpref.minDuration})		# Only for updating client prefs
# 	form.availtimes.query = AvailTimes.query.all()
# 	if form.validate_on_submit():
# 		cpref = ClientPref.query.first()
# 		print("What is my cpref? " + str(cpref))
		
# 		if form.availall.data:
# 			print("Yes, notify for all days")
# 			selectall = AvailTimes.query.all()
# 			print("What is selall" + str(selectall) + " and datatype " + str(type(selectall)))
# 			cpref.availall
# 			cpref.avtimes.clear()
# 			cpref.avtimes.extend(selectall)
# 			cpref.minDuration = form.minDuration.data
# 			db.session.commit()
# 		else:
# 			cpref.avtimes.clear()
# 			cpref.avtimes.extend(form.availtimes.data)
# 			cpref.minDuration = form.minDuration.data
# 			db.session.commit()
# 	# elif request.method == 'GET':
# 		# form = ClientPrefForm(data={'avtimes': cpref.avtimes})		# Only for updating client prefs


# 	clientname = client.firstName + " " + client.lastName
# 	legend = clientname + "'s Preferences"
	
# 	return render_template('createClientPref.html', title='Client Preferences', form=form, legend=legend)




@clients.route("/clients/overview", methods=['GET','POST'])
@login_required             # Needed for routes that can only be accessed after login
def displayClients():
	
	curr_companyid = current_user.companyid
	print("The current company is " + str(curr_companyid))
	clients = Client.query.join(ClientCompany).join(Company).filter(Company.id==curr_companyid).all()
	print("The clients are: " + str(clients))

	return render_template('allClients.html', title='Client Overview', clients=clients, legend="Client Overview")


@clients.route("/clients/pref/overview", methods=['GET','POST'])
@login_required             # Needed for routes that can only be accessed after login
def displayClientPrefs():
	curr_companyid = current_user.companyid
	print("The current company is " + str(curr_companyid))

	clients = Client.query.join(ClientCompany).join(Company).filter(Company.id==curr_companyid).all()
	print("The clients are: " + str(clients))

	MonDic={}
	TueDic={}
	WedDic={}
	ThurDic={}
	FriDic={}
	SatDic={}
	SunDic={}
	clientIDlist=[]
	
	for client in clients:

		# clientpref = ClientPref.query.filter(ClientPref.clientid==client.id)		# ALso include company ID .filter companyID
		print(str(ClientPref.avtimes))
		availabilities = AvailTimes.query.join(PrefTimes).join(ClientPref).filter(ClientPref.clientid==client.id).all()

		# availabilities = preftimes.query.filter()
		print("The availabilities are " + str(availabilities) + " with length " + str(len(availabilities)))
		MonDic[client] = 1 if len(list(filter(lambda i : i.timeUnit=='Monday',availabilities))) >0 else 0
		TueDic[client] = 1 if len(list(filter(lambda i : i.timeUnit=='Tuesday',availabilities))) >0 else 0
		WedDic[client] = 1 if len(list(filter(lambda i : i.timeUnit=='Wednesday',availabilities))) >0 else 0
		ThurDic[client] = 1 if len(list(filter(lambda i : i.timeUnit=='Thursday',availabilities))) >0 else 0
		FriDic[client] = 1 if len(list(filter(lambda i : i.timeUnit=='Friday',availabilities))) >0 else 0
		SatDic[client] = 1 if len(list(filter(lambda i : i.timeUnit=='Saturday',availabilities))) >0 else 0
		SunDic[client] = 1 if len(list(filter(lambda i : i.timeUnit=='Sunday',availabilities))) >0 else 0
		print("clientid is " + str(client.id))
		clientIDlist.append(client.id)
		# clientIDdic[client] += client.id 
		print(str(clientIDlist))


	return render_template('allClientPrefs.html', title='Client Preferences Overview', availabilities=availabilities, \
			Mon=MonDic, Tue=TueDic, Wed=WedDic, Thur=ThurDic, Fri=FriDic, Sat=SatDic, Sun=SunDic,\
			 clients=clients, legend="Client Preferences Overview", clientidlist=clientIDlist)


