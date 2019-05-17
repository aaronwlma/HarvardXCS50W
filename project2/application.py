import os
import requests

from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_session import Session
from classes import *

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
Session(app)

if __name__ == '__main__':
    socketio.run(app)

users = []

@app.route("/")
def index():
    return render_template("index.html", users=users)

@socketio.on("login")
def login(user):
    if user not in users:
        users.append(user)
        print(users)
        emit("announce userlist", users, broadcast=True)

@socketio.on("logout")
def logout(user):
    if user in users:
        users.remove(user)
        print(users)
        emit("announce userlist", users, broadcast=True)

@socketio.on("get userlist")
def userlist():
    print(users)
    emit("announce userlist", users, broadcast=True)

@socketio.on("submit comment")
def comment(data):
    print(data)
    emit("announce comment", data, broadcast=True)

# WORKS, BUT ONLINE USERS DONT LOAD ON REFRESH, NEED THAT WORKING FOR MODEL FOR CHAT
