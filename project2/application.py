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

# Initial server values
onlineUsers = {}
globalChat = Chat(name="globalChat")
channels = {'globalChat': globalChat}

# Functions on the server
def validUser(username):
    valid = False
    if (username == None or username == '' or username == 'null'):
        print("Null value detected.")
    else:
        if username in onlineUsers:
            print(username, "is not valid.")
        else:
            print(username, "is valid.")
            valid = True
    return valid

def validChan(channame):
    valid = False
    if (channame == None or channame == '' or channame == 'null'):
        print("Null value detected.")
    else:
        if channame in channels:
            print(channame, "is not valid.")
        else:
            print(channame, "is valid.")
            valid = True
    return valid

def makeUser(username):
    userObj = User(username=username)
    onlineUsers[username] = userObj
    print("Added", userObj.username, "to user list.")
    print("Online users:")
    print(list(onlineUsers.keys()))
    globalChat.add_user(userObj)
    print(userObj, "has joined global chat.")
    return userObj

def makeChan(channame):
    chanObj = Chat(name=channame)
    channels[channame] = chanObj
    print("Added", chanObj.name, "to channel list.")
    print("Current channels:")
    print(channels)
    return chanObj

if __name__ == '__main__':
    socketio.run(app)

@app.route("/")
def index():
    return render_template("index.html", users=list(onlineUsers.keys()), channels=channels)

# Socket listeners to trigger proper events
@socketio.on("login")
def login(user):
    if (validUser(user) == True):
        print("[ATTEMPT LOGIN]")
        if user not in onlineUsers:
            newUser = makeUser(user)
            print(newUser, "has connected.")
            print("Online users:")
            print(list(onlineUsers.keys()))
            emit("announce userlist", list(onlineUsers.keys()), broadcast=True)
        else:
            print(user, "already logged in.")
    else:
        emit("fail validation", user, broadcast=True)


@socketio.on("logout")
def logout(user):
    print("[ATTEMPT LOGOUT]")
    if user in onlineUsers:
        print(onlineUsers[user], "has logged out.")
        del onlineUsers[user]
        print("Online users:")
        print(onlineUsers)
        emit("announce userlist", list(onlineUsers.keys()), broadcast=True)
    else:
        print(user, "does not exist to log out.")

@socketio.on("get userlist")
def userlist():
    print("[ANNOUNCE USER LIST]")
    emit("announce userlist", list(onlineUsers.keys()), broadcast=True)

# @socketio.on("submit comment")
# def comment(data):
#     currentUser = onlineUsers[data[0]]
#     currentChat = channels[data[1]]
#     message = Message(currentUser, data[2])
#     currentChat.add_message(currentUser, message)
#     currentChat.print_messages()
#     emit("announce comment", data, broadcast=True)
#
# @socketio.on("get channel chat")
# def channelchat(data):
#     print(data)
#     chatHistory = data['room']
#     for message in chatHistory:
#         print(message)
#     emit("announce channel chat", chatHistory, broadcast=True)

WORKING ON NEW LOGIN.  RIGHT NOW LOGIN DOES NOT PERSIST THROUGH REFRESH.
