#!/usr/bin/env python

###
#-------------------------------------------------------------------------------
# manage.py
#-------------------------------------------------------------------------------
#
# Author:       Alwin Tareen
# Created:      Apr 27, 2022
#
# Venv setup:       python3 -m venv venv
# Venv activation:  source venv/bin/activate
# Check Django:     python -m django --version
# Install Django:   pip install django
#
# Project creation: django-admin startproject <projectname>
# App creation:     python manage.py startapp <appname>
#
# Migrations:   python manage.py makemigrations
# Migrate:      python manage.py migrate
# Superuser:    python manage.py createsuperuser
# Run Django:   python manage.py runserver
#
# Login:        heroku login
# Migrations:   heroku run python manage.py makemigrations
# Migrate:      heroku run python manage.py migrate
# Superuser:    heroku run python manage.py createsuperuser
#
# Conclusion:   deactivate
#
#--------------------------------------
# Deployment notes
# https://dev.to/jonatanvm/how-to-deploy-a-django-app-on-heroku-in-less-than-5-minutes-4m7n
#--------------------------------------

# Postgres database setup
#------------------------
# Note: the sqlite database has been switched to postgresql on the localhost
# by exporting the following environment variable in ~/.bashrc:
# export DATABASE_URL="postgres://altareen:password@localhost/<databasename>"
# source ~/.bashrc
#
# Install postgres: sudo apt install postgresql
# Create a database: sudo -u postgres createdb <databasename>
# Log in to postgres: sudo -u postgres psql
# Create a user: CREATE USER altareen WITH PASSWORD '<password>';
# Create privileges: ALTER USER altareen CREATEDB;
# Grant privileges: GRANT ALL PRIVILEGES ON DATABASE <databasename> TO altareen;
# Quit postgres: \q
#
# Log in to Postgres as altareen: psql -U altareen -h localhost <databasename>

# Heroku setup
#-------------
# Install heroku CLI: sudo curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
# heroku login
# heroku create codingdjango
# In Heroku, Configure Add-ons, then add a Postgres database
# heroku config:set SECRET_KEY='very-long-existing-secret-key-from-settings.py-file' -a codingdjango
# In codingdjango/settings.py, add the following secret key statement:
# SECRET_KEY = os.getenv('SECRET_KEY', 'change-in-production')
# Remove the existing SECRET_KEY value from the settings.py file.

# Required additions to settings.py
#----------------------------------
# In codingdjango/settings.py, add the following import statements at the top:
# import django_on_heroku
# import dj_database_url
# import os
# from decouple import config

# In codingdjango/settings.py, add the following to INSTALLED_APPS:
# INSTALLED_APPS = ['django.contrib.humanize',
# 'crispy_forms',
# 'taggit',
# ...
# ]

# In codingdjango/settings.py, add the following whitenoise statement to MIDDLEWARE:
# MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware',
# ...
# ]

# In codingdjango/settings.py, add the following to TEMPLATES, 'DIRS':
# TEMPLATES = [
# ...
# 'DIRS': [os.path.join(BASE_DIR, 'templates')],
# ...
# ]

# In codingdjango/settings.py, add the following for Postgres database integration:
# DATABASES = {
#     'default': dj_database_url.config(
#         default=config('DATABASE_URL')
#     )
# }
# Note: remember to comment out the existing sqlite3 database statement.

# In codingdjango/settings.py, add the following static statements
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# In codingdjango/settings:py, add the following for django_on_heroku:
# django_on_heroku.settings(locals(), staticfiles=False, allowed_hosts=False)

# At the bottom of codingdjango/settings.py, add the following condition:
# if "DYNO" in os.environ:
#    STATIC_ROOT = 'static'
#    ALLOWED_HOSTS = ['codingdjango.herokuapp.com']
#    DEBUG = False
#
# Specify a Python version of 3.8.13, because the later versions are problematic:
#----------------------------------------------------------------------------
# Create the following file:
# echo python-3.8.13 > runtime.txt

# Setup git integration:
#-----------------------
# Create a .gitignore file with the following contents:
# venv/
# __pycache__/
# db.sqlite3      

# Initialize the repository for heroku
#-------------------------------------
# git init
# heroku git:remote -a codingdjango

# Initialize the repository for github
#-------------------------------------
# Log on to github.com, create a new repository, name it codingdjango, then
# follow the command statements that appear.

# Install Requirements via pip
#-----------------------------
# pip install whitenoise
# pip install django-on-heroku
# pip install gunicorn
# pip install python-decouple
# pip install django-crispy-forms
# pip install django-taggit
# pip freeze > requirements.txt

# Additional files
#-----------------
# In the same directory as manage.py, create a templates/ folder with the following:
# templates/
#  |-- base_bootstrap.html
#  |-- registration/
#       |-- login.html
#
# In the same directory as manage.py, create a Procfile:
# echo web: gunicorn codingdjango.wsgi --log-file - > Procfile

# Push code to the heroku repository:
#------------------------------------
# git add .
# git commit -m "deploy codingdjango"
# git push heroku main

# Push code to the github repository:
#------------------------------------
# git add .
# git commit -m "deploy codingdjango"
# git push origin main
#
##

"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codingdjango.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
