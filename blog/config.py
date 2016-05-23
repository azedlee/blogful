import os
class DevelopmentConfig(object):
    # Set location of your database
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/blogful"
    # Tell Flask to use Debug mode to track down any errors in your application
    DEBUG = True
    # SECRET_KEY is used to cryptographically secure your application's session
    # However, it is not safe to keep the key in configuration, so we use os.environ.get to obtain
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", os.urandom(12))

### If connection refused, execute "sudo service postgresql start"
### In the terminal prompt, enter the following:
###     export BLOGFUL_SECRET_KEY="your_secret_key_here"