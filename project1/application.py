import os
import requests

from flask import Flask, session, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Before running, set environment variables below
# export FLASK_APP=application.py
# export FLASK_DEBUG=1
# export DATABASE_URL=postgres://lxgolwltztdvwv:3bde8230fe316aa474f8cf56b2fef0f5f38eb1b5855e1414cf2ac2b777737985@ec2-50-17-227-28.compute-1.amazonaws.com:5432/d9leo47uad454m

app = Flask(__name__)
API_KEY = "Bu3bld9w16f5oAK0XsaA"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    # Set website display variables
    return render_template("index.html")

@app.route("/search")
def search():
    # Set website display variables
    return render_template("search.html")
    
@app.route("/book")
def book():
    # Set website display variables
    return render_template("book.html")
