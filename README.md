![App logo](app/static/img/app_logo_for_readme.png)

# Budget - a Finance Management App!

# Installation

#### Create virtual environment in project's root directory:

```Shell
python -m venv venv
```

#### Activate the virtual environment:

- ##### For Linux / Mac:

  ```Shell
  source venv/bin/activate
  ```

- ##### For Windows:
  ```Shell
  source venv/Scripts/activate
  ```

#### Install the required packages:

```Shell
pip install -r requirements.txt
```

## Running

##### [1] Set the environment variables:

```Shell
export FLASK_APP=budget.py
export FLASK_DEBUG=1
```

###### You can also export a database URL and a secret key, but it is not necessary:

```Shell
export DEV_DATABASE_URL="sqlite:///$(pwd)/budget-db.sqlite" # You can use a full path to your database file.
export SECRET_KEY="{YOUR SECRET KEY}"
```

#### [2] Initial setup:

##### Create the migrations' folder:

```Shell
flask --app budget.py db init # It needs to be run only once, at the beginning.
````

##### Apply migrations:

```Shell
flask --app budget.py db upgrade # If run for the first time, it will create an empty database (without tables).
```

##### You can also enter the flask shell:
###### It is used to create database tables, add entries to them, and more.

```Shell
flask --app budget.py shell
```

###### Example usage:

```python
>>> from budget import db
>>> db.create_all() # It will create the tables (empty) in the database.
>>> exit()
```

##### [3] Run the flask app (development server) from the terminal:

```Shell
flask run
```

##### Alternative without setting environment variables:
```Shell
flask --app budget.py --debug run # You can also run the app from the budget.py file in PyCharm.
```

## Software dependencies

[Flask](https://flask.palletsprojects.com) - a web development framework that is known for its lightweight and modular design. It has many out-of-the-box features and is easily adaptable to specific requirements.

[Jinja2](https://jinja.palletsprojects.com) - a fast, expressive, extensible templating engine. Special placeholders in the template allow writing code similar to Python syntax. Then the template is passed data to render the final document.

[SQLAlchemy](https://www.sqlalchemy.org) - the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

[Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com) - an extension for Flask that adds support for SQLAlchemy to the app. It simplifies using SQLAlchemy with Flask by setting up common objects and patterns for using those objects, such as a session tied to each web request, models, and engines. This extension does not change how SQLAlchemy works or is used.

[WTForms](https://wtforms.readthedocs.io) - a flexible forms validation and rendering library for Python web development. It can work with whatever web framework and template engine that is chosen. It supports data validation, CSRF protection, internationalization (I18N), and more.

[Flask WTF](https://flask-wtf.readthedocs.io) - simple integration of Flask and WTForms, including CSRF, file upload, and reCAPTCHA.

For the full list of software dependencies see [requirements.txt](requirements.txt).

## Latest releases

**v1.0.0** (2023-10-08)

## API references

None

## [License](LICENSE)

The MIT License (MIT)

Copyright (c) 2023 Code Academy
