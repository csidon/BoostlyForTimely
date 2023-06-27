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
			first_name=form.firstName.data, 
			last_name=form.lastName.data, 
			email=form.email.data,
			mobile=form.mobile.data,
			status = "active")
		
		db.session.add(client)
		db.session.commit()
		# After creating a client, form the relationship with the client to the company
		client.companies.append(current_company)
		db.session.commit()

		db.session.refresh(client)                                           
		client_id = client.id        # can i successfully get the id?
		print("The Client's id retrieved is : " + str(client_id))
		# Create a blank client preference
		clientpref = ClientPref(min_duration=0, client_id=client_id)
		db.session.add(clientpref)
		db.session.commit()
		print("A blank client pref has been created and attached to this client")
		flash("You have created a new client! Now let's set their preferences", 'success')
		return redirect(url_for('clients.updateClientPref', client_id=client_id))
	btnCreateUpdate = "Create"
	return render_template('createClient.html', title='Create a New Client', form=form, legend="Create a New Client", btnCreateUpdate=btnCreateUpdate)



@clients.route("/client/<int:client_id>/update", methods=['GET','POST'])
@login_required 
def updateClient(client_id):
	client = Client.query.get_or_404(client_id)
	# current_company=Company.query.get(current_user.companyid)
	# Checks to make sure that the client_id belongs to the logged in user's company
	clients_with_company=Client.query.join(ClientCompany).join(Company).filter(Company.id==current_user.companyid).all()
	if client not in clients_with_company:
		abort(403)

	form = ClientForm()
	if form.validate_on_submit():
		client.first_name = form.firstName.data
		client.last_name = form.lastName.data
		client.email = form.email.data
		client.mobile = form.mobile.data
		client.status = "active"
		db.session.commit()
		flash("Your client's details have been updated", 'success')
		return redirect(url_for('clients.displayClients', client_id=client.id))

	elif request.method == 'GET':
		form.firstName.data = client.first_name
		form.lastName.data = client.last_name
		form.email.data = client.email
		form.mobile.data = client.mobile
	btnCreateUpdate = "Update"
	return render_template('createClient.html', title='Update Client Details', form=form, client=client, legend="Update Client Details", btnCreateUpdate=btnCreateUpdate)


@clients.route("/client/<int:client_id>/delete", methods=['GET','POST'])
@login_required 
def deleteClient(client_id):
	print("Do got the client_id? " + str(client_id))
	client = Client.query.get_or_404(client_id)

	# Checks to make sure that the client_id belongs to the logged in user's company
	clients_with_company=Client.query.join(ClientCompany).join(Company).filter(Company.id==current_user.companyid).all()
	if client not in clients_with_company:
		abort(403)
	client.status = "archived"
	db.session.commit()
	flash("We've archived your client information. You can still view it in your Recycle Bin for the next 90 days!", 'success')
	return redirect(url_for('main.dashboard'))

###########################################
#### ROUTES TO SET CLIENT PREFERENCES #####

@clients.route("/clientpref/<int:client_id>/update", methods=['GET','POST'])
@login_required             # Needed for routes that can only be accessed after login
def updateClientPref(client_id):
	# Checks to make sure that the client_id belongs to the logged in user's company
	client = Client.query.get_or_404(client_id)
	clients_with_company=Client.query.join(ClientCompany).join(Company).filter(Company.id==current_user.companyid).all()
	if client not in clients_with_company:
		abort(403)

	print("Existing client preferences found for client_id: " + str(client_id))
	clientpref = ClientPref.query.filter(ClientPref.client_id==client_id).first()
	# clientpref = ClientPref.query.filter(ClientPref.client_id==client_id).all()[0]
	form = ClientPrefForm(data={'minDuration':clientpref.min_duration, 'availtimes':clientpref.avtimes})
	print("Let's just check what's in clientpref.avtimes: "+ str(clientpref.avtimes))
	form.availtimes.query = AvailTimes.query.all()
	if form.validate_on_submit():

		clientpref.min_duration = form.minDuration.data,
		# clientpref.availall = int(form.availall.data),
		# print("Min dur is " + str(type(form.minDuration.data)) + " and availaAll is " + str(type(form.availall.data)))
		db.session.commit()
		# if int(form.availall.data)==0:
		clientpref.avtimes.clear()
		clientpref.avtimes.extend(form.availtimes.data)

		db.session.commit()

		flash("Preferences added!", 'success')
		# Bring the user/staff back to their client overview page

		return redirect(url_for('clients.displayClientPrefs', client_id=client_id))

	client = Client.query.get(client_id)
	clientname = client.first_name + " " + client.last_name
	legend = clientname + "'s Preferences"
	
	return render_template('createClientPref.html', title='Client Preferences', form=form, legend=legend, client_id=client_id)


# To create route for updating client preferences

# @clients.route("/client/<int:client_id>/pref", methods=['GET','POST'])
# @login_required             # Needed for routes that can only be accessed after login
# def updateClientPref(client_id):
# 	client = Client.query.get_or_404(client_id)
# 	cpref = ClientPref.query.get(client_id)
# 	# cpref = ClientPref.query.first()
# 	print("What is my cpref? " + str(cpref))
	
# 	# form = ClientPrefForm()
# 	form = ClientPrefForm(data={'availtimes': cpref.avtimes, 'minDuration':cpref.min_duration})		# Only for updating client prefs
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
# 			cpref.min_duration = form.minDuration.data
# 			db.session.commit()
# 		else:
# 			cpref.avtimes.clear()
# 			cpref.avtimes.extend(form.availtimes.data)
# 			cpref.min_duration = form.minDuration.data
# 			db.session.commit()
# 	# elif request.method == 'GET':
# 		# form = ClientPrefForm(data={'avtimes': cpref.avtimes})		# Only for updating client prefs


# 	clientname = client.first_name + " " + client.last_name
# 	legend = clientname + "'s Preferences"
	
# 	return render_template('createClientPref.html', title='Client Preferences', form=form, legend=legend)




@clients.route("/clients/overview", methods=['GET','POST'])
@login_required             # Needed for routes that can only be accessed after login
def displayClients():
	curr_companyid = current_user.companyid
	print("The current company is " + str(curr_companyid))
	clients = Client.query.join(ClientCompany).join(Company).filter(Company.id==curr_companyid, Client.status == 'active').all()
	print("The clients are: " + str(clients))

	return render_template('allClients.html', title='Client Overview', clients=clients, legend="Client Overview")


@clients.route("/clients/pref/overview", methods=['GET','POST'])
@login_required             # Needed for routes that can only be accessed after login
def displayClientPrefs():
	curr_companyid = current_user.companyid
	print("The current company is " + str(curr_companyid))

	clients = Client.query.join(ClientCompany).join(Company).filter(Company.id==curr_companyid, Client.status == 'active').all()
	print("The clients are: " + str(clients))

	MonDic={}
	TueDic={}
	WedDic={}
	ThurDic={}
	FriDic={}
	SatDic={}
	SunDic={}
	clientIDlist=[]
	availabilities = ""
	
	for client in clients:

		# clientpref = ClientPref.query.filter(ClientPref.client_id==client.id)		# ALso include company ID .filter companyID
		print(str(ClientPref.avtimes))
		availabilities = AvailTimes.query.join(PrefTimes).join(ClientPref).filter(ClientPref.client_id==client.id).all()
		# availabilities = preftimes.query.filter()
		print("The availabilities are " + str(availabilities) + " with length " + str(len(availabilities)))
		MonDic[client] = "⚫" if len(list(filter(lambda i : i.time_unit=='Monday',availabilities))) >0 else "⚪"
		TueDic[client] = "⚫" if len(list(filter(lambda i : i.time_unit=='Tuesday',availabilities))) >0 else "⚪"
		WedDic[client] = "⚫" if len(list(filter(lambda i : i.time_unit=='Wednesday',availabilities))) >0 else "⚪"
		ThurDic[client] = "⚫" if len(list(filter(lambda i : i.time_unit=='Thursday',availabilities))) >0 else "⚪"
		FriDic[client] = "⚫" if len(list(filter(lambda i : i.time_unit=='Friday',availabilities))) >0 else "⚪"
		SatDic[client] = "⚫" if len(list(filter(lambda i : i.time_unit=='Saturday',availabilities))) >0 else "⚪"
		SunDic[client] = "⚫" if len(list(filter(lambda i : i.time_unit=='Sunday',availabilities))) >0 else "⚪"
		print("client_id is " + str(client.id))
		clientIDlist.append(client.id)
		# clientIDdic[client] += client.id 
		print(str(clientIDlist))


	return render_template('allClientPrefs.html', title='Client Preferences Overview', availabilities=availabilities, \
			Mon=MonDic, Tue=TueDic, Wed=WedDic, Thur=ThurDic, Fri=FriDic, Sat=SatDic, Sun=SunDic,\
			 clients=clients, legend="Client Preferences Overview", clientidlist=clientIDlist)


