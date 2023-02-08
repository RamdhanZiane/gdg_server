from flask import Blueprint, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Members, Events, Activities, Departments
from . import models
import json
from datetime import date, datetime
from marshmallow import ValidationError
from .serializers import ActivitySchema, EventSchema, DepartmentSchema


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

# Events endpoints

@views.route('/events', methods=['GET'])
def getEventList():
	# events = Events.query.all()
	# event_list = [{column.name: getattr(event, column.name) for column in Events.__table__.columns} for event in events]
	# return jsonify([event.to_dict() for event in events])
	
	events = Events.query.all()
	event_schema = EventSchema()
	return jsonify(event_schema.dump(events, many=True))

@views.route('/events/create', methods=['POST'])
def create_event():
	# data = request.get_json()
	# try:
	# 	event = Events(**data)
	# 	event.validate_data(data)
	# except ValueError as error:
	# 	return jsonify({'error': str(error)}), 400
	# except TypeError as error:
	# 	return jsonify({'error': str(error)}), 400
	# db.session.add(event)
	# db.session.commit()
	# return jsonify(event.to_dict())
	
	event_schema = EventSchema()
	event = event_schema.load(request.json, session=db.session)
	db.session.add(event)
	db.session.flush()
	event = event_schema.dump(event)
	db.session.commit()
	return jsonify(event)

@views.route('/events/<id>', methods=['GET'])
def get_event(id):
# 	event = Events.query.get(id)
# 	if event:
# 		return jsonify(event.to_dict())
# 	return jsonify({"error":"No event with such id exists"}), 404
	
	event_schema = EventSchema()
	event = Events.query.get(id)
	if event:
		return jsonify(event_schema.dump(event))
	return jsonify({
		'message':f'No event with ID {id} found'
	}), 404

@views.route('/events/<id>/update', methods=['PUT'])
def update_event(id):
# 	event = Events.query.get(id)
# 	if event:
# 		data = request.get_json()
# 		for key, value in data.items():
# 			setattr(event, key, value)
# 		event.validate_data(data)
# 		db.session.commit()
# 		return jsonify(event.to_dict())
# 	return jsonify({"error":"No event with such id exists"}), 404

	event_schema = EventSchema()
	event = Events.query.get(id)
	if event:
		try:
			updated_event = event_schema.load(request.json, session=db.session, instance=event, partial=True)
		except ValidationError as e:
			return jsonify({"error":e.messages}), 502
		db.session.commit()
		return jsonify(event_schema.dump(event))
	return jsonify({
		'message':f'No event with ID {id} found'
	}), 404

@views.route('/events/<id>/delete', methods=['DELETE'])
def delete_event(id):
	# event = Events.query.get(id)
	# if event:
	# 	db.session.delete(event)
	# 	db.session.commit()
	# 	return jsonify(event.to_dict()), 204
	# return jsonify({"error":"No event with such id exists"}), 404
	

	event = Events.query.get(id)
	if event:
		event_schema = EventSchema()
		db.session.delete(event)
		db.session.commit()
		return jsonify({event_schema.dump(event)})
	return jsonify({
		'message':f'No event with ID {id} found'	
	}), 404

# Activities endpoints

@views.route('/activities', methods=['GET'])
def getActivityList():
	activities = Activities.query.all()
	activity_schema = ActivitySchema()
	return jsonify(activity_schema.dump(activities, many=True))

@views.route('/activities/create', methods=['POST'])
def create_activity():

	activity_schema = ActivitySchema()
	activity = activity_schema.load(request.json, session=db.session)
	db.session.add(activity)
	db.session.flush()
	activity = activity_schema.dump(activity)
	db.session.commit()
	return jsonify(activity)

@views.route('/activities/<id>', methods=['GET'])
def get_activity(id):
	activity_schema = ActivitySchema()
	activity = Activities.query.get(id)
	if activity:
		return jsonify(activity_schema.dump(activity))
	return jsonify({
		'message':f'No activity with ID {id} found'
	}), 404

@views.route('/activities/<int:id>/delete', methods=['DELETE'])
def delete_activity(id):
	activity = Activities.query.get(activity_id=id)
	if activity:
		activity_schema = ActivitySchema()
		db.session.delete(activity)
		db.session.commit()
		return jsonify({activity_schema.dump(activity)})
	return jsonify({
		'message':f'No activity with ID {id} found'	
	}), 404

@views.route('/activities/<id>/update', methods=['PUT'])
def update_activity(id):
	activity_schema = ActivitySchema()
	activity = Activities.query.get(id)
	if activity:
		try:
			updated_activity = activity_schema.load(request.json, session=db.session, instance=activity, partial=True)
		except ValidationError as e:
			return jsonify({"error":e.messages}), 502
		db.session.commit()
		return jsonify(activity_schema.dump(activity))
	return jsonify({
		'message':f'No activity with ID {id} found'
	}), 404


# Departments endpoints

@views.route('/activities', methods=['GET'])
def getDepartmentList():
	activities = Activities.query.all()
	activity_schema = ActivitySchema()
	return jsonify(activity_schema.dump(activities, many=True))

@views.route('/departments/<name>', methods=['GET'])
def get_department(name):
	department_schema = DepartmentSchema()
	department = Departments.query.get(departments_name=name)
	if department:
		return jsonify(department_schema.dump(department))
	return jsonify({
		'message':f'No department with name {name} found'
	}), 404