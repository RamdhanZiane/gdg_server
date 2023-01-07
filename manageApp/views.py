from flask import Blueprint, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return jsonify({'body':'hello world'})


# ROUTES

@views.route('/favicon.ico')
def favicon():
    # return send_from_directory(STATIC_PATH , 'favicon.ico' , mimetype='image/vnd.microsoft.icon')
    pass
	


@views.route('/', methods=['GET'])
def base():
	# return redirect(FIRST_URL)
    pass


	
@views.route('/member/add_member', methods=['GET'])
@login_required
def add_member():
	pass



@views.route('/member/extra_add', methods=['GET'])
@login_required
def extra_add():
	pass



@views.route('/member/delete_member', methods=['GET'])
@login_required
def delete_member():
	pass




@views.route('/member/update_member', methods=['GET'])
@login_required
def update_member():
	pass



@views.route('/member/get_all_members', methods=['GET'])
def get_all_members():
	#filter_by
	#filter_by_name
	#filter_by_departement_name
	
	#sort_by
	#sort_by_role
	#sort_by_season
	
	pass



@views.route('/member/<member_id>', methods=['GET'])
def member(member_id):
	pass




@views.route('/depart/get_all_departments', methods=['GET'])
def get_all_departments():
	pass



@views.route('/depart/<department_id>', methods=['GET'])
def department(department_id):
	pass

