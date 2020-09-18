[![Build Status](https://travis-ci.com/rainchen/flask-app-demo.svg?branch=master)](https://travis-ci.com/rainchen/flask-app-demo)

## Summary

A flask boilerplate demo for using flask-app

## Install dependencies 

- Run `pip install pipenv`
- Run `pipenv install --dev`

## Config

- `cp .env.sample .env`
- Update the `.env` file with the respective variables 

## Run db migration

- Run `flask create-db` to create database
- Run `flask db upgrade` to create table and apply migrations

## Check routes

- Run `flask routes`

```
Endpoint    Methods    Rule
----------  ---------  -----------------------
static      GET        /static/<path:filename>
user.users  GET, POST  /users/
user.users  GET        /users/<int:user_id>
```

## Run test

- Run `flask test`

## Run shell

- Run `flask shell`

```
>>> from api.models import *
>>> User.create(username='admin', first_name='Ming', last_name='Li')

>>> User.query.count()
1
```

## Run server in development mode

- Run `flask run`

```
 * Serving Flask app "manage.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 621-366-433
```

## Run server in production mode using WSGI server

PENDING
