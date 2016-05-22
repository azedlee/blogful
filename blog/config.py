import os
class DevelopmentConfig(object):
    # Set location of your database
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/blogful"
    # Tell Flask to use Debug mode to track down any errors in your application
    DEBUG = True

### If connection refused, execute "sudo service postgresql start"