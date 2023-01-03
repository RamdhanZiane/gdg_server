from xmlrpc.client import INTERNAL_ERROR
from flask import session , abort , Flask , Blueprint, render_template, redirect, request, jsonify , send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_socketio import SocketIO , emit , Namespace, send, join_room, leave_room
from flask_sessionstore import Session
from flask_mail import Mail, Message
# from flask_migrate import Migrate

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from werkzeug.exceptions import HTTPException
from functools import wraps





IP_ADDRESS = '192.168.100.10'
PORT = '7000'


STATIC_URL = '/static'
FIRST_URL = '/home'




# SERVER PATHS

EXECUTE_PATH = os.getcwd()

TEMPLATE_PATH = EXECUTE_PATH + "/templates_folder"
STATIC_PATH = EXECUTE_PATH + "/static_folder"



SSL_KEY_PATH = EXECUTE_PATH + "/ssl_key.key"
SSL_CERTIFICATE_PATH = EXECUTE_PATH + "/ssl_certificate.crt"  



# DATABASE SERVER 

MYSQL_SERVER = 'mysql+pymysql://root:rmzmrrmzmr@192.168.100.20:3306'

MYSQL_DATABASE = MYSQL_SERVER + '/oar'





MAIN_EMAIL_ACCOUNT = 'ramzi16.jhon.10@gmail.com'
MAIN_EMAIL_PASSWORD = ''


SECRET_KEY = 'secret-key-goes-here'



APP_CONFIG_DATA = {
    'SECRET_KEY' : SECRET_KEY,
	'DEBUG' : True ,
	
	
	'SQLALCHEMY_DATABASE_URI' : MYSQL_DATABASE,
	'SQLALCHEMY_TRACK_MODIFICATIONS' : False ,
	
	'CACHE_TYPE' : 'SimpleCache' ,
	'CACHE_DEFAULT_TIMEOUT' : 0 ,
	
	'MAIL_SERVER' : 'smtp.gmail.com',
    'MAIL_PORT' : 465,
	'MAIL_USERNAME' : MAIN_EMAIL_ACCOUNT,
	'MAIL_PASSWORD' : MAIN_EMAIL_PASSWORD,
	'MAIL_USE_TLS' : False,
	'MAIL_USE_SSL' : True
}








# set extentions
login_manager = LoginManager()
mysql = SQLAlchemy()
cache = Cache()
mail = Mail()
# migrate = Migrate()







def CreateApp():
	app = Flask(__name__ , 
				static_folder=STATIC_PATH, 
				static_url_path=STATIC_URL,
				template_folder=TEMPLATE_PATH)
	
	
	# sqlalchemy config
	app.config.update(APP_CONFIG_DATA)
		
		
	# init extentions
	login_manager.init_app(app)
	mysql.init_app(app)
	#migrate.init_app(app, mysql)
	cache.init_app(app) 
	mail.init_app(app) 
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

	#socketio.run(app , host="192.168.100.7" , port=7000 , certfile=SSL_CERTIFICATE_PATH , keyfile=SSL_KEY_PATH)
	
