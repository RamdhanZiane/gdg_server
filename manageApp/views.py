from flask import Blueprint, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Members, Events, Activities
from . import models
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return jsonify({'body':'hello world'})


# ROUTES

# @views.route('/favicon.ico')
# def favicon():
#     # return send_from_directory(STATIC_PATH , 'favicon.ico' , mimetype='image/vnd.microsoft.icon')
#     pass
	


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



@views.route('/depart/<int:id>', methods=['GET'])
def department(department_id):
	pass

# user = db.one_or_404(
#     db.select(User).filter_by(username=username),
#     description=f"No user named '{username}'."
# )

@views.route('/events', methods=['GET'])
def getEventList():
	# events = db.session.query(models.Members)
	events = Events.query.all()
	return jsonify(events)

@views.route('/events/create', methods=['POST'])
def create_event():
	# data = request.get_json()

	event_id = request.form['event_id']
	name = request.form['name']
	age = request.form['age']
	position = request.form['position']
	event = Events()

	db.session.add(event)
	db.session.commit()
	return {
		jsonify(event)
	}

@views.route('/events/<int:id>', methods=['GET'])
def get_event(id):
	event = Events.query.filter_by(event_id=id).first()
	if event:
		return jsonify(event)
	return {
		'status_code':404,
		'message':f'No event with ID {id} found'
	}

@views.route('/events/<int:id>/delete', methods=['DELETE'])
def delete_event(id):
	event = Events.query.filter_by(event_id=id).first()
	if event:
		db.session.delete(event)
		db.session.commit()
		return {
			'message':'No such event exists',
			'status_code':204
		}
	return {
		'status_code':404
	}



@views.route('/activities', methods=['GET'])
def getEventList():
	# activities = db.session.query(models.Members)
	activities = activities.query.all()
	return jsonify(activities)

@views.route('/activities/create', methods=['POST'])
def create_event():
	# data = request.get_json()

	event_id = request.form['event_id']
	name = request.form['name']
	age = request.form['age']
	position = request.form['position']
	activity = Activities()

	db.session.add(event)
	db.session.commit()
	return {
		jsonify(event)
	}

@views.route('/activities/<int:id>', methods=['GET'])
def get_event(id):
	event = Activities.query.filter_by(activity_id=id).first()
	if event:
		return jsonify(event)
	return {
		'status_code':404,
		'message':f'No activity with ID {id} found'
	}

@views.route('/activities/<int:id>/delete', methods=['DELETE'])
def delete_event(id):
	activity = Activities.query.filter_by(activity_id=id).first()
	if activity:
		db.session.delete(activity)
		db.session.commit()
		return {
			'message':'No such activity exists',
			'status_code':204
		}
	return {
		'status_code':404
	}