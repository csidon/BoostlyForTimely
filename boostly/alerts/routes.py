# Contains all the routes specific to alerts - waitlistAlert
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from boostly import db
# from boostly.utils import cleanup     # Learn how sessions work, then enable and insert
from boostly.alerts.forms import WaitAlertForm, SelectAlerteesForm
from boostly.alerts.emailAlert import sendEmail
from boostly.models import TempWaitAlert, SentWaitAlert, MsgTmpl, AvailTimes, PrefTimes, ClientPref, Client, ClientCompany, Company
from flask_login import current_user, login_required
from datetime import datetime


alerts = Blueprint('alerts', __name__)

@alerts.route("/waitalert/<int:tempalertid>/<string:owneremail>", methods=['GET','POST'])
@login_required             # Needed for routes that can only be accessed after login
def newWaitAlert(tempalertid, owneremail):
    print("owneremail is " + owneremail + " and the logged in user is " + current_user.user_email)	# Might need to put userID check in there once it comes to multi-user on one device. But for now this is actually more efficient and secure

    form = WaitAlertForm()
    print(" What does current_user get...?" + str(current_user) + " with datatype: " + str(type(current_user)))
    # The form displays the message template information interspersed with dynamic notification information
    msg = MsgTmpl.query.get(1)
    print("Message retrieved: " + str(msg))

    context = dict()
    alert=TempWaitAlert()
    if tempalertid==0 and owneremail=="new":
        alert = TempWaitAlert(slot_length=0, slot_start_date_time=datetime.now())
    elif owneremail != current_user.user_email:                               # ** Put in if id=0 and string="" conditions, then ENABLE LATER
        abort(403)
    else:
        # If check is successful, then the alert belongs to current_user
        alert = TempWaitAlert.query.get_or_404(tempalertid)

    context['alertSubject1'] =  msg.subj1
    context['companyName'] =  current_user.coyowner.company_name
    context['alertSubject2'] =  msg.subj2
    context['alertBody1'] = msg.part1                                                   # Hi + [clientName]
    context['alertBody2'] = msg.part2                                                   # I’m contacting everyone on my waitlist as a
    context['slotLength'] = alert.slot_length                                            #slotLength
    context['alertBody3'] = msg.part3                                                   # min 
    context['bizType'] = ""                                                             #massage  
    context['slotDay'] = alert.slot_start_date_time.strftime("%w")                         # appointment is now available on
    context['slotDate'] = datetime.strptime(str(alert.slot_start_date_time.strftime("%d/%m/%y")),("%d/%m/%y"))
    context['alertBody4'] = msg.part4                                                   # starting at 
    context['slotStartTime'] = alert.slot_start_date_time.strftime("%H:%M")                # 
    context['alertBody5'] = msg.part5                                                   # \nIf you would like to book in please do so on this link
    context['alertBody6'] = msg.part6                                                   # Look forward to seeing you
    context['alertBody7'] = msg.part7
    context['alertBody8'] = msg.part8

    context['bookingURL'] = '[staff.bookURL]'

    if form.validate_on_submit():

        # Collect data from form and update TempWaitAlert
        # Combine start date and time to startDateTime

        alert.slot_start_date_time = datetime.combine(form.slotStartDate.data, form.slotStartTime.data)
        alert.slot_length = form.slotLength.data
        # Attach current_user.id to user_id
        alert.user_id = current_user.id
        alert.status = "draft"
        alert.msg_tmpl = msg.id
        last_updated = datetime.now()

        if tempalertid==0 and owneremail=="new":
            # This will be a new entry, so add to database and get new alertID
            try:
                db.session.add(alert)
                db.session.commit()
                db.session.refresh(alert)     # Allows me to get the company_id
                tempalertid = alert.id        # can i successfully get the id?
                print("The Alert id retrieved is : " + str(tempalertid))
            except Exception as err:
                raise err

        else:
            try:
                # Just update the existing alert entry
                db.session.commit()
            except Exception as err:
                raise err

        flash('Please select the alert recipients', 'success')
        return redirect(url_for('alerts.selectAlertees', tempalertid=tempalertid))

    elif request.method == 'GET':
        dbSlotDT = alert.slot_start_date_time

        context['slotDay'] = dbSlotDT.strftime("%A")
        context['slotDate'] = dbSlotDT.strftime("%d %b %Y")
        context['slotTime'] = dbSlotDT.strftime("%H:%M")
        context['slotLength'] = alert.slot_length

        form.slotStartDate.data = dbSlotDT
        form.slotStartTime.data = dbSlotDT
        form.slotLength.data = alert.slot_length

    return render_template('createAlert.html', title='Send a new waitlist notification', form=form, context=context, legend="New Waitlist Alert", alert=alert)


#########################################################################################################
##  Routes for selecting clients that we want to alert/notify
##----------------------------------------------------------------------------------------------------

@alerts.route("/waitalert/<int:tempalertid>/alertees", methods=['GET','POST'])
@login_required             # Needed for routes that can only be accessed after login
def selectAlertees(tempalertid):
    alert = TempWaitAlert.query.get_or_404(tempalertid)
    alertDayOfWeek = alert.slot_start_date_time.strftime("%A")  
    # Filter preftimes table to get all clientpref_ids of clients matching those days
    curr_companyid = current_user.companyid
    print("The current  company is " + str(curr_companyid))
    # Querying the database to get the intersection between the Company and the Client using the current_user's company id, then adding status filtering on top of that
    clients = Client.query.join(ClientCompany).join(Company).filter(Company.id==curr_companyid, Client.status == 'active')
    print("The clients are: " + str(clients))
    # print("alertDayOfWeek is " + str(alertDayOfWeek) + " with type " + str(type(alertDayOfWeek)))

    availhumans = []

    alertid = tempalertid
    #-- Now we present the data in the UI table
    form = SelectAlerteesForm()
    context = dict()
    context['slotAvailDay'] =  alert.slot_start_date_time.strftime("%A")  
    # context['lastAlerted'] =  		# To add last alerted
    # context['alertyesno'] = msg.part1
    if form.validate_on_submit():
        try:
            selectedClients = form.selectedClients.data.split(',')
            # We need to process the selected client ids here but for now let's just print it
            company_name =  current_user.coyowner.company_name
            for client in selectedClients:
                # print("Checking that this is a client of:" + str(client) + " with the right datatype " + str(type(client)))
                sendEmail(tempalertid, company_name, int(client), current_user)	# Sends email notification and creates a record in SentWaitAlert db table
            # Update parent alert with status of Sent
            alert.status = "sent"
            db.session.commit()
            print("The selected clients are" + str(selectedClients))

            flash('Notifications sent!', 'success')
            return redirect(url_for('alerts.alertHistory'))
        except Exception as err:
            raise err


    elif request.method == 'GET':
        for client in clients:
            inloop = ClientPref.query.join(PrefTimes).join(AvailTimes)\
                        .filter(AvailTimes.time_unit==alertDayOfWeek)\
                        .filter(ClientPref.client_id==client.id).all()
            if len(inloop) > 0:
                availhumans.append(client)

            print("Available humans inloop pulled are: " + str(availhumans))

    useremail = current_user.user_email
    return render_template('selectAlertees.html', useremail = useremail, availhumans=availhumans, alertid=alertid, alertDayOfWeek=alertDayOfWeek, clients=clients, title='Select the recipents of the alert', form=form, context=context, legend="Select the recipents of the alert", alert=alert)


@alerts.route("/waitalert/history", methods=['GET','POST'])
@login_required             # Needed for routes that can only be accessed after login
def alertHistory():

    curr_companyid = current_user.companyid
    print("The current company is " + str(curr_companyid))

    alerts = SentWaitAlert.query.filter(SentWaitAlert.sent_user_id==current_user.id).order_by(SentWaitAlert.last_updated.desc()).all()
    print("The alerts retrieved are " + str(alerts))

    sentClient = {}
    slotDetails = {}
    slotLength = {}
    alertStatus = {}
    lastUpdated = {}
    for alert in alerts:
        # Have to pull out all this information to be able to query Client db for name
        client = Client.query.get(alert.client_id)
        sentClient[alert] = client.first_name + " " + client.last_name

        slotDetails[alert] = alert.slot_start_date_time.strftime("%A, %d %b %Y")
        slotLength[alert] = str(alert.slot_length)
        alertStatus[alert] = alert.status
        lastUpdated[alert] = str(alert.last_updated)

        print("List of clients sent to: " + str(sentClient[alert]) + " with slot deets: " + str(slotDetails))
        
    return render_template('alertHistory.html', title='Alert History', legend="Alert History", alerts=alerts,\
                    client=sentClient, details=slotDetails, length=slotLength, status=alertStatus, updated=lastUpdated)
