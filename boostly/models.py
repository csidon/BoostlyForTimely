from datetime import datetime       # Manages datetime issues
from boostly import db, loginManager
from flask_login import UserMixin

@loginManager.user_loader
def loadUser(user_id):
    return User.query.get(int(user_id))


# Refer to documentation for more in-depth info about how the classes relate to each other
# All relationship variables are named in lowercase, while class/tableNames and columnNames for other properties are in camelCase


# Associating ids from the Client with the Company
ClientCompany = db.Table('client_company', 
    db.Column('client_id', db.Integer, db.ForeignKey('client.id')), 
    db.Column('company_id', db.Integer, db.ForeignKey('company.id')), 
    )


# The company model isn't really used in the front end for the MVP but is created to form the relationship between the User and Clients. 
# It is the equivalent of your "Company Admin Account"
class Company(db.Model):                                                 
    id = db.Column(db.Integer, primary_key = True)
    company_name = db.Column(db.String(100), nullable=False)
    # Association table allows us to find out which clients belong to this company using Company.clientsof <<backref>>
    userstaff = db.relationship('User', backref='coyowner', lazy=True, uselist=False)  # 1 Company --> * Users (staff)


class User(db.Model, UserMixin):                                                 
    id = db.Column(db.Integer, primary_key = True)
    user_first_name = db.Column(db.String(100), nullable=False)
    user_last_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    timely_booking_url = db.Column(db.String(120), nullable=False, default="remove default!!")
    # A hash will be generated for user_image to be 20 Char, and userPass as 60 Char
    user_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    user_password = db.Column(db.String(60), nullable=False)
    # Each User can only belong to a Company. So 1 Company --> * Users
    companyid = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)   # Attaches user to company.id
    # Linking User with their alerts (1 User --> * Alerts)
    waitalerts = db.relationship('TempWaitAlert', backref='alertbelongsto', lazy=True, uselist=False) 

    def __repr__(self):
        return f"User('{self.user_email}', '{self.user_password}', '{self.user_image}')"



class Client(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.Integer)
    status = db.Column(db.String(30))
    pswd = db.Column(db.String(60))                                             # For when we want to give clients a way to make their own changes
    companies = db.relationship('Company', secondary=ClientCompany, backref='clientsof')         # Refer to client_company table for client/company relsp
    clientprefs = db.relationship('ClientPref', backref='client', uselist=False)           # Forming a 1 Client --> * ClientPref relationship

    def to_dict(self):
        return {
            'id': self.id,
            'fname': self.first_name,
            'lname': self.last_name,
            'email': self.email,
            'mobile': self.mobile,
            'status': self.status
        }

# Association table connecting the ClientPref with AvailTimes 
PrefTimes = db.Table(
    'pref_times', 
    db.Column("clientpref_id", db.ForeignKey('client_pref.id')),
    db.Column("availtimes_id", db.ForeignKey('avail_times.id')),
)


class ClientPref(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    min_duration = db.Column(db.Integer, nullable=False, default=60)
    last_notified = db.Column(db.DateTime)
    last_clicked = db.Column(db.DateTime)         # For future if able to build SMTP tracking functionality 
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # 1 record will be created for *each* slot that the client is available for
    # So if client available only for MondayAM, TuesAM and WedsAM, then there will be 3x client pref records
    # availall = db.Column(db.Integer)        # If client checks availall, then no need to check AvailTimes table
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)   # Attaches ClientPref to Client's ID
    
    avtimes = db.relationship("AvailTimes", secondary=PrefTimes, back_populates="clientprefs" ) # * clientprefs --> * AvailTimes
    # prefstaffer = db.relationship('PrefStaff', backref='preferwho', lazy=True)
    


class AvailTimes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    time_unit = db.Column(db.String(30), nullable=False, unique=True)    # For now, split into Mon-Fri chunks. 
    clientprefs = db.relationship("ClientPref", secondary=PrefTimes, back_populates="avtimes" )
    def __str__(self):
        return self.time_unit




# class Event(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     calEventUID = db.Column(db.String(100), nullable=False)
#     eventOwner = db.Column(db.String(120), nullable=False)
#     status = db.Column(db.String(30), nullable=False)
#     eventStart = db.Column(db.DateTime, nullable=False)
#     eventEnd = db.Column(db.DateTime, nullable=False)
#     eventUpdated = db.Column(db.DateTime, nullable=False)

# Trying to create everything in lowercase since Lambda doesn't seem to accept camelCase
class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    cal_event_uid = db.Column(db.String(100), nullable=False)
    event_owner = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    event_start = db.Column(db.DateTime, nullable=False)
    event_end = db.Column(db.DateTime, nullable=False)
    event_updated = db.Column(db.DateTime, nullable=False)


# The Message template table store default "canned messages" that are used to alert clients, 
# broken down into parts to allow inserting i.e. date/time/username data in between
class MsgTmpl(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subj1 = db.Column(db.String(120))
    subj2 = db.Column(db.String(120))
    part1 = db.Column(db.String(120))
    part2 = db.Column(db.String(120))
    part3 = db.Column(db.String(120))
    part4 = db.Column(db.String(120))
    part5 = db.Column(db.String(120))           
    part6 = db.Column(db.String(120))
    part7 = db.Column(db.String(120))
    part8 = db.Column(db.String(120))
    waitalerts = db.relationship('TempWaitAlert', backref='msgtemplate', lazy=True, uselist=False) 
#     def __repr__(self):
#         return f"MsgTmpl('{self.id}', '{self.part1}', '{self.part2}','{self.part3}')"



# This is a table that stores temporary alert data. A cron job can be run daily to remove data that is no longer useful/necessary
# There are 2 types of alerts --> One registers that a slot is available/created, 
# the other registers that an alert has been sent (and who it's been sent to)
class TempWaitAlert(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    # Alert data
    slot_start_date_time = db.Column(db.DateTime, nullable=False)
    slot_length = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))        # Attached when business owner submits waitAlert form part 1
    msg_tmpl = db.Column(db.Integer, db.ForeignKey('msg_tmpl.id'))    # Attached when business owner submits waitAlert form part 1
    # For cron job to look at to know whether to clear out or not
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.now())
    status = db.Column(db.String(30))

    def __repr__(self):
        return f"TempWaitAlert('{self.id}', '{self.slot_start_date_time}', '{self.slot_length}','{self.sendStatus}')"


# There are 2 types of temp alerts --> One registers that a slot available, 
# the other registers that an alert has been sent (and who it's been sent to)
class SentWaitAlert(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    # Alert data
    slot_start_date_time = db.Column(db.DateTime, nullable=False)
    slot_length = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))        # Attached when business owner submits waitAlert form part 1
    msg_tmpl = db.Column(db.Integer, db.ForeignKey('msg_tmpl.id'))    # Attached when business owner submits waitAlert form part 1

    # Send data
    client_id = db.Column(db.Integer)        # This will be null if not sent, otherwise there will be multiple records for each batch notification, 1 for each alert
    send_alert_id = db.Column(db.Integer)  # This will be null for the parent Alert when sent. If populated, the id should match with the parent AlertID
    send_flag = db.Column(db.Integer)
    # For cron job to look at to know whether to clear out or not
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.now())
    status = db.Column(db.String(30))

    def __repr__(self):
        return f"TempWaitAlert('{self.id}', '{self.slot_start_date_time}', '{self.slot_length}','{self.sendStatus}')"

# class UserTest(db.Model, UserMixin):                                                # User is also the "BusinessOwner", or the overarching account. 
#     id = db.Column(db.Integer, primary_key = True)
#     user_first_name = db.Column(db.String(100), nullable=False)
#     user_last_name = db.Column(db.String(100), nullable=False)
#     user_email = db.Column(db.String(120), unique=True, nullable=False)
#     # A hash will be generated for user_image to be 20 Char, and userPass as 60 Char
#     user_image = db.Column(db.String(20), nullable=False, default='default.jpg')
#     user_password = db.Column(db.String(60), nullable=False)
#     staffers2 = db.relationship('StaffTest', backref='userowner2', lazy=True, uselist=False)     # 1 User -> * Staff. Lazy=True db will load data in one go
    

#     def __repr__(self):
#         return f"User('{self.user_email}', '{self.user_password}', '{self.user_image}')"



