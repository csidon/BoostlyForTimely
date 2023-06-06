# Contains all the routes specific to alerts - waitlistAlert
#****** To change task to createUpdateTask


from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, jsonify
from boostly import db
from boostly.alerts.forms import WaitAlertForm
from boostly.models import User, TempWaitAlert
from flask_login import current_user, login_required
from werkzeug.datastructures import ImmutableMultiDict  # To allow data input to request.form
from datetime import datetime


alerts = Blueprint('alerts', __name__)




@alerts.route("/waitalert/<int:id>", methods=['GET','POST'])
# @login_required             # Needed for routes that can only be accessed after login
def newWaitAlert(id):
    # alert = TempWaitAlert.query.get_or_404(id)
    # if alert.staff != current_user:                               # ** ENABLE LATER
    #     abort(403)
    form = WaitAlertForm()
    context = dict()

    #--- HARDCODED DATA TO BEGIN
    context['alertSubject'] =  'A new slot has opened up!'
    # 'alertReceiver' : 
    context['alertBody1'] = 'Hi '                                                       #[clientName]
    context['alertBody2'] = ',  I’m contacting everyone on my waitlist as a '           #slotLength
    context['alertBody3'] = 'min massage appointment is now available on '              #slotDay + slotDate
    context['alertBody4'] = ' starting at '                                             #slotTime   
    context['alertBody5'] = ' \nIf you would like to book in please do so on this link' #[staffs booking link].
    context['alertBody6'] = '. Look forward to seeing you, '                            #[Staff name]

    context['clientName'] = '[BobTheClient]'
    # context['slotLength'] = '[TempWaitAlert.slotLength]'
    # context['slotDay'] = 'TempWaitAlert.slotDay + conversion'
    # context['slotDate'] = 'TempWaitAlert.slotDateTime + conversion'
    # context['slotDay'] = 'TempWaitAlert.slotDateTime + conversion'
    # context['slotTime'] = 'TempWaitAlert.slotDateTime + conversion'
    context['staffName'] = '[staff.prefName]'
    context['bookingURL'] = '[staff.bookURL]'
    #--- END OF HARDCODED DATA

    if form.validate_on_submit():
        # Send all the form data to EmailAlert.py, which will then do the following FOR EACH CLIENT
        # slotDateTime = ""           # ** get the date and time, format string, then convert to datetime object **
        # alert = TempWaitAlert(
        #     slotStartDateTime=slotDateTime, 
        #     slotLength=form.slotLength.data, 
        #     msgTmpl = 1,            # Use the default message template always for now 
        #     staff=  # lookup staffID based on alertID, 
        #     client=client       # Referencing client of clients
        #     )
        # # Send alert, get send status, then update to TempWaitAlert table
        # db.session.add(alert)
        # db.session.commit()
        # # When all of the clients in the waitlist have been committed to database
        # # In theory, here we should have a success/failure flag system that would check send status and report back to client. That's for v2
        flash('Your waitlist notification alert is being sent!', 'success')
        return redirect(url_for('main.dashboard'))

    elif request.method == 'GET':
        # Get data from the database to display on createAlert.html
        # # Get the datetime from the database and split it up to day, date, and time
        # slotDay = TempWaitAlert.slotStartDateTime
        # slotDate = TempWaitAlert.slotStartDateTime
        # slotTime = TempWaitAlert.slotStartDateTime
        # form.slotStartDate.data = slotDate
        # form.slotStartTime.data = slotTime
        # form.slotLength.data = alert.slotLength

        #--- HARDCODED DATA TO START
        dummySlotStartDateTime = "2023-05-16 20:15:00"      # Check to see if db returns string or datetime obj, but i suspect string
        dummySlotEndDT = "2023-05-16 22:45:00"
        # To calculate slot length, convert start and end time to datetime < -- try doing this early on instead of at this stage
        t1 = datetime.strptime(dummySlotStartDateTime, "%Y-%m-%d %H:%M:%S")
        print('Start time:', t1.time())
        t2 = datetime.strptime(dummySlotEndDT, "%Y-%m-%d %H:%M:%S")
        print('End time:', t2.time())
        deltaMins = (t2-t1).total_seconds()/60
        deltaMinsnInt = "{:.0f}".format(deltaMins)
        print("Time difference is {:.0f}".format(deltaMins) + " minutes")

        context['slotDay'] = t1.strftime("%A")
        context['slotDate'] = t1.strftime("%d %b %Y")
        context['slotTime'] = t1.strftime("%H:%M")
        context['slotLength'] = deltaMinsnInt

        form.slotStartDate.data = t1
        form.slotStartTime.data = t1
        form.slotLength.data = deltaMinsnInt



    # context['doing'] = Task.query.filter(Task.userID==current_user.id,Task.taskStatus=="doing").count()
    # context['done'] = Task.query.filter(Task.userID==current_user.id,Task.taskStatus=="done").count()


    return render_template('createAlert.html', title='Send a new waitlist notification', form=form, context=context, legend="New Waitlist Alert")

