[![Build Status](https://travis-ci.com/rainchen/flask-app-demo.svg?branch=master)](https://travis-ci.com/rainchen/flask-app-demo)

## Summary

A flask boilerplate demo for using flask-app

## Install dependencies 

- Run `pip install pipenv`
- Run `pipenv install --dev`

## Config

- `cp .env.sample .env`
- Update the `.env` file with the respective variables 

## Activate Pipenv shell

```
$ pipenv shell

# call flask CLI in the shell
$ flask --version
Python 3.7.7
Flask 1.1.2
Werkzeug 1.0.1
```

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

## Improve Python Code Quality

### Run linter

run linter

```
$ flask dev lint
```

run linter and generate html report

```
$ flask dev lint --html-report=tmp/dev/report/pylint-report.html
```

config lowest lint score, useful for CI

```
$ flask dev lint --lowest-score=8.0
# $? will be none-zero if pylint_score is lower then lowest_score
```

### Run formatter

reformats codes to follow the Google Python Style Guide

```
$ flask dev format

Run formatter

No changes needed.
# $? will be non-zero if some files need to be changed
```

format codes and make changes to files in place

```
$ flask dev format --in-place

Run formatter
[NOTICE]Make changes to files in place!
```

### Run security audit

```
$ flask dev security_audit
# $? will be non-zero if found security issues
```

run security audit and generate html report

```
$ flask dev security_audit --html-report=tmp/dev/report/bandit-report.html
```


## Package management

manage packages with pipenv and Pipfile

### Show installed packages

```
# displays currently-installed dependency graph information in Pipfile.lock
$ pipenv graph

# list required packages in requirements format
$ pipenv run pip freeze
```

### Add a new package

```
$ pipenv install [--dev] <package>~=major.minor
# e.g.: 
$ pipenv install --dev pylint-report~=0.1.8
```

### Upgrade a package

```
# upgrade a package in Pipfile
$ pipenv install --keep-outdated [--dev] <package>~=x.y.z
# e.g.:
$ pipenv install --keep-outdated --dev pylint-report==0.1.8

# upgrade a package and auto update Pipfile.lock
$ pipenv update --keep-outdated <pkg>
# e.g.:
$ pipenv update --keep-outdated pylint-report
```

just update Pipfile.lock for the  new package requirements

```
# records the new requirements to the Pipfile.lock file
# pipenv lock --keep-outdated
```

*NOTES: DO NOT update Pipfile.lock manually, should always update it by running `pipenv` command*

### Remove a package

```
$ pipenv uninstall --keep-outdated <package>
```
