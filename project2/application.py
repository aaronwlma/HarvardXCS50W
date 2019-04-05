import os
import requests

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_session import Session
from classes import *

app = Flask(__name__, static_url_path='')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
Session(app)

if __name__ == '__main__':
    socketio.run(app)

users = []
chatrooms = []
votes = {"yes": 0, "no": 0, "maybe": 0}

@app.route("/")
def index():
    return render_template("index.html", votes=votes)

@socketio.on("submit vote")
def vote(data):
    selection = data["selection"]
    votes[selection] += 1
    emit("vote totals", votes, broadcast=True)

# @app.route("/attempt_login")
# def attempt_login():
#     login_name = request.form.get("login_name")
#     if User(login_name) in users:
#         print("User", login_name, "already exists. JS Popup here.")
#         return redirect(url_for('index'))
#     session["login_name"] = User(login_name)
#     users.append(session["login_name"])
#     print(users)
#     return redirect(url_for('index'))
#
# @app.route("/attempt_logout")
# def attempt_logout():
#     user = session.get("login_name")
#     session.pop("login_name", None)
#     try:
#         users.remove(user)
#     except:
#         print("WARNING: User object wasn't found. JS Popup here.")
#     print(users)
#     return redirect(url_for('index'))
