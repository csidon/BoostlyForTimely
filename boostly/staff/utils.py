# Contains utility functions that are used by the routes in this package
import os
import secrets              # Package that generates a random hex value
from PIL import Image       # Pillow package that helps to resize image
from flask import flash  # Not needed here but commonly used, clean up if not used on submission!
from boostly import application, db
from boostly.models import Staff



# This function creates a record in the Staff db. Used in users /register route 
def replicateUser(user, uid):
    staff = Staff(firstName=user.userFirstName, lastName=user.userLastName, prefName=user.userFirstName, email=user.userEmail, service="",
        bookURL="", userid=uid)
    db.session.add(staff)        # Adds user to db
    db.session.commit()         # Commits user to db
    flash('Note: Your staff account has been created as well.', 'success')
    db.session.refresh(staff)                                           
    staffID = staff.id 
    print("Your staff id is: " + str(staffID))
    
    return staffID



