from main import *
from mysql_databases_modules import *




def GetUserData(user_id) :
	x = {}
	
	user = Users.query.filter_by(user_id=user_id).first()
	if not(user) :
		return 404
	
	#if current_user.is_authenticated :
	x['user_id'] = user.user_id
	x['created_time'] = user.created_time
	
	return x




main_route = Blueprint('main_route', __name__) 




# ROUTES

@main_route.route('/favicon.ico')
def favicon():
    return send_from_directory(STATIC_PATH , 'favicon.ico' , mimetype='image/vnd.microsoft.icon')
	


@main_route.route('/', methods=['GET'])
def base():
	return redirect(FIRST_URL)



@main_route.route('/login', methods=['GET' , 'POST'])
def login():
	pass


@main_route.route('/logout', methods=['GET'])
@login_required
def logout():
	pass


@main_route.route('/add_admin', methods=['POST'])
@login_required
def add_admin():
	pass


@main_route.route('/delete_admin', methods=['POST'])
@login_required
def delete_admin():
	pass


@main_route.route('/add_users', methods=['GET' , 'POST'])
@login_required
def add_users():
	pass



@main_route.route('/home', methods=['GET'])
def home():
	pass


@main_route.route('/user/<user_id>', methods=['GET'])
def user(user_id):
	pass



app.register_blueprint(main_route)
