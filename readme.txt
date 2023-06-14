>> cd /boostly
>> venv\Scripts\activate

# Install the requirements
pip install -r requirements.txt 

>> in TLD

# One time setup to allow for easy running of Flask app
>> set FLASK_APP=application.py

# Test to see if it works
>> flask run

# To run app, in (venv)
python boostly.py

flask shell
from boostly import app

# FOR EB DEPLOYMENTS
Make sure that the following are NOT in the requirements.txt file!!
pypiwin32==223
pywin32==305

Make sure that main application is renamed to application.py and the flask app is also application and not another name. Refactor using Pycharm!!
Make sure that .idea and __pycache__ files are deleted before upload


user_1 = User(userFirstName='Chris', userLastName='DaTester', userEmail='chris.chonghuihui@gmail.com', userPassword='superDev!')

####################################
# Tips & Tricks
#----------------------------------
# To get out of venv
>> venv\Scripts\deactivate

## Basic sqlite db connectivity
# In TLD:
> python
>> from boostly import db
>> db.create_all()

## To add a user, after <<flask shell>> and <<create_all()>>, create a user using e.g. 
user_1 = User(userEmail='new@test.com', userPassword="password!")
db.session.add(user_1)
db.session.commit() 		## commits it to the DB


## Query users using:
User.query.all()
user = User.query.filter_by(userEmail="new@test.com".first()
user.id

## Adding a task (tied to user defined above)
task_1 = Task(taskTitle="Connect to DB", taskDescription="help!!!", userID=user.id, taskDue="02/03/23")
db.session.add(task_1)
db.session.commit()

## To clear db of all entries, use
db.drop_all()
from boostly.models import AvailTimes, Client, ClientCompany, ClientPref, Company, Event, PrefTimes, TempWaitAlert, User

# Some adds
from boostly import db
db.create_all()
from boostly.models import AvailTimes, Client, ClientCompany, ClientPref, Company, Event, PrefTimes, TempWaitAlert, User
coy1 = Company(companyName="Lena Massage")
db.session.add(coy1)
db.session.commit()
user1 = User(userFirstName="Testy", userLastName="Tester", userEmail="test@test.com", userPassword="$2b$12$6Lxi6jt8RtxNlggq9ugHlusxuDmbydw084Gl5IfQfcSVjERO6vtLu", companyid=1)
db.session.add(user1)
db.session.commit()
staff1 = Staff(firstName="The", lastName="Therapist", prefName="Terry", email="terry@pist.com", service="", bookURL="", userid=1)
client1 = Client(firstName="Richie", lastName="Rich", email="richie@rich.com", staffid=2)
alert1 = TempWaitAlert(slotStartDateTime="2023-05-16 20:15:00", slotLength=45, staffuid=2, clientid=2)
alert2 = TempWaitAlert(slotStartDateTime="2023-06-01 11:30:00", slotLength=120, staffuid=2, clientid=2)


user1 = User(userFirstName="Testy", userLastName="Tester", userEmail="test@test.com", userPassword="$2b$12$6Lxi6jt8RtxNlggq9ugHlusxuDmbydw084Gl5IfQfcSVjERO6vtLu")
staff1 = Staff(firstName="Testy", lastName="Therapist", prefName="Terry", email="terry@pist.com", service="", bookURL="", userid=1)
client1 = Client(firstName="Baby", lastName="Yoda", email="yoda@client.com", mobile=220220222)


# Prepopulating the db with timeslots 
# (Not sure if this is acceptable, but coded this way so that it's clear what availtime options there are)
av1=AvailTimes(timeUnit='Monday')
av2=AvailTimes(timeUnit='Tuesday')
av3=AvailTimes(timeUnit='Wednesday')
av4=AvailTimes(timeUnit='Thursday')
av5=AvailTimes(timeUnit='Friday')
av6=AvailTimes(timeUnit='Saturday')
av7=AvailTimes(timeUnit='Sunday')

db.session.add(av1)
db.session.add(av2)
db.session.add(av3)
db.session.add(av4)
db.session.add(av5)
db.session.add(av6)
db.session.add(av7)
db.session.commit()

cp1=ClientPref(minDuration=60)

availList = [ AvailTimes('Monday AM'), AvailTimes('Monday PM'),
        AvailTimes('Tuesday AM'), AvailTimes('Tuesday PM'),
        AvailTimes('Wednesday AM'), AvailTimes('Wednesday PM'),
        AvailTimes('Thursday AM'), AvailTimes('Thursday PM'),
        AvailTimes('Friday AM'), AvailTimes('Friday PM'),
        AvailTimes('Saturday AM'), AvailTimes('Saturday PM'),
        AvailTimes('Sunday AM'), AvailTimes('Sunday PM')]
for each in availList:
    db.session.add(each)
db.session.commit()


<button class="btn btn-success btn-sm rounded-0" type="button" data-toggle="tooltip" data-placement="top" title="Edit"><i class="fa fa-edit"></i></button>