from manageApp import create_app , db

from config import *

app = create_app()


# with app.app_context():
# 	app.create_all() 
	
	
if __name__ == '__main__':
    app.run(debug=True)