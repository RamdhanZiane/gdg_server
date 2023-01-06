from main import *
from modules import *





main_route = Blueprint('main_route', __name__) 




# ROUTES

@main_route.route('/favicon.ico')
def favicon():
    return send_from_directory(STATIC_PATH , 'favicon.ico' , mimetype='image/vnd.microsoft.icon')
	


@main_route.route('/', methods=['GET'])
def base():
	return redirect(FIRST_URL)




@main_route.route('/auth/signin', methods=['GET'])
def signin():
	pass


@main_route.route('/auth/signup', methods=['GET'])
@login_required
def signup():
	pass
	
	
@main_route.route('/auth/signout', methods=['GET'])
@login_required
def signout():
	pass


	
@main_route.route('/member/add_member', methods=['GET'])
@login_required
def add_member():
	pass



@main_route.route('/member/extra_add', methods=['GET'])
@login_required
def extra_add():
	pass



@main_route.route('/member/delete_member', methods=['GET'])
@login_required
def delete_member():
	pass




@main_route.route('/member/update_member', methods=['GET'])
@login_required
def update_member():
	pass



@main_route.route('/member/get_all_members', methods=['GET'])
def get_all_members():
	#filter_by
	#filter_by_name
	#filter_by_departement_name
	
	#sort_by
	#sort_by_role
	#sort_by_season
	
	pass



@main_route.route('/member/<member_id>', methods=['GET'])
def member(member_id):
	pass




@main_route.route('/depart/get_all_departments', methods=['GET'])
def get_all_departments():
	pass



@main_route.route('/depart/<department_id>', methods=['GET'])
def department(department_id):
	pass



app.register_blueprint(main_route)
