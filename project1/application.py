import os
import requests

from flask import Flask, render_template, request, session, url_for, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

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

@app.route("/", methods=["GET", "POST"])
def index():
    # Set website display variables
    if session.get("username") is None:
        return render_template("login.html")
    return redirect(url_for('home'))

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")

@app.route("/createuser", methods=["POST"])
def createuser():
    request_username = request.form.get("request_username")
    request_password = request.form.get("request_password")
    repeat_password = request.form.get("repeat_password")
    if request_password != repeat_password:
        return render_template("error.html", message="Passwords do not match, please try again.")
    if db.execute("SELECT * FROM users WHERE name = :name", {"name": request_username}).rowcount != 0:
        return render_template("error.html", message="Username already exists, please try again.")
    db.execute("INSERT INTO users (name, password) VALUES (:name, :password)", {"name": request_username, "password": request_password})
    db.commit()
    session["username"] = request_username
    return render_template("success.html", message="You have successfully signed up.")

@app.route("/attemptlogin", methods=["POST"])
def attemptlogin():
    username = request.form.get("username")
    password = request.form.get("password")
    # Make sure username exists in database
    if db.execute("SELECT * FROM users WHERE name = :name", {"name": username}).rowcount == 0:
        return render_template("error.html", message="Invalid user name, please sign up first.")
    # Make sure the password is correct
    passwords = db.execute("SELECT password FROM users WHERE name = :name", {"name": username})
    for row in passwords:
        if row[0] == password:
            session["username"] = username
            return redirect(url_for('home'))
    return render_template("error.html", message="Your password is incorrect, please try again.")

@app.route('/attemptlogout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route("/home", methods=["GET", "POST"])
def home():
    username=session["username"]
    return render_template("home.html", username=username)

@app.route("/search", methods=["POST"])
def search():
    searchrequest = request.form.get("bookinfo")
    results = db.execute("SELECT * FROM books WHERE isbn LIKE '%' || :isbn || '%' OR title LIKE '%' || :title || '%' OR author LIKE '%' || :author || '%'", {"isbn": searchrequest, "title": searchrequest, "author": searchrequest}).fetchall()
    return render_template("search.html", results=results)

@app.route("/book")
def book():
    # Set website display variables
    return render_template("book.html")
