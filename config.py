


IP_ADDRESS = '192.168.100.10'
PORT = '7000'


STATIC_URL = '/static'
FIRST_URL = '/home'



EXECUTE_PATH = os.getcwd()


STATIC_PATH = EXECUTE_PATH + "/static_folder"
TEMPLATE_PATH = EXECUTE_PATH + "/templates_folder"



SSL_KEY_PATH = EXECUTE_PATH + "/ssl_key.key"
SSL_CERTIFICATE_PATH = EXECUTE_PATH + "/ssl_certificate.crt"  



MYSQL_SERVER = 'mysql+pymysql://root:password@192.168.100.20:3306'
MYSQL_DATABASE = MYSQL_SERVER + '/test'



SECRET_KEY = 'secret-key-goes-here'



APP_CONFIG_DATA = {
    'SECRET_KEY' : SECRET_KEY,
	'DEBUG' : True ,
	
	'SQLALCHEMY_DATABASE_URI' : MYSQL_DATABASE,
	'SQLALCHEMY_TRACK_MODIFICATIONS' : False ,
	
	'CACHE_TYPE' : 'SimpleCache' ,
	'CACHE_DEFAULT_TIMEOUT' : 0 ,
}

