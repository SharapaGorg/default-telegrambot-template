# Default layout for Telegram bot

### I am developing this repo so that anyone can use it as a framework or just find something useful in my structure or technology stack

## Features

Features of this repo as framework:
 - convenient and flexible structure
 - proven technology stack
 - logging data in the database
 - automatic update of user data (new user / last message with the bot)
 - division of functions by permissions (ordinary user / moderator)
 - well-thought-out database structure with the necessary tables (users/moderators/logs)

## Quick start

Clone directory

```git clone https://github.com/SharapaGorg/aiogram-framework```

Go to cloned directory, make virtual environment, activate it and install requirements

```cd aiogram-framework``` 

```python -m venv env``` ```env\Scripts\activate```

```pip install -r requirements.txt```

Setup config.py

```python
TOKEN = "YOUR TOKEN"
RESERVE_TOKEN = "YOUR RESERVE TOKEN"
```

Launch app

```python main.py```

## Structure
```
aiogram-framework
│
├── database
│ ├── __init__.py
│ ├── base (database)
│ └── ...database interaction files...
│
├── handlers
│ ├── __init__.py
│ └── ...handlers (bot functions)...
│
├── static
│ ├── __init__.py
│ ├── commands.py
│ ├── texts.py
│ └── ...your custom static files...
│
├── widgets
│ ├── __init__.py
│ ├── button.py
│ ├── button_slider.py
│ └── ...your custom widgets...
│
├── .gitignore
├── app.log
├── config.py
├── controller.py
├── main.py
├── models.py (database tables structures)
├── README.md
├── requirements.txt
└── utils.py
```

#### Database

This directory contains files for interacting 
with the database, each file has a name corresponding to the name of the table

P.S SQlAlchemy is used to interact with the database

#### Handlers

This Directory contains files with functions called by bot commands. 
In this template, the files are divided by access level, that is, commands for ordinary users - users.py, for moderators - moders.py, and so on. 
For convenience, you can separate files by themes of commands or anything else.

#### Static

This contains files containing static information. This template contains texts.py - 
the bot's replicas that it sends and commands.py - the list of commands it uses

In the future, it is supposed to store most of this information in 
a database for convenience and the ability to change from a remote web interface or something else.

#### Widgets

Widgets - by analogy with ui widgets - interface components

This template contains the following widgets:
* button
* button slider
* calendar
* questions chain

I think it makes no sense to explain what each of the widgets does, if it is not clear, just check for yourself

#### controller

Base classes:
* sqlalchemy class (database interaction object)
* aiogram bot object
* aiogram dispatcher object
* logger object
