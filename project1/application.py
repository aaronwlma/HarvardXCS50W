################################################################################
# ReviewBook
################################################################################
# @author         Aaron Ma
# @description    Flask webpage that allows users view book data and post
#                 personal reviews for books on the website
# @date           April 1st, 2019
################################################################################

################################################################################
# Import the relevant libraries and tools for the website to run
################################################################################
import os
import requests

from flask import Flask, render_template, request, session, url_for, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

################################################################################
# Developer values for use and troubleshooting
################################################################################
# Environment variables set for flask to run
# export FLASK_APP=application.py
# export FLASK_DEBUG=1
# export DATABASE_URL=(INSERT YOUR DATABASE URL HERE)

# Set goodreads to True if you have a API Key from GoodReads
goodreads = False
# if goodreads == True:
#     # API Key from GoodReads
#     API_KEY = "(INSERT YOUR GOODREADS API KEY HERE)"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

################################################################################
# Functions and routes for the flask website
################################################################################
@app.route("/", methods=["GET", "POST"])
def index():
    # Produce proper webpage depending on whether user is already logged in
    if session.get("username") is None:
        username = None
        return render_template("login.html", username=username)
    return redirect(url_for('home'))

@app.route("/login", methods=["GET", "POST"])
def login():
    # Webpage for logging in or signing up
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Webpage for signing up, username set to None as a precaution/prequisite
    username = None
    return render_template("signup.html", username=username)

@app.route("/createuser", methods=["POST"])
def createuser():
    # Function that creates user
    # Sets local variable username as None if the session is logged in as none
    if session.get("username") is None:
        username = None
    # Retrieves values from signup.html and stores to local variables
    request_username = request.form.get("request_username")
    request_password = request.form.get("request_password")
    repeat_password = request.form.get("repeat_password")
    # Conditional statements to make sure request account is a valid account
    # Passwords entered need to be identical
    if request_password != repeat_password:
        return render_template("error.html", message="Passwords do not match, please try again.", username=username, signuppage=True)
    # All fields have to be filled in
    if request_username is "" or request_password is "" or repeat_password is "":
        return render_template("error.html", message="Not all fields are filled, please try again.", username=username, signuppage=True)
    # Requested username cannot already exist
    if db.execute("SELECT * FROM users WHERE name = :name", {"name": request_username}).rowcount != 0:
        username = None
        return render_template("error.html", message="Username already exists, please try again.", username=username, signuppage=True)
    # If all conditions pass, insert form values into the database with the following query and return success webpage
    db.execute("INSERT INTO users (name, password) VALUES (:name, :password)", {"name": request_username, "password": request_password})
    user = db.execute("SELECT * FROM users WHERE name = :name", {"name": request_username})
    for row in user:
        if row[2] == request_password:
            session["userid"] = row[0]
            session["username"] = request_username
    db.commit()
    return render_template("success.html", message="You have successfully signed up.", username=request_username, newuser=True)

@app.route("/attemptlogin", methods=["POST"])
def attemptlogin():
    # Function to trigger log in attempt
    # Retrieve form values from login.html webpage
    username = request.form.get("username")
    password = request.form.get("password")
    # Conditional statements to verify log in
    # Make sure username exists in database
    if db.execute("SELECT * FROM users WHERE name = :name", {"name": username}).rowcount == 0:
        username = None
        return render_template("error.html", message="Invalid user name, please sign up first.", username=username)
    # If retrieved password is correct, redirect to the home.html webpage
    user = db.execute("SELECT * FROM users WHERE name = :name", {"name": username})
    for row in user:
        if row[2] == password:
            session["username"] = username
            session["userid"] = row[0]
            return redirect(url_for('home'))
    # If the password is incorrect, reset local variable to None and render error.html webpage
    username = None
    return render_template("error.html", message="Your password is incorrect, please try again.", username=username)

@app.route("/attemptlogout")
def logout():
   # Remove the username and userid from the session if it is there and go back to index page
   session.pop('username', None)
   session.pop('userid', None)
   return redirect(url_for('index'))

@app.route("/home", methods=["GET", "POST"])
def home():
    # Home webpage for users
    # Set session variables as local variables to work with
    username=session["username"]
    userid=session["userid"]
    # Retrieve user's previously reviewed books to display on the home.html page
    results = db.execute("SELECT rating, review, isbn, title, author FROM reviews JOIN users on users.id = user_id JOIN books on books.id = book_id WHERE user_id = :userid", {"userid": userid}).fetchall()
    numbooks = len(results)
    # Return the home page after retrieving the values
    return render_template("home.html", results=results, numbooks=numbooks, username=username)

@app.route("/search", methods=["GET", "POST"])
def search():
    # Search webpage for users
    # Retrieve session, form, and database values to store as local variables to render proper search result
    username=session["username"]
    searchrequest = request.form.get("bookinfo").lower()
    results = db.execute("SELECT * FROM books WHERE isbn LIKE '%' || :isbn || '%' OR LOWER(title) LIKE '%' || :title || '%' OR LOWER(author) LIKE '%' || :author || '%'", {"isbn": searchrequest, "title": searchrequest, "author": searchrequest}).fetchall()
    numresults = len(results)
    if numresults == 0:
        return render_template("search.html", results=results, numresults=numresults, username=username)
    return render_template("search.html", results=results, numresults=numresults, username=username)

@app.route("/book/")
def allbooks():
    # Show all books webpage for users
    # Retrieve session and database values to store as local variables to return all books on one page
    username=session["username"]
    results = db.execute("SELECT * FROM books").fetchall()
    numresults = len(results)
    return render_template("allbooks.html", results=results, numresults=numresults, username=username)

@app.route("/book/<string:isbn>", methods=["GET"])
def book(isbn):
    # Book information webpage for users
    # Retrieve session and database values to store as local variables and define useful local variables
    username=session["username"]
    userid=session["userid"]
    userevaluated = False
    # Make sure book exists and return error page if it doesn't
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return render_template("error.html", message="Book does not exist in our database.")
    session["bookid"] = book[0]
    if goodreads == True:
        # Retrieve GoodReads information on the book from their API (Make sure you define API_KEY as your own GoodReads API KEY)
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": API_KEY, "isbns": isbn})
        resJson = res.json()
        # Parse the JSON response for the information desired and store to useful local variables
        try:
            goodreadsrating = resJson['books'][0]['average_rating']
            goodreadsnumreview = resJson['books'][0]['reviews_count']
        except:
            goodreadsrating = 'Does not exist on GoodReads'
            goodreadsnumreview = 'Does not exist on GoodReads'
    else:
        goodreadsrating = 'GoodReads data disabled.'
        goodreadsnumreview = 'GoodReads data disabled.'
    # Generate information for the user
    # Check to see if user reviewed it already and if they did, display their review
    results = db.execute("SELECT rating, review, isbn, title, author FROM reviews JOIN users on users.id = user_id JOIN books on books.id = book_id WHERE reviews.user_id = :userid AND reviews.book_id = :bookid", {"userid": userid, "bookid": session["bookid"]}).fetchall()
    if len(results) != 0:
        userevaluated = True
    # Display the total number of reviews on the website as well as the average score
    totalresults = db.execute("SELECT rating, review, name FROM reviews JOIN users on users.id = user_id JOIN books on books.id = book_id WHERE reviews.book_id = :bookid", {"bookid": session["bookid"]}).fetchall()
    numreviews = len(totalresults)
    totalscore = 0
    for row in totalresults:
        print(row)
        totalscore += row[0]
    if numreviews == 0:
        averagerating = 'N/A'
    else:
        averagerating = round(totalscore/numreviews, 2)
    return render_template("book.html", totalresults=totalresults, averagerating=averagerating, numreviews=numreviews, userevaluated=userevaluated, results=results, bookisbn=book[1], booktitle=book[2], bookauthor=book[3], bookyear=book[4], goodreadsrating=goodreadsrating, goodreadsnumreview=goodreadsnumreview, username=username)

@app.route("/attemptreview", methods=["POST"])
def attemptreview():
    # Function to attempt submitting a review
    # Make sure there is a session id for the user and book
    if session["userid"] == None or session["bookid"] == None:
        return render_template("error.html", message="User ID or book ID not found, please return to home and try again.")
    # Retrieve the ratings from the book.html review page
    userrating = request.form.get("userrating")
    userreview = request.form.get("userreview")
    # Check to see if the user already has an entry on the database and produce error page if they already do
    results = db.execute("SELECT * FROM reviews WHERE user_id = :userid AND book_id = :bookid", {"userid": session["userid"], "bookid": session["bookid"]}).fetchall()
    if len(results) != 0:
        return render_template("error.html", message="User has already reviewed this book, please return to home and try again.")
    db.execute("INSERT INTO reviews (rating, review, user_id, book_id) VALUES (:rating, :review, :user_id, :book_id)", {"rating": userrating, "review": userreview, "user_id": session["userid"], "book_id": session["bookid"]})
    db.commit()
    session["bookid"] = None
    # Produce success page if the query succeeds
    return render_template("success.html", message="Success! Your review has been received and posted to your ReviewBook.", tobook=True)
