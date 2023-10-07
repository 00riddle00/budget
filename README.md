
### Export environment variables

```bash
export DATABASE_URL="sqlite:///$(pwd)/budget-db.sqlite" # You can use a full path to your database file.
export SECRET_KEY="LPhW~G@?b{*k'8;&MQbT=[~(M-VzDMKk.rP%kAnK"
```

### Create the migrations folder

```bash
flask --app budget.py db init # It needs to be run only once, at the beginning.
````

### Apply migrations
```bash
flask --app budget.py db upgrade # If run for the first time, it will create an empty database (without tables).
```

### Enter the flask shell and create the tables

`flask --app budget.py shell`

```python
>>> from budget import db
>>> db.create_all() # It will create the tables (empty) in the database.
>>> exit()
```

### Run the flask app from the terminal

```bash
flask --app budget.py run --debug # You can also run the app from the budget.py file in PyCharm.
```
