from datetime import datetime       # Manages datetime issues
from boostly import db, loginManager
from flask_login import UserMixin

@loginManager.user_loader
def loadUser(userID):
    return User.query.get(int(userID))


# Refer to documentation for more in-depth info about how the classes relate to each other
# All relationship variables are named in lowercase, while class/tableNames and columnNames for other properties are in camelCase


# Associating ids from the Client with the Company
ClientCompany = db.Table('client_company', 
    db.Column('clientID', db.Integer, db.ForeignKey('client.id')), 
    db.Column('companyID', db.Integer, db.ForeignKey('company.id')), 
    )


# The company model isn't really used in the front end for the MVP but is created to form the relationship between the User and Clients. 
# It is the equivalent of your "Company Admin Account"
class Company(db.Model):                                                 
    id = db.Column(db.Integer, primary_key = True)
    companyName = db.Column(db.String(100), nullable=False)
    # Association table allows us to find out which clients belong to this company using Company.clientsof <<backref>>
    userstaff = db.relationship('User', backref='coyowner', lazy=True, uselist=False)  # 1 Company --> * Users (staff)


class User(db.Model, UserMixin):                                                 
    id = db.Column(db.Integer, primary_key = True)
    userFirstName = db.Column(db.String(100), nullable=False)
    userLastName = db.Column(db.String(100), nullable=False)
    userEmail = db.Column(db.String(120), unique=True, nullable=False)
    # A hash will be generated for userImage to be 20 Char, and userPass as 60 Char
    userImage = db.Column(db.String(20), nullable=False, default='default.jpg')
    userPassword = db.Column(db.String(60), nullable=False)
    # Each User can only belong to a Company. So 1 Company --> * Users
    companyid = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)   # Attaches user to company.id

    def __repr__(self):
        return f"User('{self.userEmail}', '{self.userPassword}', '{self.userImage}')"



class Client(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.Integer)
    status = db.Column(db.String(30))
    pswd = db.Column(db.String(60))                                             # For when we want to give clients a way to make their own changes
    companies = db.relationship('Company', secondary=ClientCompany, backref='clientsof')         # Refer to client_company table for client/company relsp
    clientprefs = db.relationship('ClientPref', backref='client', uselist=False)           # Forming a 1 Client --> * ClientPref relationship

    def to_dict(self):
        return {
            'id': self.id,
            'fname': self.firstName,
            'lname': self.lastName,
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
    minDuration = db.Column(db.Integer, nullable=False, default=60)
    lastNotified = db.Column(db.DateTime)
    lastClicked = db.Column(db.DateTime)         # For future if able to build SMTP tracking functionality 
    lastUpdated = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # 1 record will be created for *each* slot that the client is available for
    # So if client available only for MondayAM, TuesAM and WedsAM, then there will be 3x client pref records
    availall = db.Column(db.Integer)        # If client checks availall, then no need to check AvailTimes table
    clientid = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)   # Attaches ClientPref to Client's ID
    
    avtimes = db.relationship("AvailTimes", secondary=PrefTimes, back_populates="clientprefs" ) # * clientprefs --> * AvailTimes
    # prefstaffer = db.relationship('PrefStaff', backref='preferwho', lazy=True)
    


class AvailTimes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    timeUnit = db.Column(db.String(30), nullable=False, unique=True)    # For now, split into Mon-Fri chunks. 
    clientprefs = db.relationship("ClientPref", secondary=PrefTimes, back_populates="avtimes" )
    def __str__(self):
        return self.timeUnit



# REMOVE STAFF PREFERENCE TABLE
# # This table is used to link the client's preference to staff. 
# # For the MVP, this wont be used because there's only one staff per user so the client either signs up or not. 
# # Instead, the staffPreference will default to 0 (no preference)
# class PrefStaff(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     clientprefid = db.Column(db.Integer, db.ForeignKey('client_pref.id'), nullable=False, default=0)      # 0 == no preference
#     staffprefid = db.Column(db.Integer, nullable=False)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    calEventUID = db.Column(db.String(100), nullable=False)
    eventOwner = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    eventStart = db.Column(db.DateTime, nullable=False)
    eventEnd = db.Column(db.DateTime, nullable=False)
    eventUpdated = db.Column(db.DateTime, nullable=False)


# class MsgTmpl(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     subj = db.Column(db.String(120), nullable=False)
#     part1 = db.Column(db.String(120), nullable=False)
#     part2 = db.Column(db.String(120), nullable=False)
#     part3 = db.Column(db.String(120), nullable=False)
#     part4 = db.Column(db.String(120), nullable=False)
#     part5 = db.Column(db.String(120), nullable=False)           # 1 Staff -> * Alerts
#     wAlert = db.relationship('TempWaitAlert', backref='msgtmpl', lazy=True) 

#     def __repr__(self):
#         return f"MsgTmpl('{self.id}', '{self.part1}', '{self.part2}','{self.part3}')"



# This is a table that stores temporary alert data. A cron job can be run daily to remove data that is no longer useful/necessary
class TempWaitAlert(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    slotStartDateTime = db.Column(db.DateTime, nullable=False)
    slotLength = db.Column(db.Integer, nullable=False)
    sendStatus = db.Column(db.String(30))
    sendFlag = db.Column(db.Integer)
    lastUpdated = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # msgTmpl = db.Column(db.Integer, db.ForeignKey('msgtmpl.id'), nullable=False)
    # staffuid = db.Column(db.Integer, nullable=False)
    clientid = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    status = db.Column(db.String(30))

    def __repr__(self):
        return f"TempWaitAlert('{self.id}', '{self.slotStartDateTime}', '{self.slotLength}','{self.sendStatus}')"

# class UserTest(db.Model, UserMixin):                                                # User is also the "BusinessOwner", or the overarching account. 
#     id = db.Column(db.Integer, primary_key = True)
#     userFirstName = db.Column(db.String(100), nullable=False)
#     userLastName = db.Column(db.String(100), nullable=False)
#     userEmail = db.Column(db.String(120), unique=True, nullable=False)
#     # A hash will be generated for userImage to be 20 Char, and userPass as 60 Char
#     userImage = db.Column(db.String(20), nullable=False, default='default.jpg')
#     userPassword = db.Column(db.String(60), nullable=False)
#     staffers2 = db.relationship('StaffTest', backref='userowner2', lazy=True, uselist=False)     # 1 User -> * Staff. Lazy=True db will load data in one go
    

#     def __repr__(self):
#         return f"User('{self.userEmail}', '{self.userPassword}', '{self.userImage}')"


# class StaffTest(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     firstName = db.Column(db.String(100), nullable=False)
#     lastName = db.Column(db.String(100), nullable=False)
#     prefName = db.Column(db.String(100), nullable=False)    # This is what will be used to send out messages
#     email = db.Column(db.String(120), nullable=False)
#     service = db.Column(db.String(50))
#     bookURL = db.Column(db.String(120), nullable=False)
#     userid2 = db.Column(db.Integer, db.ForeignKey('user_test.id'), nullable=False)   # Attaches staff to UserID




### REFACTOR CODE IN THE FUTURE TO MAKE SURE THAT THE MODELS ARE USNG THE LATEST MAPPING SQLALCHEMY RELATIONSHIP!######
# class TestParentUser(db.Model):
#     __tablename__= "tpu_table"
#     id: Mapped[int] = db.mapped_column(primary_key=True)
#     userFirstName: Mapped[string] = db.Column(db.String(100), nullable=False)
#     userLastName = db.Column(db.String(100), nullable=False)
#     userEmail = db.Column(db.String(120), unique=True, nullable=False)
#     # A hash will be generated for userImage to be 20 Char, and userPass as 60 Char
#     userImage = db.Column(db.String(20), nullable=False, default='default.jpg')
#     userPassword = db.Column(db.String(60), nullable=False)
#     staffers2: db.Mapped[List["TestChildStaff"]] = relationship(back_populates="imyourfather")


# class TestChildStaff(db.Model):

#     __tablename__= "tcs_table"
#     id = db.Column(db.Integer, primary_key = True)
#     firstName = db.Column(db.String(100), nullable=False)
#     lastName = db.Column(db.String(100), nullable=False)
#     prefName = db.Column(db.String(100), nullable=False)    # This is what will be used to send out messages
#     email = db.Column(db.String(120), nullable=False)
#     service = db.Column(db.String(50))
#     bookURL = db.Column(db.String(120), nullable=False)
#     testuserid = Mapped[int] = mapped_column(ForeignKey("tpu_table.id")) 

#     db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)   # Attaches staff to UserID
#     clients = db.relationship('Client', backref='staffowner', lazy=True)         # 1 Staff -> * Clients