import os

# Import the Flask object
from flask import Flask

# Create an application instance
app = Flask(__name__)

# Sets config_path to the config we want for development, testing or production phases
config_path = os.environ.get("CONFIG_PATH", "blog.config.DevelopmentConfig")
app.config.from_object(config_path)

# Imports come after app object because the views.py and filters.py will both make use of the app object
# . is the current folder
from . import views
from . import filters
from . import login