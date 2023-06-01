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



####################################
# Tips & Tricks
#----------------------------------
# To get out of venv
>> venv\Scripts\deactivate

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


