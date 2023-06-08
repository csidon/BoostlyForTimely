# Contains all the routes specific to staff - account

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from boostly import db, bcrypt
from boostly.models import User
from boostly.staff.forms import UpdateStaffAccountForm
from boostly.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from boostly.users.utils import saveImage                                       # Making use of the users saveImage package


staffers = Blueprint('staffers', __name__)

@staffers.route("/staffaccount", methods=['GET','POST'])
# @login_required
def account():
    form = UpdateStaffAccountForm()
    # Getting the staffer's id based on the logged in 
    print("Can I get the staffers' id? ---> " + str(type(current_user.staffers.id)))
    print("Can I get the staffers' id? ---> " + str(current_user.staffers.id))
    current_staff = current_user.staffers
    if form.validate_on_submit():
        current_staff.firstName = form.firstName.data
        current_staff.lastName = form.lastName.data
        current_staff.prefName = form.prefName.data
        current_staff.email = form.email.data
        current_staff.service = form.service.data
        current_staff.bookURL = form.bookURL.data


        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('staff.staffaccount'))
    elif request.method == 'GET':
        form.firstName.data = current_staff.firstName
        form.lastName.data = current_staff.lastName
        form.prefName.data = current_staff.prefName
        form.email.data = current_staff.email
        form.service.data = current_staff.service
        form.bookURL.data = current_staff.bookURL

    return render_template('staffaccount.html', title='Your Boostly User Account', form=form)


