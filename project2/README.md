# Project 2 - Flack: Webpage Chat Client

This project was created in fulfillment of HarvardX's "CS50W: Web Programming with Python and JavaScript" course on edX.  The project is a chat client webpage that allows users to log in, create chat channels, and chat with other users connected to the server.  The server side program in this project was written in Python and the client side program was written in JavaScript and HTML.  Additional notable tools and languages used in this project were Flask and SocketIO.  The primary objective of the project was to practice client and server communication by creating a dynamic webpage using Python and JavaScript.

## Requirements

The resulting webpage can be viewed by pulling this repository, installing the requirements, and launching Flask.  

1.  First, requirements.txt needs to be installed.  This can be done with the following terminal command in the repository folder:
```
pip3 install -r requirements.txt
```
2.  Once the requirements are installed, the computer environment variables need to be set.  This can be done with the following terminal command in the repository folder:
```
export FLASK_APP=application.py
export FLASK_DEBUG=0
```
Do note that the user must put FLASK_DEBUG to 0 in order for the website application to work.

Once these requirements are met, running Flask will deploy the webpage to a local host while making the local machine the server.  Note that the program uses local storage to determine the current user.  If the server is to be shut down, the local storage should be properly cleared before the reset.  If it is not, then once the server runs again, the user will get no functionality until he or she re-logs.

## Webpage Details

The following notes details key components in the repository and how they relate to the webpage.

#### application.py

This is backbone of the server.  It contains definitions and all possible routes, broadcast messages, and how to handle them.  Note that the program imports class objects from classes.py, so the server needs classes.py to properly run.

The program can be broken down into three main sections:  defined functions, application routes, and socket listeners.  In the defined functions portion of the code, the functions deal with validating and making user and channel names.  These functions compare against the server array (for users) and dictionary (for channels) to verify whether the channel or user is already in use.  If the user or channel is valid, then the client can proceed with their request.  If not, then the client receives an invalid response and responds accordingly.  In the application routes, the login and newchan routes are the routes take the clients are redirected to when requesting in making a new user or channel.  The routes call the functions mentioned earlier, and return the valid or invalid response depending on the server's response.  Lastly, the socket listeners listen for a message from the clients, and when the clients send that message, the server runs the associated program and broadcasts the results.  The associated functions with the socket include all related chat and user information retrieval from the server.

#### classes.py

This program stores the definitions for the associated class objects for the server.  The three objects created in this body of code is chat, user, and message.  The chat object stores up to 100 messages, and removes the oldest if the 101th one is inputted.  The chat object also stores the usernames of those currently using the chat.  The user object carries the user name, as well as the chat channel that the object is currently engaged in.  Lastly, the message object carries the username, the message, as well as the time stamp of the message in the object.  These three objects are called by the main application to organize the data received from the client side and to sent back to engaged clients.

#### templates/index.html

This HTML template corresponds to the displayed webpage.  The proper html template is called using render_template in the application.py script.  Conditions using Jinja2 were also introduced in the templates to display the proper input user name.

#### static/check.js

This is the JavaScript script that verifies that all necessary information is retrieved before loading the webpage.  It prompts the user to input a username if no local storage value for that is found.  The prompt is called recursively, as it continually checks against the server values until a value that is valid is received.  It establishes the default chat channel to be the Global Chat, and allows the webpage to be generated.

#### static/page.js

This is the main JavaScript script that determines what the webpage displays depending on what is sent and received to and from the server.  Using SocketIO, this script is a listener that sends requests and listens for announcements in regards to updating chat elements and channel information.  The first half deals with sending information to the server using querySelector.  Logging out, changing channels, making channels, and sending messages to the chat are all dealt with by selecting HTML elements to trigger a send command to the server to update.  The second half deals with receiving information from the server when the server broadcasts new information.  The listeners deal with receiving new messages from other users, users logging in and out and users changing channels.  Collectively, this script actively listens for new information from the server while providing an avenue for the client to communicate with the server.

## Places to Improve

Naming conventions across this project are inconsistent.  "Chat," "chan," and "channel" are used interchangeably, and camel casing is used only sparingly.  Additionally, variables are defined multiple times when not needed.  These two inconsistencies lead to a dirtier code, and this was a result of not properly planning out the structure of the code prior to beginning the project.  There are also a few edge cases not addressed in this project.  If a user launches one webpage in one window, and opens and incognito window in another, the other page will enter a reloading loop.  The looping ends once the window becomes the active window, but this behavior is due to using document.reload() being placed in the recursive loop asking for the user name.  In order to resolve this situation, a more robust implementation of verifying user names should be employed.  Lastly, the webpage layout was designed with only one window size in mind.  If this webpage were to be loaded on a different sized window, the elements within the window would not be aesthetically scaled properly.  While this issue could be solved using CSS/Bootstrap properties, the primary focus of this project was to work with communication between server and client, and so support for multiple browsers was deemed to be too time consuming to address.

## Concluding Remarks

This project--creating chat webpage using Python and Javascript--allowed me to have a detailed understanding of how communication between server and client could be.  I learned how to use multiple programming languages together in one application, set up SocketIO listeners and broadcasts, create a website that dynamically updates its content based on server values, and implement intuitive class objects to make organization of information more intuitive.  This project provided valuable information to use in the future, when I have to deal with multiple clients communicating with servers.  I also learned more about JavaScript conventions and syntax.  I found that I while I get excited for writing the functions for the server, I do not get excited for setting up the client side behavior.  I found that writing code for how variables are displayed feels tedious.  Overall, the project allowed me to exercise a broad range of skills related to web programming.  I exercised JavaScript in writing scripts to deal with communication with the server, Python programming for creating objects and using them, and adapting new tools such as SocketIO to use in website deployment.  However, I did not particularly enjoy making sure my clients were displaying the server information in a presentable manner.  In the future, when I create webpages to show case my projects, I will likely try to keep the webpage elements looking clean and simple to avoid having to consider how the information will look on multiple client displays.  

## Exercised Skills/Tools/Languages
- Python
- JavaScript
- HTML
- Flask
- SocketIO
