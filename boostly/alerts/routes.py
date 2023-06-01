# Contains all the routes specific to alerts - waitlistAlert
#****** To change task to createUpdateTask


from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, jsonify
from boostly import db
from boostly.alerts.forms import WaitAlertForm
from boostly.models import User, Alert
from flask_login import current_user, login_required
from werkzeug.datastructures import ImmutableMultiDict  # To allow data input to request.form


alerts = Blueprint('alerts', __name__)


# Basic waitalert template
waitAlertContents = [
    {
        'alertSubject' : 'A new slot has opened up!',
        'alertReceiver' : 
        'alertBody' : 'Hi [clientName],  I’m contacting everyone on my waitlist as a [slotLength] massage appointment is now available on' +
                        '[slotDay] and [slotDate] starting at [slotStart]. ' + 
                        '\nIf you would like to book in please do so on this link [bOwns booking link]. Look forward to seeing you, [bOwns name]'
    }

]



# def lambdaData(event):
    
#     # Collect data passed from parent lambda function!
    
#     calID = event['freeCalID']
#     freeOwner = event['freeOwner']
#     freeStatus = event['freeStatus']
#     freeStart = event['freeStart']
#     freeEnd = event['freeEnd']
#     parentSentTimestamp = event['sendingTimestamp']

#     freeDateStart = datetime.strptime(freeStart, '%Y-%m-%d %H:%M:%S' )
#     freeStartTime = freeDateStart.strftime('%H:%M%p')
#     freeStartDay = freeDateStart.strftime('%A')
#     freeStartDate = freeDateStart.strftime('%d %b %Y')
#     print("The freeStatus before condition is: " + freeStatus)
    
#     if freeStatus=="confirmed":
#         freeStatus = "moved"
        
#     print("The freeStatus after condition is: " + freeStatus)
#     fromName = "Boostly Notifications"
#     fromAddress = "no-reply@whitecathearing.com"
    
    
    
#     # # This address must be verified with Amazon SES.
#     SENDER = fromName+ "<" + fromAddress + ">"


# @alerts.route("/waitalert/<int:employeeID>", methods=['GET','POST'])
# @login_required             # Needed for routes that can only be accessed after login
# def newWaitAlert(event):
#     # Get data from lambda function



    form = WaitAlertForm()
    context = dict()
    context['alertSubject'] =  'A new slot has opened up!'
        # 'alertReceiver' : 
    context['alertBody1'] = 'Hi [clientName],  I’m contacting everyone on my waitlist as a '
    context['alertBody2'] = ' massage appointment is now available on '
    context['alertBody3'] = ' starting at '
    context['alertBody4'] = ' \nIf you would like to book in please do so on this link [bOwns booking link]. Look forward to seeing you, '

    if request.method == 'POST':
        selectedStatus = form.taskStatus.data
        task = Task(
            taskTitle=form.taskTitle.data, 
            taskDescription=form.taskDescription.data, 
            userID=current_user.id, owner=current_user, 
            taskDue=form.taskDue.data, 
            taskStatus=selectedStatus,
            taskPriority=form.taskPriority.data
            )
        db.session.add(task)
        db.session.commit()
        flash('New Task Created!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('createAlert.html', title='Send a new waitlist notification', form=form, context=context, legend="New Waitlist Alert")




    # context = dict()
    # dateToday = datetime.today()
    # context['overdue'] = Task.query.filter(Task.userID == current_user.id, Task.taskDue < dateToday, Task.taskStatus != "archived").count()
    # context['overdueTasks'] = Task.query.filter(Task.userID == current_user.id, Task.taskDue < dateToday, Task.taskStatus != "archived").order_by(Task.taskDue)
    # context['tasks'] = Task.query.filter(Task.userID==current_user.id)
    # context['todo'] = Task.query.filter(Task.userID==current_user.id,Task.taskStatus=="todo").count()
    # context['doing'] = Task.query.filter(Task.userID==current_user.id,Task.taskStatus=="doing").count()
    # context['done'] = Task.query.filter(Task.userID==current_user.id,Task.taskStatus=="done").count()
    # context['todoTasks'] = Task.query.filter(Task.userID == current_user.id, Task.taskStatus == "todo").order_by(Task.taskDue)
    # context['doingTasks'] = Task.query.filter(Task.userID == current_user.id, Task.taskStatus == "doing").order_by(Task.taskDue)
    # context['doneTasks'] = Task.query.filter(Task.userID == current_user.id, Task.taskStatus == "done").order_by(Task.taskDue)
    # context['archivedTasks'] = Task.query.filter(Task.userID == current_user.id, Task.taskStatus == "archived").order_by(Task.taskDue)
    return render_template('dashboard.html', title='Your Boostly Stats At A Glance', context=context)


    # 'Hi [clientName],  I’m contacting everyone on my waitlist as a '
    # alertBody2 [slotLength] massage appointment is now available on' +
    #                     '[slotDay] and [slotDate] starting at [slotStart]. ' + 
    #                     '\nIf you would like to book in please do so on this link [bOwns booking link]. Look forward to seeing you, [bOwns name]'