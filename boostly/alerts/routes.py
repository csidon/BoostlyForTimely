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
    alert = TempWaitAlert.query.get_or_404(id)
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
    

        dbSlotDT = alert.slotStartDateTime

        context['slotDay'] = dbSlotDT.strftime("%A")
        context['slotDate'] = dbSlotDT.strftime("%d %b %Y")
        context['slotTime'] = dbSlotDT.strftime("%H:%M")
        context['slotLength'] = alert.slotLength

        form.slotStartDate.data = dbSlotDT
        form.slotStartTime.data = dbSlotDT
        form.slotLength.data = alert.slotLength



    # context['doing'] = Task.query.filter(Task.userID==current_user.id,Task.taskStatus=="doing").count()
    # context['done'] = Task.query.filter(Task.userID==current_user.id,Task.taskStatus=="done").count()


    return render_template('createAlert.html', title='Send a new waitlist notification', form=form, context=context, legend="New Waitlist Alert", alert=alert)

