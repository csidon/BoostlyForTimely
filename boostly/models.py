from datetime import datetime       # Manages datetime issues
from boostly import db, loginManager
from flask_login import UserMixin

@loginManager.user_loader
def loadUser(userID):
    return User.query.get(int(userID))

class User(db.Model, UserMixin):                                                # User is also the "BusinessOwner", or the overarching account. 
    id = db.Column(db.Integer, primary_key = True)
    userFirstName = db.Column(db.String(100), nullable=False)
    userLastName = db.Column(db.String(100), nullable=False)
    userEmail = db.Column(db.String(120), unique=True, nullable=False)
    # A hash will be generated for userImage to be 20 Char, and userPass as 60 Char
    userImage = db.Column(db.String(20), nullable=False, default='default.jpg')
    userPassword = db.Column(db.String(60), nullable=False)
    staffers = db.relationship('Staff', backref='userowner', lazy=True, uselist=False)     # 1 User -> * Staff. Lazy=True db will load data in one go
    

    def __repr__(self):
        return f"User('{self.userEmail}', '{self.userPassword}', '{self.userImage}')"


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    prefName = db.Column(db.String(100), nullable=False)    # This is what will be used to send out messages
    email = db.Column(db.String(120), nullable=False)
    service = db.Column(db.String(50))
    bookURL = db.Column(db.String(120), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)   # Attaches staff to UserID
    clients = db.relationship('Client', backref='staffowner', lazy=True)         # 1 Staff -> * Clients
 

class Client(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.Integer)
    status = db.Column(db.String(30))
    pswd = db.Column(db.String(60))                                             # For when we want to give clients a way to make their own changes
    staffid = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)   # Attaches client to staffID
    alerts = db.relationship('TempWaitAlert', backref='alertwho', lazy=True)          # 1 Client -> * Alerts
    clientprefer = db.relationship('ClientPref', backref='iprefer', lazy=True, uselist=False)          # 1 Client -> * Preferences

    def to_dict(self):
        return {
            'id': self.id,
            'fname': self.firstName,
            'lname': self.lastName,
            'email': self.email,
            'mobile': self.mobile,
            'status': self.status
        }





class ClientPref(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    minDuration = db.Column(db.Integer, nullable=False, default=60)
    lastNotified = db.Column(db.DateTime)
    lastClicked = db.Column(db.DateTime)         # For future if able to build SMTP tracking functionality 
    lastUpdated = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # 1 record will be created for *each* slot that the client is available for
    # So if client available only for MondayAM, TuesAM and WedsAM, then there will be 3x client pref records
    # timeavail = db.Column(db.Integer, nullable=False, default=0)           # 0 == Available for all slots, otherwise refer to AvailTimes table. 
    availall = db.Column(db.Integer, nullable=False)
    avtimes = db.relationship("AvailTimes", secondary="preftimes", back_populates="clientprefs" )
    prefstaffer = db.relationship('PrefStaff', backref='preferwho', lazy=True)
    clientid = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)   # Attaches ClientPref to Client's ID


class AvailTimes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    timeUnit = db.Column(db.String(30), nullable=False, unique=True)    # For now, split into AM and PM chunks. 
    clientprefs = db.relationship("ClientPref", secondary="preftimes", back_populates="avtimes" )
    def __str__(self):
        return self.timeUnit


# Association table connecting the ClientPref with AvailTimes 
db.Table(
    'preftimes', 
    db.Column("clientpref_id", db.ForeignKey('client_pref.id'), primary_key=True),
    db.Column("availtimes_id", db.ForeignKey('avail_times.id'), primary_key=True),
)


# This table is used to link the client's preference to staff. 
# For the MVP, this wont be used because there's only one staff per user so the client either signs up or not. 
# Instead, the staffPreference will default to 0 (no preference)
class PrefStaff(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    clientprefid = db.Column(db.Integer, db.ForeignKey('client_pref.id'), nullable=False, default=0)      # 0 == no preference
    staffprefid = db.Column(db.Integer, nullable=False)


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
    staffuid = db.Column(db.Integer, nullable=False)
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