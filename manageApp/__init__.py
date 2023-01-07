from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'App_Secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')

    from .models import Members

    # create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Members.query.get(id)


    
    # set login manager
    @login_manager.user_loader
    def load_user(id): 
        # return Accounts.query.get(id)
        pass



    @login_manager.unauthorized_handler
    def unauthorized_callback():
    	# if request.method == 'GET':
    	#     return redirect(FIRST_URL)
        # else:
    	#     return 'you are not authenticated'
        pass


    return app


# def create_database(app):
#     if not path.exists('manageApp/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')