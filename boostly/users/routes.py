# Contains all the routes specific to users - register, login, logout, account

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from boostly import db, bcrypt
from boostly.utils import cleanup
from boostly.models import User, Company
from boostly.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from boostly.users.utils import saveImage


users = Blueprint('users', __name__)

@users.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
        # First create a new company
            company = Company(company_name=form.companyName.data)
            db.session.add(company)        # Adds company to db
            db.session.commit()         # Commits company to db
            db.session.refresh(company)     # Allows me to get the companyID
            companyid = company.id        # can i successfully get the id?
            print("The Companys id retrieved is : " + str(companyid))

            # Using Bcrypt to hash the password so that we don't store passwords in plain text
            hashedPW = bcrypt.generate_password_hash(form.userPassword.data).decode('utf-8')
            # Create an object user with the data collected from the form, passing in the hashed password (instead of cleartext)
            user = User(user_email=form.userEmail.data, timely_booking_url=form.timelyBookingURL.data, user_last_name=form.userLastName.data, user_first_name=form.userFirstName.data, user_password=hashedPW, companyid=companyid)
            user = User(user_email=form.userEmail.data, user_last_name=form.userLastName.data,  timely_booking_url=form.timelyBookingURL.data, user_first_name=form.userFirstName.data, user_password=hashedPW, companyid=companyid)
            db.session.add(user)        # Adds user to db
            db.session.commit()         # Commits user to db                   
            flash('Your account has been created. Please log into your account', 'success')
            return redirect(url_for('users.login'))
        except Exception as err:
            raise err
        finally:
            cleanup(db.session)

    errors = [{'field': key, 'messages': form.errors[key]} for key in form.errors.keys()] if form.errors else []
    return render_template('register.html', title='Sign up for your Boostly Account!', form=form, errors=errors)

@users.route("/login", methods=['GET','POST'])
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.userEmail.data).first()
        print("You have filtered data from your db, user = " + str(user))
        # Decrypt the password hash and check it against the users' password in the database
        # If they match, log the user in and remember their "remember me " choice
        if user and bcrypt.check_password_hash(user.user_password, form.userPassword.data):
            login_user(user, remember=form.userRemember.data)
            # If the user has been trying to access a specific page before logging in, redirect them to that page. Otherwise redirect them to home
            nextPage = request.args.get('next')
            return redirect(nextPage) if nextPage else redirect(url_for('main.dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
            return render_template('login.html', title='Log into your Boostly Account!', form=form)
    return render_template('login.html', title='Log into your Boostly Account!', form=form)


@users.route("/logout")
def logout():
    # Uses flask-login's logout_user function
    logout_user()
    return redirect(url_for('main.home')) 

@users.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    coyID = current_user.companyid
    print("The coyID pulled is "+ str(coyID))
    current_company=Company.query.get(coyID)
    print("The current_company pulled is "+ str(current_company))
    if form.validate_on_submit():
        try:

            if form.uploadImage.data:
                # Saving the picture and updating the database with the hex-ed filename
                hexedImage = saveImage(form.uploadImage.data)
                current_user.user_image = hexedImage
                current_user.user_first_name = form.userFirstName.data
                current_user.user_last_name = form.userLastName.data
                current_user.user_email = form.userEmail.data
                current_company.company_name = form.companyName.data
                current_user.timely_booking_url = form.timelyBookingURL.data
                db.session.commit()
                flash('Your account has been updated', 'success')
                return redirect(url_for('users.account'))
        except Exception as err:
            raise err
        finally:
            cleanup(db.session)
        
    elif request.method == 'GET':
        form.companyName.data = current_company.company_name
        form.timelyBookingURL.data = current_user.timely_booking_url
        form.userFirstName.data = current_user.user_first_name
        form.userLastName.data = current_user.user_last_name
        form.userEmail.data = current_user.user_email

    userImage = url_for('static', filename='profilePics/' + current_user.user_image)
    return render_template('account.html', title='Your Boostly User Account', userImage=userImage, form=form)

