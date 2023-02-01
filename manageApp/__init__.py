from flask import Flask , jsonify
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

from config import *


mysql = SQLAlchemy()
login_manager = LoginManager()


def create_app():
	app = Flask(__name__)
	app.config.update(APP_CONFIG_DATA)

	mysql.init_app(app)

	from .views import views
	from .auth import auth
	from .member import member

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/auth')
	app.register_blueprint(member, url_prefix='/member')


	from .models import Members

	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)


	@login_manager.user_loader
	def load_user(member_id):
		return Members.query.get(member_id)



	@login_manager.unauthorized_handler
	def unauthorized_callback():
		data = {}
		data['code'] = 400
		data['message'] = 'you are not authenticated.'
		
		return jsonify(data)


	return app


# def create_database(app):
#     if not path.exists('manageApp/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')