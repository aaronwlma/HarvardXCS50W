################################################################################
# Flack
################################################################################
# @author         Aaron Ma
# @description    Chat client that allows conversations in a global chat or in a
#                 custom channel
# @date           May 22nd, 2019
################################################################################

# ALL FUNCTIONS IN, RIGHT NOW DUPLICATE CHANNEL NAMES ARE WORKING AND IT SHOULDNT

################################################################################
# Import the relevant libraries and tools for the website to run
################################################################################
import os
import requests

from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_session import Session
from classes import *

################################################################################
# Developer values for use and troubleshooting
################################################################################
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
Session(app)

# Initial server values
onlineUsers = {}
globalChat = Chat(name="Global Chat")
channels = {'Global Chat': globalChat}
if __name__ == '__main__':
    socketio.run(app)

################################################################################
# Functions for the flask website
################################################################################
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
    userObj = User(username=username, chat='Global Chat')
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
    print(list(channels.keys()))
    return chanObj

################################################################################
# Routes and socket communications for the flask website
################################################################################
# Default page for the application
@app.route("/")
def index():
    return render_template("index.html", users=list(onlineUsers.keys()), channels=channels)

# XMLHttpRequest to listen for attempts to log in to chat
@app.route("/login", methods=["GET", "POST"])
def login():
    user = request.form.get("nameInput")
    valid = False
    if (validUser(user) == True):
        print("[ATTEMPT LOGIN]")
        if user not in onlineUsers:
            newUser = makeUser(user)
            print(newUser, "has connected.")
            print("Online users:")
            print(list(onlineUsers.keys()))
            valid = True
        else:
            print(user, "already logged in.")
    else:
        print(user, "is not a valid name.")
    return jsonify({"valid": valid})

# Socket listeners to trigger proper events
@socketio.on("get userlist")
def userlist():
    userlist = list(onlineUsers.keys())
    emit("announce userlist", userlist, broadcast=True)

@socketio.on("logout")
def logout(user):
    print("[ATTEMPT LOGOUT]")
    if user in onlineUsers:
        print(onlineUsers[user], "has logged out.")
        del onlineUsers[user]
        print("Online users:")
        print(onlineUsers)
    else:
        print(user, "does not exist to log out.")
    userlist = list(onlineUsers.keys())
    emit("announce userlist", userlist, broadcast=True)

@socketio.on("submit comment")
def comment(username, channame, comment):
    currentUser = onlineUsers[username]
    currentChat = channels[channame]
    message = Message(currentUser, comment)
    currentChat.add_message(currentUser, message)
    data = message.print_message()
    chatHistory = currentChat.return_messages()
    emit("announce channel chat", [chatHistory, channame], broadcast=True)

@socketio.on("create channel")
def createchannel(channame, username):
    print("[CREATE CHANNEL]")
    if channame in channels.keys():
        print(channame, "already exists.")
        emit("announce invalid channel", channame, broadcast=True)
    else:
        newChan = makeChan(channame)
        print(newChan, "was created.")
        userObj = onlineUsers[username]
        userObj.chat = channame
        newChan.add_user(userObj)
        print(userObj, "has been added", newChan)
        channellist = list(channels.keys())
        emit("announce channel list", channellist, broadcast=True)
        emit("announce change channel", channame, broadcast=True)

@socketio.on("change channel")
def changechannel(channame, username):
    print("[CHANGE CHANNEL]")
    userObj = onlineUsers[username]
    userObj.chat = channame
    emit("announce change channel", channame, broadcast=True)

@socketio.on("get channel chat")
def channelchat(channame):
    chat = channels[channame]
    chatHistory = chat.return_messages()
    emit("announce channel chat", [chatHistory, channame], broadcast=True)

@socketio.on("get channel list")
def channellist():
    channellist = list(channels.keys())
    emit("announce channel list", channellist, broadcast=True)
