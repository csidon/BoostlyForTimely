from flask import Flask
from flask_sqlalchemy import SQLAlchemy	# Manages database sync
from flask_bcrypt import Bcrypt			# Hashes passwords so that they are secure
from flask_login import LoginManager	# Manages logins/cookies



application = Flask(__name__)

# Set a secret key to prevent against modifying cookies and XSS requests on forms (randomly generated using python's secrets.token_hex)
application.config['SECRET_KEY'] = 'ea3c9fdee984c581c3272cb37b6268746bc67adcdbb60ede'
# format for the URI is postgresql://{user}:{password}@{RDS endpoint}/{db name, default is postgres}
# application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgresmaster:1NewPass!@s3-lambda-rdspostgresv2.clbvaq8mp9jk.us-east-1.rds.amazonaws.com:5432/boostly_db'
# application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(application)
application.app_context().push()
bcrypt = Bcrypt(application)
loginManager = LoginManager(application)
loginManager.login_view = 'login'			# Flask function that brings user back to login page if they haven't logged in
loginManager.login_message_category = 'info'		# Makes pretty - Assigns Bootstraps' "info" category styling to login-related messages

from boostly.users.routes import users
# from boostly.tasks.routes import tasks
from boostly.main.routes import main
from boostly.alerts.routes import alerts

application.register_blueprint(users)
# application.register_blueprint(tasks)
application.register_blueprint(main)
application.register_blueprint(alerts)