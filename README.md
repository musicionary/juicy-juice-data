# Juicy Juice Data Analysis

## Quick Start
To visit a live version of the site, please visit: https://juicy-juice-data.herokuapp.com/

### First Steps
```sh
$ git clone https://github.com/musicionary/juicy-juice-data.git my_project_folder
$ cd my_project_folder
```

### Virtual Environment Setup
```sh
$ pip install virtualenv
# this project uses python 3.6, and this determines the python interpreter.
$ virtualenv -p /usr/bin/python3.6 my_project
$ source my_project/bin/activate
$ pip install -r requirements.txt
# to deactivate the virtualenv
$ deactivate
```

### Or, if you are using virtualenvwrapper:
```sh
$ pip install virtualenvwrapper
$ export WORKON_HOME=~/.virtualenvs
$ source /usr/local/bin/virtualenvwrapper.sh
$ mkvirtualenv my_project
$ workon my_project
$ pip install -r requirements.txt
# to deactivate the virtualenv
$ deactivate
```

### Set up the Database
-- This project uses PostgreSQL

```sh
# For Mac
$ brew install postgres
# For Linux
$ apt-get install postgresql-9.4
```

(For Windows, I recommend this post on SO for setting up PostgreSQL https://stackoverflow.com/questions/7086654/installing-postgres-on-windows-for-use-with-ruby-on-rails#answer-7133391)

### Set up Migrations

```sh
# start the postgres server
$ postgres
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

### Seed the database

```sh
$ python manage.py seed
```

### Run

Run each in a different terminal window...

```sh
# the app
$ python manage.py runserver
```

To view the full list of Juicy Juicy products visit:
localhost:5000/

To see a JSON representation of the total number of products, calories, and calories per ounce visit:
localhost:5000/api/v1/totals


License
-------

MIT License. Copyright &copy; 2017 "Chip Carnes"
