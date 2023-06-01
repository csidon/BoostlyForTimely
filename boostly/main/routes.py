# Contains all the routes specific to main routes - home(not logged in), dashboard(logged in)

from flask import render_template, url_for, flash, Blueprint
from boostly.models import User
from boostly.users.forms import LoginForm
from flask_login import current_user, login_required
from datetime import datetime




main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    # tasks = Task.query.all()
    users = User.query.all()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(userEmail=form.userEmail.data).first()
        # Decrypt the password hash and check it against the users' password in the database
        # If they match, log the user in and remember their "remember me " choice
        if user and bcrypt.check_password_hash(user.userPassword, form.userPassword.data):
            login_user(user, remember=form.userRemember.data)
            # If the user has been trying to access a specific page before logging in, redirect them to that page. Otherwise redirect them to home
            nextPage = request.args.get('next')
            return redirect(nextPage) if nextPage else redirect(url_for('main.dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('home.html', users=users, form=form)

@main.route("/dashboard")
@login_required             # Needed for routes that can only be accessed after login
def dashboard():
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

@main.route("/test")
def test():
    return 'test'