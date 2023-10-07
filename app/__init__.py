from config import config
from flask import Flask
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

db = SQLAlchemy()


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	login_manager.init_app(app)

	db.init_app(app)

	# TODO: attach routes and custom error pages here

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	return app

# # Create the app.
# app = Flask(__name__,
# 			template_folder='budget_app/templates',
# 			static_folder='budget_app/static')
#
# # Configure the app.
# current_dir = os.path.join(os.path.dirname(__file__),
# 						   'database.db')  # !!! Sukurtas kintamasis, kuris nurodo dabartinį katalogą.
# db_uri = 'sqlite:///' + current_dir  # !!! Sukurtas kintamasis, kuris nurodo duomenų bazės URI.
# app.config['SQLALCHEMY_DATABASE_URI'] = db_uri  # !!! Pakeista, kad būtų nurodytas duomenų bazės kelias.
#
# app.config['TEMPLATES_AUTO_RELOAD'] = True  # This is for debugging purposes.
# app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# # Configure the login manager.
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# login_manager.init_app(app)
#
# class Base(DeclarativeBase):
# 	pass
#
#
# db = SQLAlchemy(model_class=Base)
#
#
# # Configure the migration engine.
# migrate = Migrate(app, db)
# db.init_app(app)
#
# # Import blueprints.
#
# from budget_app.auth.auth import auth as auth_blueprint
#
# app.register_blueprint(auth_blueprint)
#
# from budget_app.main.main import main as main_blueprint
#
# app.register_blueprint(main_blueprint)
#
# # Import models.
# from models import User
#
#
# # Create the user loader function.
# @login_manager.user_loader
# def load_user(user_id):
# 	return User.query.get(int(user_id))
#
#
# with app.app_context():
# 	db.create_all()
#
# if __name__ == '__main__':
# 	app.run(debug=True)
