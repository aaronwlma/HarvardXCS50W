import os
import requests

from flask import Flask, render_template, request, session, url_for, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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

@app.route("/", methods=["GET", "POST"])
def index():
    # Set website display variables
    if session.get("username") is None:
        username = None
        return render_template("login.html", username=username)
    return redirect(url_for('home'))

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    username = None
    return render_template("signup.html", username=username)

@app.route("/createuser", methods=["POST"])
def createuser():
    if session.get("username") is None:
        username = None
    request_username = request.form.get("request_username")
    request_password = request.form.get("request_password")
    repeat_password = request.form.get("repeat_password")
    if request_password != repeat_password:
        return render_template("error.html", message="Passwords do not match, please try again.", username=username, signuppage=True)
    if request_username is "" or request_password is "":
        return render_template("error.html", message="Not all fields are filled, please try again.", username=username, signuppage=True)
    if db.execute("SELECT * FROM users WHERE name = :name", {"name": request_username}).rowcount != 0:
        username = None
        return render_template("error.html", message="Username already exists, please try again.", username=username, signuppage=True)
    db.execute("INSERT INTO users (name, password) VALUES (:name, :password)", {"name": request_username, "password": request_password})
    db.commit()
    session["username"] = request_username
    return render_template("success.html", message="You have successfully signed up.", username=request_username, newuser=True)

@app.route("/attemptlogin", methods=["POST"])
def attemptlogin():
    username = request.form.get("username")
    password = request.form.get("password")
    # Make sure username exists in database
    if db.execute("SELECT * FROM users WHERE name = :name", {"name": username}).rowcount == 0:
        username = None
        return render_template("error.html", message="Invalid user name, please sign up first.", username=username)
    # Make sure the password is correct
    passwords = db.execute("SELECT password FROM users WHERE name = :name", {"name": username})
    for row in passwords:
        if row[0] == password:
            session["username"] = username
            return redirect(url_for('home'))
    username = None
    return render_template("error.html", message="Your password is incorrect, please try again.", username=username)

@app.route("/attemptlogout")
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route("/home", methods=["GET", "POST"])
def home():
    username=session["username"]
    return render_template("home.html", username=username)

@app.route("/search", methods=["GET", "POST"])
def search():
    username=session["username"]
    searchrequest = request.form.get("bookinfo")
    results = db.execute("SELECT * FROM books WHERE isbn LIKE '%' || :isbn || '%' OR title LIKE '%' || :title || '%' OR author LIKE '%' || :author || '%'", {"isbn": searchrequest, "title": searchrequest, "author": searchrequest}).fetchall()
    numresults = len(results)
    if numresults == 0:
        return render_template("search.html", results=results, numresults=numresults, username=username)
    return render_template("search.html", results=results, numresults=numresults, username=username)

@app.route("/book/")
def allbooks():
    username=session["username"]
    results = db.execute("SELECT * FROM books").fetchall()
    numresults = len(results)
    return render_template("allbooks.html", results=results, numresults=numresults, username=username)

@app.route("/book/<string:isbn>", methods=["GET"])
def book(isbn):
    username=session["username"]
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return render_template("error.html", message="Book does not exist in our database.")
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": API_KEY, "isbns": isbn})
    resJson = res.json()
    try:
        goodreadsrating = resJson['books'][0]['average_rating']
        goodreadsnumreview = resJson['books'][0]['reviews_count']
    except:
        goodreadsrating = 'Does not exist on GoodReads'
        goodreadsnumreview = 'Does not exist on GoodReads'
    # Set website display variables
    return render_template("book.html", bookisbn=book[1], booktitle=book[2], bookauthor=book[3], bookyear=book[4], goodreadsrating=goodreadsrating, goodreadsnumreview=goodreadsnumreview, username=username)

@app.route("/attemptreview", methods=["POST"])
def attemptreview():
    print('hehe2')
    userrating = request.form.get("userrating")
    userreview = request.form.get("userreview")
    print(userrating)
    print('hehe3')
    print(userreview)
    return render_template("success.html", message="Success! Your review has been received and posted to your ReviewBook.")
