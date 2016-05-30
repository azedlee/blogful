import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.login import UserMixin

from . import app

# Basic Boilerplate code for working with a database using SQLAlchemy
# Create an engine which will talk to the database specified in config.py
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

# Create a declarative base variable - acts like a repository for the models and will issue the create table
# statements to build up the database's table structure
Base = declarative_base()

# Commit and start a new session
Session = sessionmaker(bind=engine)
session = Session()

class Entry(Base):
    __tablename__ = "entries"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)
    author_id = Column(Integer, ForeignKey('users.id'))

# User model to create a login system
class User(Base, UserMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))
    entries = relationship("Entry", backref="author")

# Construct the table in the database

Base.metadata.create_all(engine)