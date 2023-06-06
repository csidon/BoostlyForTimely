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
    # employees = db.relationship('Staff', backref='owneruser', lazy=True)     # 1 User -> * Staff. Lazy=True db will load data in one go
    

    def __repr__(self):
        return f"User('{self.userEmail}', '{self.userPassword}', '{self.userImage}')"


# class Staff(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     firstName = db.Column(db.String(100), nullable=False)
#     lastName = db.Column(db.String(100), nullable=False)
#     prefName = db.Column(db.String(100), nullable=False)    # This is what will be used to send out messages
#     email = db.Column(db.String(120), nullable=False)
#     service = db.Column(db.String(30), nullable=False)
#     bookURL = db.Column(db.String(120), nullable=False)
#     ownerID = db.Column(db.Integer, db.ForeignKey('owneruser.id'), nullable=False)   # Attaches staff to UserID
#     clients = db.relationship('Client', backref='staff', lazy=True)         # 1 Staff -> * Clients
#     wAlert = db.relationship('TempWaitAlert', backref='staff', lazy=True)         # 1 Staff -> * Alerts

# class Client(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     firstName = db.Column(db.String(100), nullable=False)
#     lastName = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(120), nullable=False)
#     mobile = db.Column(db.Integer)
#     ownerID = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)   # Attaches client to staffID
#     wAlert = db.relationship('TempWaitAlert', backref='client', lazy=True) 


# class Event(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     calEventUID = db.Column(db.String(100), nullable=False)
#     eventOwner = db.Column(db.String(120), nullable=False)
#     status = db.Column(db.String(30), nullable=False)
#     eventStart = db.Column(db.DateTime, nullable=False)
#     eventEnd = db.Column(db.DateTime, nullable=False)
#     eventUpdated = db.Column(db.DateTime, nullable=False)


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
    # staff = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    # client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

    def __repr__(self):
        return f"TempWaitAlert('{self.id}', '{self.slotStartDateTime}', '{self.slotLength}','{self.sendStatus}')"

# class Alert(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     # alertOwner = db.Column(db.String(180), nullable=False)      # This will be the email address of the owner
#     alertTitle = db.Column(db.String(180), nullable=False)
#     alertDescription = db.Column(db.Text, nullable=False)
#     slotStartDateTime = db.Column(db.DateTime, nullable=False)      # Set upon instantiation
#     slotLength = db.Column(db.Integer, nullable=False)

#     alertStatus = db.Column(db.String, nullable=True, default='pending')       # Pending, Sent, Archived
#     alertSentOn = db.Column(db.DateTime)                                        # Default is empty, filled only when alert is sent
#     # alertRecipientID = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False) 
#     # ownerID = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)       # Attached to staff instead of main user 

#     def __repr__(self):
#         return f"Alerts('{self.alertTitle}', '{self.alertDescription}', '{self.slotStartDateTime}','{self.slotStartLength}','{self.alertStatus}')"

#     slotStartDate = DateField('Date of available appointment slot', format="%Y-%m-%d")
#     # slotday = 
#     slotStartTime = TimeField('Appointment Start Time', validators=[DataRequired()], default = '')
#     slotLength = 




