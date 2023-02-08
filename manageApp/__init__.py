from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from os import path
from flask_login import LoginManager
from datetime import date, datetime
import json

DB_NAME = "database.db"
db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.strftime("%d/%m/%Y")
        return json.JSONEncoder.default(self, obj)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'App_Secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # app.json_encoder = CustomJSONEncoder
    db.init_app(app)
    ma.init_app(app)

    from .views import views
    from .auth import auth
    from .member import member
    from .models import Members

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(member, url_prefix='/member')

    with app.app_context():
        db.create_all()

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