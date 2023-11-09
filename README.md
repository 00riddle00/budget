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

---------------------------------------

## Deployment: First steps (2023-11-10)

Let's say we have root access to an **Ubuntu 22.04 LTS** server with an IP **207.154.242.27**, and the user we would create will be called **riddle**.

`ssh root@207.154.242.27`

`sudo useradd -m riddle`

`sudo passwd riddle`

`nano /etc/sudoers`:

```
# User privilege specification
root    ALL=(ALL:ALL) ALL
riddle  ALL=(ALL:ALL) ALL
```

`chsh -s /bin/bash riddle`

`exit`

`ssh riddle@207.154.242.27`

`sudo apt update && sudo apt upgrade` (After the upgrade, it will be suggested that a new kernel version could be booted, the prompt will appear on which services to restart - select default options and select "OK").

`sudo reboot` (Needed for booting a new kernel version. You will be logged out of the server. Wait a little bit, and connect to the server again).

`ssh riddle@207.154.242.27`

`sudo apt install git`

`cd /home/riddle`

`git clone <repository with budget project, with the root directory called "budget"> .`

`python3 -V`

`sudo apt install python3-pip python3-venv`

## Deployment with Nginx, Gunicorn and Supervisor (2023-11-10)

`python3 -m venv budget/venv`

`cd budget/`

`source venv/bin/activate`

`pip install -r requirements.txt`

`rm budget-dev.sqlite3` (If you have a database file in Git repo and would like to remove it).

`flask --app budget.py db init`

`flask --app budget.py db upgrade`

`flask --app budget.py shell`

```
>>> from budget import db
>>> db.create_all() # It will create the tables (empty) in the database.
>>> exit()
```

`export FLASK_APP=budget.py`

`flask run --host=0.0.0.0`

`(In your browser, go to 207.154.242.27:5000 - the application works, but in DEBUG mode)`

`Ctrl + c`

`sudo apt install nginx`

`pip install gunicorn`

`pip freeze > requirements-prod.txt`

`sudo rm /etc/nginx/sites-enabled/default`

`sudo nano /etc/nginx/sites-enabled/flask_app`:

```
server {
    listen 80;
    server_name 207.154.242.27;

    location /static {
        alias /home/riddle/budget/app/static;
    }

    location / {
        proxy_pass http://localhost:5000;
        include /etc/nginx/proxy_params;
        proxy_redirect off;
    }
}
```

`sudo systemctl restart nginx`

`(In your browser, go to 207.154.242.27 - the application doesn't work yet, you will get an Nginx error)`

`nano /home/riddle/budget/wsgi.py`:

```
from budget import app

if __name__ == "__main__":
     app.run()
```

`nproc --all` (it will most likely show "1" - that 1 processor core is available).

`gunicorn --bind 0.0.0.0:5000 wsgi:app` (3 = 2 * {number of cores} + 1).

`(In your browser, go to 207.154.242.27 - the application works, but if we stop the gunicorn process, it will stop. For that, we need to install and configure Supervisor)`

`Ctrl + c`

`sudo nano /etc/supervisor/conf.d/budget.conf`:

```
[program:budget]
directory=/home/riddle/budget
command=/home/riddle/budget/venv/bin/gunicorn --bind 0.0.0.0:5000 wsgi:app
user=riddle
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/budget/budget.err.log
stdout_logfile=/var/log/budget/budget.out.log
```

`sudo mkdir -p /var/log/budget`

`sudo touch /var/log/budget/budget.err.log`

`sudo touch /var/log/budget/budget.out.log`

`sudo supervisorctl reload`

`(In your browser, go to 207.154.242.27 - the application works)`

`sudo nano /etc/nginx/nginx.conf`:

```
http {

        ##
        # Basic Settings
        ##

        sendfile on;
        tcp_nopush on;
        types_hash_max_size 2048;
        client_max_body_size 5M;    <--- add this line (increasing the limit of uploaded photo size)
        # server_tokens off;

        ...
        ...
        ...
}
```

`sudo systemctl restart nginx`

`(In your browser, go to 207.154.242.27 - the application works)`

## Deployment with Apache (2023-11-10)

`sudo apt install apache2 libapache2-mod-wsgi-py3`

`cd /var/www/`

`sudo rm -rf html/`

`sudo cp -r /home/riddle/budget .`

`sudo chown -R riddle:riddle /var/www`

`python3 -m venv budget/venv`

`cd budget/`

`source venv/bin/activate`

`pip install -r requirements.txt`

`rm budget-dev.sqlite3` (If you have a database file in Git repo and would like to remove it).

`flask --app budget.py db init`

`flask --app budget.py db upgrade`

`flask --app budget.py shell`

```
>>> from budget import db
>>> db.create_all() # It will create the tables (empty) in the database.
>>> exit()
```

`export FLASK_APP=budget.py`

`flask run --host=0.0.0.0`

`(In your browser, go to 207.154.242.27:5000 - the application works, but in DEBUG mode)`

`cd /etc/apache2/sites-enabled/`

`sudo nano flask_app.conf`:

```
<VirtualHost *:80>
    ServerName 207.154.242.27
    ServerAdmin tomasgiedraitis@gmail.com

    LogLevel warn
    ErrorLog ${APACHE_LOG_DIR}/flask-error.log
    CustomLog ${APACHE_LOG_DIR}/flask-access.log combined

    WSGIDaemonProcess budget processes=1 threads=15 python-path=/var/www/budget python-home=/var/www/budget/venv
    WSGIProcessGroup budget
    WSGIScriptAlias / /var/www/budget/wsgi.py

    <Directory /var/www/budget>
        Require all granted
    </Directory>
</VirtualHost>
```

`sudo mv 000-default.conf 000-default.conf.backup`

`cd /var/www/`

`nano budget/wsgi.py`:

```
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/budget/")

from budget import app as application
```

`sudo chown -R www-data:www-data /var/www/budget`

`sudo systemctl restart apache2`

`(In your browser, go to 207.154.242.27 - the application works)`
