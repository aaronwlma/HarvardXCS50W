#!/bin/bash

export FLASK_APP=application.py
export FLASK_DEBUG=1
export DATABASE_URL=postgres://lxgolwltztdvwv:3bde8230fe316aa474f8cf56b2fef0f5f38eb1b5855e1414cf2ac2b777737985@ec2-50-17-227-28.compute-1.amazonaws.com:5432/d9leo47uad454m
export API_KEY = "Bu3bld9w16f5oAK0XsaA"

echo "FLASK_APP=" $FLASK_APP
echo "FLASK_DEBUG=" $FLASK_DEBUG
echo "DATABASE_URL=" $DATABASE_URL
echo "API_KEY=" $API_KEY
