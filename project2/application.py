################################################################################
# Flack - Main Application (Server)
################################################################################
# @author         Aaron Ma
# @description    Chat client that allows conversations in a global chat or in a
#                 custom channel
# @component      Program to initialize server values that clients can
#                 communicate with to send and receive chat messages with other
#                 clients
# @date           May 30th, 2019
################################################################################

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

# Initial global server values
onlineUsers = {}
globalChat = Chat(name="Global Chat")
channels = {'Global Chat': globalChat}
if __name__ == '__main__':
    socketio.run(app)

################################################################################
# Functions for the flask website
################################################################################
# Function to compare username to server usernames to determine validity
def validUser(username):
    valid = False
    if (username == None or username == '' or username == 'null'):
        valid = False
    else:
        if username in onlineUsers:
            valid = False
        else:
            valid = True
    return valid

# Function to compare channel name to server channel names to determine validity
def validChan(channame):
    valid = False
    if (channame == None or channame == '' or channame == 'null'):
        valid = False
    else:
        if channame in channels:
            valid = False
        else:
            valid = True
    return valid

# Function to create a user object with default parameters
def makeUser(username):
    userObj = User(username=username, chat='Global Chat')
    onlineUsers[username] = userObj
    globalChat.add_user(userObj)
    return userObj

# Function to create a channel object with default parameters
def makeChan(channame):
    chanObj = Chat(name=channame)
    channels[channame] = chanObj
    return chanObj

################################################################################
# Routes and socket communications for the flask website
################################################################################
# Default page for the application
@app.route("/")
def index():
    return render_template("index.html", channels=channels)

# XMLHttpRequest to listen for attempts to log in to chat
@app.route("/login", methods=["GET", "POST"])
def login():
    user = request.form.get("nameInput")
    valid = False
    if (validUser(user) == True):
        if user not in onlineUsers:
            newUser = makeUser(user)
            valid = True
        else:
            valid = False
    else:
        valid = False
    return jsonify({"valid": valid})

# XMLHttpRequest to listen for attempts to create a new channel
@app.route("/newchan", methods=["GET", "POST"])
def newchan():
    chan = request.form.get("chanInput")
    valid = False
    if (validChan(chan) == True):
        if chan not in channels:
            newChan = makeChan(chan)
            valid = True
        else:
            valid = False
    else:
        valid = False
    return jsonify({"valid": valid})

# Socket listeners to trigger proper events
# Listener to return the global user list to the client
@socketio.on("get userlist")
def userlist():
    userlist = list(onlineUsers.keys())
    emit("announce userlist", userlist, broadcast=True)

# Listener that generates initial log in webpage values on client side
@socketio.on("initial login")
def initiallogin(user):
    currentUser = onlineUsers[user]
    currentChat = channels[currentUser.chat]

    message = Message(currentUser, user + " has joined the channel.")
    message.joinchat = True
    currentChat.add_message(currentUser, message)
    chatHistory = currentChat.return_messages()
    emit("announce channel chat", [chatHistory, currentChat.name], broadcast=True)

# Listener that removes user information from the server and alerts the client
@socketio.on("logout")
def logout(user):
    currentUser = onlineUsers[user]
    currentChat = channels[currentUser.chat]

    message = Message(currentUser, user + " has left the channel.")
    message.joinchat = True
    currentChat.add_message(currentUser, message)
    chatHistory = currentChat.return_messages()
    emit("announce channel chat", [chatHistory, currentChat.name], broadcast=True)

    if user in onlineUsers:
        del onlineUsers[user]
    userlist = list(onlineUsers.keys())
    emit("announce userlist", userlist, broadcast=True)

# Listener that receives a comment and saves it to the server and broadcasting it to all clients
@socketio.on("submit comment")
def comment(username, channame, comment):
    currentUser = onlineUsers[username]
    currentChat = channels[channame]

    message = Message(currentUser, comment)
    currentChat.add_message(currentUser, message)
    data = message.print_message()
    chatHistory = currentChat.return_messages()
    emit("announce channel chat", [chatHistory, channame], broadcast=True)

# Listener that changes user established channel and returns proper channel chat info to client
@socketio.on("change channel")
def changechannel(currchan, channame, username):
    userObj = onlineUsers[username]
    userObj.chat = channame
    currentUser = onlineUsers[username]
    currentChat = channels[currchan]

    message = Message(currentUser, username + " has left the channel.")
    message.joinchat = True
    currentChat.add_message(currentUser, message)
    chatHistory = currentChat.return_messages()
    emit("announce channel chat", [chatHistory, currchan], broadcast=True)

    currentChat = channels[channame]
    message = Message(currentUser, username + " has joined the channel.")
    message.joinchat = True
    currentChat.add_message(currentUser, message)
    chatHistory = currentChat.return_messages()
    emit("announce channel chat", [chatHistory, channame], broadcast=True)

# Listener that returns the channel's chat history to the client
@socketio.on("get channel chat")
def channelchat(channame):
    chat = channels[channame]
    chatHistory = chat.return_messages()
    emit("announce channel chat", [chatHistory, channame], broadcast=True)

# Listener that returns the existing channels to the clients
@socketio.on("get channel list")
def channellist():
    channellist = list(channels.keys())
    emit("announce channel list", channellist, broadcast=True)
