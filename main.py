from flask import session , abort , Flask , Blueprint, render_template, redirect, request, jsonify , send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_sessionstore import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from xmlrpc.client import INTERNAL_ERROR
from werkzeug.exceptions import HTTPException


from config import *




login_manager = LoginManager()
mysql = SQLAlchemy()
cache = Cache()






def CreateApp():
	app = Flask(__name__ , 
				static_folder=STATIC_PATH, 
				static_url_path=STATIC_URL,
				template_folder=TEMPLATE_PATH)
	
	
	app.config.update(APP_CONFIG_DATA)
		
		
	login_manager.init_app(app)
	mysql.init_app(app)
	cache.init_app(app) 
	Session(app)
	
	
	return app


	
app = CreateApp()



from routes import *





# set login manager
@login_manager.user_loader
def load_user(id): 
	return Accounts.query.get(id)



@login_manager.unauthorized_handler
def unauthorized_callback():
	if request.method == 'GET':
		return redirect(FIRST_URL)
	else :
		return 'you are not authenticated'




'''@app.errorhandler(Exception)
def handle_exception(e):
	data = get_data()
	#data.update(SERVER_DATA)

	if isinstance(e, HTTPException):
		# e.code
		# e.name
		# e.description
		pass
		
	else :
		pass


	if request.method == 'GET' :
		return 
	
	return '''






@app.after_request
def add_header(response):
	mysql.session.close()
	
	return response



with app.app_context():
	cache.clear()
	
	mysql.create_all() 



if __name__ == '__main__':
	
	app.run(host=IP_ADDRESS , port=PORT , ssl_context=(SSL_CERTIFICATE_PATH , SSL_KEY_PATH))#

