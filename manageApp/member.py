from flask import Blueprint, request, flash, jsonify
from flask_login import login_required, current_user
from . import db as mysql
import json
from .models import Members, Activities, Events, Departments, USERS_ROLES, EVENTS_ROLES


member = Blueprint('member', __name__)




def is_admin(user_id) :
	is_admin = Members.query.filter(Members.member_id==user_id,
									mysql.or_(Members.role=='leader',Members.role=='hr')).first()
	if is_admin:
		return True
		
	return False
	



# ROUTES
	
@member.route('/add_member', methods=['GET'])
@login_required
def add_member():	
	data = {}
	
	
	if not is_admin(current_user.member_id) :
		data['code'] = 400
		data['message'] = 'you are not allowed to perform this action'
		return jsonify(data)
		
		
	ALLOWED_ROLES = ['comanager' , 'member' , 'alumni']

	full_name = request.form.get('full_name')
	email = request.form.get('email')
	joined_time = request.form.get('joined_time')
	discord_id = request.form.get('discord_id')
	role = request.form.get('role')
	
	user = Members.query.filter(Members.email==email).first()
	if user:
		data['code'] = 400
		data['message'] = 'Member exists.'
		return jsonify(data)
	
	if not role in ALLOWED_ROLES :
		data['code'] = 400
		data['message'] = 'role not allowed.'
		return jsonify(data)
		
		
	new_user = Members(email=email, 
					first_name=first_name, 
					joined_time=joined_time,
					discord_id=discord_id,
					role=role)
	mysql.session.add(new_user)
	mysql.session.commit()
	
	data['code'] = 200
	data['message'] = 'Member added successfully.'
	return jsonify(data)



@member.route('/extra_add', methods=['GET'])
@login_required
def extra_add():
	data = {}
	
	if not is_admin(current_user.member_id) :
		data['code'] = 400
		data['message'] = 'you are not allowed to perform this action'
		return jsonify(data)
		
		
	pass




@member.route('/<member_id>', methods=['GET'])
def get_member(member_id):
	data = {}
	
	user = Members.query.filter(Members.member_id==member_id).first()
	if not user:
		data['code'] = 400
		data['message'] = 'Member does not exist.'
		return jsonify(data)
	
	data['member_id'] = user.member_id
	data['full_name'] = user.full_name
	data['email'] = user.email
	data['joined_time'] = user.joined_time
	data['discord_id'] = user.discord_id
	data['role'] = user.role
	data['member_activities'] = []
	data['member_events'] = []
	data['member_departments'] = []
	
	for activity in user.member_activities :
		x = {}
		x['activity_id'] = activity.activity_id
		x['activity_name'] = activity.activity_name
		x['created_time'] = activity.created_time
		data['member_activities'].append(x)
	
	for event in user.member_events :
		x = {}
		x['event_id'] = event.event_id
		x['event_title'] = event.event_title
		x['started_time'] = event.started_time
		x['ended_time'] = event.ended_time
		x['event_role'] = event.event_role
		data['member_events'].append(x)
	
	for department in user.member_departments :
		x = {}
		x['department_id'] = department.department_id
		x['department_name'] = department.department_name
		x['is_comanager'] = department.is_comanager
		x['is_joined'] = department.is_joined
		x['joined_time'] = department.joined_time
		x['exit_time'] = department.exit_time
		data['member_departments'].append(x)
		
	data['code'] = 200
	data['message'] = 'success.'
	return jsonify(data)



@member.route('/<member_id>/delete_member', methods=['DELETE'])
@login_required
def delete_member(member_id):
	data = {}
	
	if not is_admin(current_user.member_id) :
		data['code'] = 400
		data['message'] = 'you are not allowed to perform this action'
		return jsonify(data)
		
		
	user = Members.query.filter_by(Members.member_id==member_id)
	if not user.first() :
		data['code'] = 400
		data['message'] = 'Member does not exist.'
		return jsonify(data)
	
	user.delete()
	mysql.session.commit()
	
	data['code'] = 200
	data['message'] = 'Member deleted successfully.'
	return jsonify(data)



@member.route('/<member_id>/update_member', methods=['GET'])
@login_required
def update_member(member_id):
	data = {}
	
	if not is_admin(current_user.member_id) :
		data['code'] = 400
		data['message'] = 'you are not allowed to perform this action'
		return jsonify(data)
		
	ALLOWED_ROLES = ['comanager' , 'member' , 'alumni']

	full_name = request.form.get('full_name')
	email = request.form.get('email')
	joined_time = request.form.get('joined_time')
	discord_id = request.form.get('discord_id')
	role = request.form.get('role')
	
	user = Members.query.filter(Members.member_id==member_id).first()
	if not user:
		data['code'] = 400
		data['message'] = 'Member does not exist.'
		return jsonify(data)
	
	if not role in ALLOWED_ROLES :
		data['code'] = 400
		data['message'] = 'role not allowed.'
		return jsonify(data)
		
	check_email = Members.query.filter(Members.email==email,
								Members.member_id!=member_id)
	if check_email.first() :
		data['code'] = 400
		data['message'] = 'Email already used.'
		return jsonify(data)
	
	user.full_name = full_name
	user.email = email
	user.joined_time = joined_time
	user.discord_id = discord_id
	user.role = role
	
	mysql.session.commit()
	
	data['code'] = 200
	data['message'] = 'Member updated successfully.'
	return jsonify(data)



@member.route('/<member_id>/add_activity', methods=['POST'])
@login_required
def add_member_activity(member_id):
	data = {}
	
	if not is_admin(current_user.member_id) :
		data['code'] = 400
		data['message'] = 'you are not allowed to perform this action'
		return jsonify(data)
	
	activity_id = request.form.get('activity_id')
	
	user = Members.query.filter(Members.member_id==member_id).first()
	if not user:
		data['code'] = 400
		data['message'] = 'Member does not exist.'
		return jsonify(data)
	
	activity = Activities.query.filter(Activities.activity_id==activity_id).first()
	if not activity:
		data['code'] = 400
		data['message'] = 'Activity does not exist.'
		return jsonify(data)
	
	if not activity in user.member_activities :
		user.member_activities.append(activity)
	
	mysql.session.commit()
	
	data['code'] = 200
	data['message'] = 'Activity added to member successfully.'
	return jsonify(data)



@member.route('/<member_id>/delete_activity', methods=['DELETE'])
@login_required
def delete_member_activity(member_id):
	data = {}
	
	if not is_admin(current_user.member_id) :
		data['code'] = 400
		data['message'] = 'you are not allowed to perform this action'
		return jsonify(data)
	
	activity_id = request.form.get('activity_id')
	
	user = Members.query.filter(Members.member_id==member_id).first()
	if not user:
		data['code'] = 400
		data['message'] = 'Member does not exist.'
		return jsonify(data)
	
	activity = Activities.query.filter(Activities.activity_id==activity_id).first()
	if not activity:
		data['code'] = 400
		data['message'] = 'Activity does not exist.'
		return jsonify(data)
	
	if activity in user.member_activities :
		user.member_activities.remove(activity)
	
	mysql.session.commit()
	
	data['code'] = 200
	data['message'] = 'Activity deleted from member successfully.'
	return jsonify(data)



@member.route('/<member_id>/add_event', methods=['POST'])
@login_required
def add_member_event(member_id):
	data = {}
	
	if not is_admin(current_user.member_id) :
		data['code'] = 400
		data['message'] = 'you are not allowed to perform this action'
		return jsonify(data)
	
	event_id = request.form.get('event_id')
	event_role = request.form.get('event_role')
	
	if not event_role in EVENTS_ROLES :
		data['code'] = 400
		data['message'] = 'role not allowed.'
		return jsonify(data)
		
	user = Members.query.filter(Members.member_id==member_id).first()
	if not user:
		data['code'] = 400
		data['message'] = 'Member does not exist.'
		return jsonify(data)
	
	event = Events.query.filter(Events.event_id==event_id).first()
	if not event:
		data['code'] = 400
		data['message'] = 'Event does not exist.'
		return jsonify(data)
	
	user_event = Users_Events.query.filter(Users_Events.event_id==event_id,
											Users_Events.member_id==member_id).first()
	if not user_event:
		new_user_event = Users_Events(event_id=event_id,
									member_id=member_id,
									event_role=event_role)
		mysql.session.add(new_user_event)
	
	mysql.session.commit()
	
	data['code'] = 200
	data['message'] = 'Event added to member successfully.'
	return jsonify(data)



@member.route('/<member_id>/delete_event', methods=['DELETE'])
@login_required
def delete_member_event(member_id):
	data = {}
	
	if not is_admin(current_user.member_id) :
		data['code'] = 400
		data['message'] = 'you are not allowed to perform this action'
		return jsonify(data)
	
	event_id = request.form.get('event_id')
	
	user = Members.query.filter(Members.member_id==member_id).first()
	if not user:
		data['code'] = 400
		data['message'] = 'Member does not exist.'
		return jsonify(data)
	
	event = Events.query.filter(Events.event_id==event_id).first()
	if not event:
		data['code'] = 400
		data['message'] = 'Event does not exist.'
		return jsonify(data)
	
	user_event = Users_Events.query.filter(Users_Events.event_id==event_id,
											Users_Events.member_id==member_id)
	if user_event.first():
		user_event.delete()
		
	mysql.session.commit()
	
	data['code'] = 200
	data['message'] = 'Event deleted from member successfully.'
	return jsonify(data)



@member.route('/<member_id>/add_department', methods=['POST'])
@login_required
def add_member_department(member_id):
	data = {}
	
	if not is_admin(current_user.member_id) :
		data['code'] = 400
		data['message'] = 'you are not allowed to perform this action'
		return jsonify(data)
	
	department_id = request.form.get('department_id')
	
	is_comanager = False
	if 'is_comanager' in request.form :
		is_comanager = True
		
	user = Members.query.filter(Members.member_id==member_id).first()
	if not user:
		data['code'] = 400
		data['message'] = 'Member does not exist.'
		return jsonify(data)
	
	department = Departments.query.filter(Departments.department_id==department_id).first()
	if not department:
		data['code'] = 400
		data['message'] = 'Department does not exist.'
		return jsonify(data)
	
	user_department = Users_Departments.query.filter(Users_Departments.department_id==department_id,
													Users_Departments.member_id==member_id).first()
	if not user_department:
		new_user_department = Users_Departments(department_id=department_id,
												member_id=member_id,
												is_comanager=is_comanager)
		mysql.session.add(new_user_department)
	
	mysql.session.commit()
	
	data['code'] = 200
	data['message'] = 'Member added to department successfully.'
	return jsonify(data)



@member.route('/<member_id>/delete_department', methods=['POST'])
@login_required
def delete_member_department(member_id):
	data = {}
	
	if not is_admin(current_user.member_id) :
		data['code'] = 400
		data['message'] = 'you are not allowed to perform this action'
		return jsonify(data)
	
	department_id = request.form.get('department_id')
	
	user = Members.query.filter(Members.member_id==member_id).first()
	if not user:
		data['code'] = 400
		data['message'] = 'Member does not exist.'
		return jsonify(data)
	
	department = Departments.query.filter(Departments.department_id==department_id).first()
	if not department:
		data['code'] = 400
		data['message'] = 'Department does not exist.'
		return jsonify(data)
	
	user_department = Users_Departments.query.filter(Users_Departments.department_id==department_id,
													Users_Departments.member_id==member_id).first()
	if user_department:
		user_department.is_joined = False
		user_department.exit_time = mysql.func.now()
		
	mysql.session.commit()
	
	data['code'] = 200
	data['message'] = 'Member deleted from department successfully.'
	return jsonify(data)



@member.route('/get_all_members', methods=['GET'])
def get_all_members():
	data = {}
	
	filter_by_name = request.args.get("filter_by_name")
	if filter_by_name == None :
		filter_by_name = ''
	
	filter_by_depart_name = request.args.get("filter_by_depart_name")
	if filter_by_depart_name == None :
		filter_by_depart_name = ''
	
	filter_by_role = request.args.get("filter_by_role")
	if filter_by_role == None or not filter_by_role in USERS_ROLES:
		filter_by_role = ''
	
	# Members.member_departments.any(Departments.departments_name.contains(filter_by_depart_name))).\
	members = Members.query.filter(Members.full_name.contains(filter_by_name),
									Members.role.contains(filter_by_role),
									Members.role.contains(filter_by_role),
									Departments.departments_name.contains(filter_by_depart_name)).\
							outerjoin(Departments, Members.member_departments).\
							order_by(Members.joined_time.desc()).\
							all()
	
	data['members'] = []
	
	for member in members :
		member_data = {}
		member_data['member_id'] = member.member_id
		member_data['full_name'] = member.full_name
		member_data['email'] = member.email
		member_data['joined_time'] = member.joined_time
		member_data['discord_id'] = member.discord_id
		member_data['role'] = member.role
		member_data['member_activities'] = []
		member_data['member_events'] = []
		member_data['member_departments'] = []
		
		for activity in member.member_activities :
			x = {}
			x['activity_id'] = activity.activity_id
			x['activity_name'] = activity.activity_name
			x['created_time'] = activity.created_time
			member_data['member_activities'].append(x)
		
		for event in member.member_events :
			x = {}
			x['event_id'] = event.event_id
			x['event_title'] = event.event_title
			x['started_time'] = event.started_time
			x['ended_time'] = event.ended_time
			x['event_role'] = event.event_role
			member_data['member_events'].append(x)
		
		for department in member.member_departments :
			x = {}
			x['department_id'] = department.department_id
			x['department_name'] = department.departments_name
			x['is_comanager'] = department.is_comanager
			x['is_joined'] = department.is_joined
			x['joined_time'] = department.joined_time
			x['exit_time'] = department.exit_time
			member_data['member_departments'].append(x)
		
		data['members'].append(member_data)
	
	data['code'] = 200
	data['message'] = 'success.'
	return jsonify(data)

