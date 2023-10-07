export DATABASE_URL=sqlite:///database.db

export SECRET_KEY="LPhW~G@?b{*k'8;&MQbT=[~(M-VzDMKk.rP$kAnK"

flask --app budget.py run --debug

flask --app budget.py db init

flask --app budget.py db upgrade

flask --app budget.py shell
>>> from budget import db
>>> db.create_all()
>>> exit()
