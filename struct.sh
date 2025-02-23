#!/bin/bash

# Create the main directory
mkdir rodentsec

# Navigate into the main directory
cd my_flask_app

# Create the app directory and its subdirectories
mkdir app
mkdir app/routes
mkdir app/templates
mkdir app/static
mkdir app/static/css
mkdir app/static/js

# Create the migrations directory
mkdir migrations

# Create the __init__.py files
touch app/__init__.py
touch app/routes/__init__.py

# Create the Python files
touch app/models.py
touch app/routes/auth.py
touch app/routes/main.py
touch config.py
touch run.py
touch requirements.txt
touch .env

# Create the HTML template files
touch app/templates/base.html
touch app/templates/home.html
touch app/templates/services.html
touch app/templates/about.html
touch app/templates/contact.html
touch app/templates/login.html
touch app/templates/signup.html
touch app/templates/dashboard.html

echo "Folder structure created successfully!"