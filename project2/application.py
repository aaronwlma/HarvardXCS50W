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

@app.route("/")
def index():
    print(users)
    return render_template("index.html", users=users)

@socketio.on("login")
def login(user):
    if user not in users:
        users.append(user)
        print(users)
        emit("announce login", {"users": users}, broadcast=True)

@socketio.on("logout")
def logout(user):
    users.remove(user)
    print(users)
    emit("announce logout", {"users": users}, broadcast=True)
