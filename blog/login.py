from . import app
from flask.ext.login import LoginManager

from .database import session, User # Question - why is there a dot in front of the database

# Create an instance of the LoginManager and initialize it
login_manager = LoginManager() # Question - What does "Create an Instance of x" mean?
login_manager.init_app(app)

# login_view is the name of the view which an unauthorized user will be redirected to when they try
# to access a protected resource
login_manager.login_view = "login_get"
# login_message_category is a category used to classify any error messages from Flask-Login
# Used in conjunction with Bootstrap's alerts system to give the user information about the login process
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(id):
    return session.query(User).get(int(id))

