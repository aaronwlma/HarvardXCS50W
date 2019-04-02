# Project 1 - ReviewBook: Website for Reviewing and Rating Books

This project was created in fulfillment of HarvardX's "CS50W: Web Programming with Python and JavaScript" course on edX.  The project is a book review webpage that allows users to sign up, view, and write reviews for books on the website database.  The project was written in Python with the database constructed with PostgreSQL, and the contents were displayed using HTML.  Additional notable tools and languages used in this project were Flask, Heroku, and SQLAlchemy.  The primary objective of the project was to create a dynamic webpage built on Python using Flask.

## Requirements

The resulting webpage can be viewed by pulling this repository, installing the requirements, and launching Flask.  

1.  First, requirements.txt needs to be installed.  This can be done with the following terminal command in the repository folder:
```
pip3 install -r requirements.txt
```
2.  Once the requirements are installed, a PostgreSQL database location needs to be created.  In this project, a PostgreSQL database was hosted on Heroku, and a database URL was generated.  This database URL is required in order to store the website data.

3.  Once the requirements are installed and a database URL was obtained, the computer environment variables need to be set.  This can be done with the following terminal command in the repository folder:
```
export FLASK_APP=application.py
export FLASK_DEBUG=1
export DATABASE_URL=(INSERT YOUR DATABASE URL HERE)
```
Do note that the user must put their own database URL in the statement above for the website application to work.

Once these requirements are met, running Flask will deploy the webpage to a local host.  Note that in order to enable data from GoodReads, the user must acquire their own GoodReads API key and insert the key in application.py.  Data from GoodReads is disabled by default, and is not part of the requirement for the website to run.

## Webpage Details

The following notes details key components in the repository and how they relate to the webpage.

#### application.py

This is backbone of the webpage.  It contains definitions and all possible website URL routes and how to handle them.  Note that to enable data from GoodReads, `goodreads=False` should be set to `True` in this file.

Each app route addresses either generating a webpage, a JSON response, or conducting a check.  For the app routes generating webpages, each function associated with the app route first collects the required data.  This may be the username, password, or book id. Once the information is verified or stored in a session, the information is rendered in a template that is preset in an html template file.  For the app route that generates a JSON response, the function takes in an input isbn, and retrieves data from the PostgreSQL database for the user and returns the information as a JSON response.  Lastly, for the app routes that conduct checks, these app routes check and update the PostgreSQL database with new information, and if it returns successful, it will generate a success html page that is also from a html template.  If it proves unsuccessful, these app routes will return error pages with the proper information.

#### import.py

This is the script that takes a books CSV and inputs the information into the PostgreSQL database hosted on Heroku.  The script reads in the CSV file and loops through each value to insert into the database.

#### create.sql

This is the queries sent to the database to create the proper database tables and relations to support the website.

#### templates/.html

These are the html templates corresponding to the webpage.  The proper html template is called using render_template in the application.py script.  Conditions using Jinja2 were also introduced in the templates to display the proper information depending on various situations.  All the html templates extend layout.html, which is the parent layout for the website that specifies the CSS stylesheet for the webpage.

## Places to Improve

Passwords are stored as plain text in the PostgreSQL database.  With proper SQL injection, a password can be retrieved in plain text.  For security reasons, it would be best to protect this information.  Also, the variable naming in this project did not adhere to Python conventional syntax.  In the future, naming variables spaced with underscores will be ideal.  Additionally, the project uses a number of SQL queries to retrieve and update data to the database.  In the future, it may be cleaner and simpler to use object relational mapping to manipulate database information.  This would allow for quicker implementation of new functionality to the website as well.

## Concluding Remarks

This project--creating a dynamic webpage using Python with Flask--allowed me to have a detailed understanding of how dynamic websites function.  I learned how to set up a SQL database, create a website that interfaces with this database, and deploy a webpage that allows users to interact with the database.  This is a valuable tool to have in the future, when I have other projects that I would like to use APIs to set up a simple dynamic website.  I also learned more about Python conventions and syntax.  I found that I while I get excited for writing the functions for the website, I do not get excited for setting up the environment for the website to run.  Overall, the project allowed me to exercise a broad range of skills related to web programming.  I exercised SQL database design and queries, Python programming for webpages, and adapting new tools to use in website deployment.  However, I did not particularly enjoy making sure my local files met the requirements to run the website.  In the future, when I create webpages to show case my projects, I will likely try to use as few tools with dependencies as possible to allow for my webpage to be self-contained.  

## Exercised Skills/Tools/Languages
- Python
- PostgreSQL
- HTML
- Flask
