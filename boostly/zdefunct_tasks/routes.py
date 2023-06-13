# Contains all the routes specific to tasks - newTask, task
#****** To change task to createUpdateTask


from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, jsonify
from boostly import db
from boostly.tasks.forms import TaskForm
from boostly.models import User, Task
from flask_login import current_user, login_required
from werkzeug.datastructures import ImmutableMultiDict  # To allow data input to request.form


tasks = Blueprint('tasks', __name__)

@tasks.route("/task/new", methods=['GET','POST'])
@login_required             # Needed for routes that can only be accessed after login
def newTask():
    form = TaskForm()
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
    return render_template('createTask.html', title='New Task', form=form, legend="New Task")



@tasks.route("/task/<int:taskID>/update", methods=['GET','POST'])
@login_required 
def updateTask(taskID):
    task = Task.query.get_or_404(taskID)
    if task.owner != current_user:
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task.taskTitle = form.taskTitle.data
        task.taskDescription = form.taskDescription.data
        task.taskDue = form.taskDue.data
        task.taskStatus = form.taskStatus.data
        db.session.commit()
        flash('Your task has been updated', 'success')
        return redirect(url_for('main.dashboard'))

    elif request.method == 'GET':
        form.taskTitle.data = task.taskTitle
        form.taskDescription.data = task.taskDescription
        form.taskDue.data = task.taskDue
        form.taskStatus.data = task.taskStatus

    return render_template('createTask.html', title='Update Task', form=form, task=task, legend="Update Task")


@tasks.route("/task/<int:taskID>/delete", methods=['POST'])
@login_required 
def deleteTask(taskID):
    task = Task.query.get_or_404(taskID)
    # if task.owner != current_user:
    #     abort(403)
    task.taskStatus = "archived"
    db.session.commit()
    flash("We've archived your task. You can still view it in your Recycle Bin for the next 90 days!", 'success')
    return redirect(url_for('main.dashboard'))

    # return render_template('createTask.html', title='Update Task', form=form, task=task, legend="Update Task")