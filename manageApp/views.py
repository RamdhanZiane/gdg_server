from flask import Blueprint, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Members, Events, Activities
from . import models
import json
from datetime import date, datetime

from .serializers import ActivitySchema

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

# @views.route('/events/create', methods=['POST'])
# @views.route('/events/<int:id>', methods=['GET', 'UPDATE'])


@views.route('/events', methods=['GET'])
def getEventList():
	events = Events.query.all()
	# return jsonify(events)
	# return Events.fs_get_delete_put_post(id)
	event_list = [{column.name: getattr(event, column.name) for column in Events.__table__.columns} for event in events]
	return jsonify([event.to_dict() for event in events])

@views.route('/events/create', methods=['POST'])
def create_event():
	data = request.get_json()
	try:
		event = Events(**data)
		event.validate_data(data)
	except ValueError as error:
		return jsonify({'error': str(error)}), 400
	except TypeError as error:
		return jsonify({'error': str(error)}), 400
	db.session.add(event)
	db.session.commit()
	return jsonify(event.to_dict())

@views.route('/events/<id>', methods=['GET'])
def get_event(id):
	event = Events.query.get(id)
	if event:
		return jsonify(event.to_dict())
	return jsonify({"error":"No event with such id exists"}), 404

@views.route('/events/<id>/update', methods=['PUT'])
def update_event(id):
	event = Events.query.get(id)
	if event:
		data = request.get_json()
		for key, value in data.items():
			setattr(event, key, value)
		event.validate_data(data)
		db.session.commit()
		return jsonify(event.to_dict())
	return jsonify({"error":"No event with such id exists"}), 404

@views.route('/events/<id>/delete', methods=['DELETE'])
def delete_event(id):
	event = Events.query.get(id)
	if event:
		db.session.delete(event)
		db.session.commit()
		return jsonify(event.to_dict()), 204
	return jsonify({"error":"No event with such id exists"}), 404



@views.route('/activities', methods=['GET'])
def getActivityList():
	
	# activities = Activities.query.all()
	# list = [act.serialize() for act in activities]
	# return json.dumps(list)
	
	activities = Activities.query.all()
	activity_schema = ActivitySchema()
	return jsonify(activity_schema.dump(activities, many=True))

@views.route('/activities/create', methods=['POST'])
def create_activity():
	# activity_name = request.form['activity_name']
	# created_time = request.form['created_time']
	# activity = Activities(activity_name, created_time)

	# db.session.add(activity)
	# db.session.commit()
	# return json.dumps(activity.serialize())

	activity_schema = ActivitySchema()
	activity_data = activity_schema.load(request.json, session=db.session)
	activity = Activities(activity_data)
	# db.session.add(activity)
	# db.session.commit()
	return jsonify(activity_data)

@views.route('/activities/<int:id>', methods=['GET'])
def get_activity(id):
	activity = Activities.query.filter_by(activity_id=id).first()
	if activity:
		return jsonify(activity)
	return {
		'status_code':404,
		'message':f'No activity with ID {id} found'
	}

@views.route('/activities/<int:id>/delete', methods=['DELETE'])
def delete_activity(id):
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