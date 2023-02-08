from manageApp import create_app , mysql

from config import *

app = create_app()


with app.app_context():
	mysql.create_all() 
	
	
if __name__ == '__main__':
    app.run(debug=True)