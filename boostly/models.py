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
    # employees = db.relationship('Employee', backref='owneruser', lazy=True)     # 1 User -> * Employees. Lazy=True db will load data in one go
    

    def __repr__(self):
        return f"User('{self.userEmail}', '{self.userPassword}', '{self.userImage}')"


# class Employee(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     firstName = db.Column(db.String(100), nullable=False)
#     lastName = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     ownerID = db.Column(db.Integer, db.ForeignKey('owneruser.id'), nullable=False)   # Attaches employee to UserID
#     clients = db.relationship('Client', backref='belongsto', lazy=True)         # 1 Employee -> * Clients
#     alerts = db.relationship('Alert', backref='employee', lazy=True)

# class Client(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     firstName = db.Column(db.String(100), nullable=False)
#     lastName = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     mobile = db.Column(db.Integer)
#     ownerID = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)   # Attaches client to EmployeeID
#     alerts = db.relationship('Alert', backref='client', lazy=True)


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    alertTitle = db.Column(db.String(180), nullable=False)
    alertDescription = db.Column(db.Text, nullable=False)
    slotStartDateTime = db.Column(db.DateTime, nullable=False)      # Set upon instantiation
    slotLength = db.Column(db.Integer, nullable=False)

    alertStatus = db.Column(db.String, nullable=True, default='pending')       # Pending, Sent, Archived
    alertSentOn = db.Column(db.DateTime)                                        # Default is empty, filled only when alert is sent
    # alertRecipientID = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False) 
    # ownerID = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)       # Attached to employee instead of main user 

    def __repr__(self):
        return f"Alerts('{self.alertTitle}', '{self.alertDescription}', '{self.slotStartDateTime}','{self.slotStartLength}','{self.alertStatus}')"





    slotStartDate = DateField('Date of available appointment slot', format="%Y-%m-%d")
    # slotday = 
    slotStartTime = TimeField('Appointment Start Time', validators=[DataRequired()], default = '')
    slotLength = 