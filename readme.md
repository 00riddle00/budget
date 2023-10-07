set DATABASE_URL=sqlite:///database.db

set SECRET_KEY="b'\x8d\x9a\x12\xf2\xe1\x1b\xaa\x08\x8b\xe2P\x1e\xf7\xfc\xee=\xe7\x19\x00\xc2\x99Q\xae%D\xcf\x85\xae:\xd3\t\xa6'"

flask --app budget.py run --debug

flask --app budget.py db init

flask --app budget.py db upgrade

flask --app budget.py shell
>>> from budget import db
>>> db.create_all()
>>> exit()
