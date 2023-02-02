from . import db as mysql
from flask_login import UserMixin
from sqlalchemy.sql import func
import uuid
from datetime import datetime
from sqlalchemy.inspection import inspect


USERS_ROLES = ['lead' , 'hr' , 'comanager' , 'member' , 'alumni']
EVENTS_ROLES = ['team_leader' , 'organizer' , 'participant']



# Users_Activities = mysql.Table(
#     "members__activities",
#     mysql.Column("member_id", mysql.String(100), mysql.ForeignKey("members.member_id", ondelete="CASCADE")),
#     mysql.Column("activity_id", mysql.String(100), mysql.ForeignKey("activities.activity_id", ondelete="CASCADE")),
# )



# Users_Events = mysql.Table(
# 	"members__events",
# 	mysql.Column("member_id", mysql.String(100), mysql.ForeignKey("members.member_id", ondelete="CASCADE")), # PRIMARY_KEY=TRUE
# 	mysql.Column("event_id", mysql.String(100), mysql.ForeignKey("events.event_id", ondelete="CASCADE")),

# 	mysql.Column('event_role', mysql.String(100))
# )



# Users_Departments = mysql.Table(
# 	"members__departments",
# 	mysql.Column("member_id", mysql.String(100), mysql.ForeignKey("members.member_id", ondelete="CASCADE")), # PRIMARYKEY=TRUE
# 	mysql.Column("department_id", mysql.String(100), mysql.ForeignKey("departments.department_id", ondelete="CASCADE")),

# 	mysql.Column('is_comanager',mysql.Boolean() , default=False),
	
# 	mysql.Column('is_joined',mysql.Boolean() , default=True),
# 	mysql.Column('joined_time',mysql.DateTime(timezone=True), default=mysql.func.now()),
# 	mysql.Column('exit_time',mysql.DateTime(timezone=True), default=mysql.func.now())
# )



# ACCOUNTS DATABASE CLASS
class Members(UserMixin, mysql.Model):
	__tablename__ = 'members' 
	
	member_id = mysql.Column(mysql.String(100), primary_key=True , unique=True , default=uuid.uuid4().hex) 
	full_name = mysql.Column(mysql.String(100) , default='') 
	email = mysql.Column(mysql.String(100) , default='') 
	joined_time = mysql.Column(mysql.DateTime(timezone=True) , default=mysql.func.now()) 
	discord_id = mysql.Column(mysql.String(100) , unique=True , default='') 

	role = mysql.Column(mysql.String(100) , default='') 
	password = mysql.Column(mysql.String(100) , default='')
	
	is_su = mysql.Column(mysql.Boolean, default=False)
	is_hr = mysql.Column(mysql.Boolean, default=False)

	alumni = mysql.Column(mysql.Boolean, default=False)
	# member_activities = mysql.relationship('Activities', secondary=Users_Activities, backref='member',cascade="all, delete",passive_deletes=True)
	# member_events = mysql.relationship('Events', secondary=Users_Events, backref='member',cascade="all, delete",passive_deletes=True)
	# member_departments = mysql.relationship('Departments', secondary=Users_Departments, backref='member',cascade="all, delete",passive_deletes=True)

	#mysql.Column(mysql.DateTime(timezone=True), default=mysql.func.now())



class Activities(mysql.Model):
	__tablename__ = 'activities' 
	
	activity_id = mysql.Column(mysql.Integer, primary_key=True , unique=True) 
	activity_name = mysql.Column(mysql.String(100) , default='') 
	created_time = mysql.Column(mysql.Date() , default='') 
	
	# members = mysql.relationship('Members', secondary=Users_Activities, backref='activities' ,cascade="all, delete",passive_deletes=True)

	# def __init__(self, name, time):
	# 	self.activity_name = name
	# 	self.created_time = datetime.strptime(time, '%d/%m/%Y')

	# def serialize(self):
	# 	return { 
	# 	'activity_id': self.activity_id,
	#     'activity_name': self.activity_name,
	# 	'created_time': self.created_time.isoformat()
	#     }

class Events(mysql.Model):
	__tablename__ = 'events'

	event_id = mysql.Column(mysql.String(100), primary_key=True , unique=True , default=uuid.uuid4().hex)
	event_title = mysql.Column(mysql.String(100) , default='') 
	started_time = mysql.Column(mysql.DateTime(timezone=True), default=mysql.func.now())
	ended_time = mysql.Column(mysql.DateTime(timezone=True), default=mysql.func.now())
	
	# event_members = mysql.relationship('Members', secondary=Users_Events, backref='event' ,cascade="all, delete",passive_deletes=True)

	def to_dict(model_instance, query_instance=None):
		if hasattr(model_instance, '__table__'):
			return {c.name: str(getattr(model_instance, c.name)) for c in model_instance.__table__.columns}
		else:
			cols = query_instance.column_descriptions
			return { cols[i]['name'] : model_instance[i]  for i in range(len(cols)) }

	def from_dict(dict, model_instance):
		for c in model_instance.__table__.columns:
			setattr(model_instance, c.name, dict[c.name])

	def validate_data(self, data):
		keys = data.keys()
		if 'started_time' in keys:
			value = datetime.strptime(data['started_time'], '%d/%m/%Y')
			if not value:
				raise ValueError("Event started_date must be in format 'dd/mm/yyyy'")
			else:
				self.started_time = value
		if 'ended_time' in keys:
			value = datetime.strptime(data['ended_time'], '%d/%m/%Y')
			if not value:
				raise ValueError("Event ended_date must be in format 'dd/mm/yyyy'")
			else:
				self.ended_time = value


class Departments(mysql.Model):
	__tablename__ = 'departments'

	department_id = mysql.Column(mysql.String(100), primary_key=True , unique=True , default=uuid.uuid4().hex)
	departments_name = mysql.Column(mysql.String(100) , default='') 
	manager_count = mysql.Column(mysql.Integer, default=0)
	# department_members = mysql.relationship('Members', secondary=Users_Departments, backref='department' ,cascade="all, delete",passive_deletes=True)

	def __init__(self, departmentName):
		self.departments_name = departmentName
		self.manager_count = 0

class Member_Activity(mysql.Model):
    __tablename__ = "member_activity"
    id = mysql.Column(mysql.String(100), primary_key = True, unique=True , default=uuid.uuid4().hex)
    member_id = mysql.Column(mysql.String(100), mysql.ForeignKey("members.member_id", ondelete="CASCADE"), primary_key=True)
    activity_id = mysql.Column(mysql.String(100), mysql.ForeignKey("activities.activity_id", ondelete="CASCADE"), primary_key=True)
    member = mysql.relationship('Members', backref="activities")
    activity = mysql.relationship('Activities', backref="members")

    __table_args__ = (
        mysql.UniqueConstraint('member_id', 'activity_id'),
      )


class User_event(mysql.Model):
    __tablename__ = "member_event"
    id = mysql.Column(mysql.String(100), primary_key = True, unique=True , default=uuid.uuid4().hex)
    member_id = mysql.Column(mysql.String(100), mysql.ForeignKey("members.member_id", ondelete="CASCADE"), primary_key=True)
    event_id = mysql.Column(mysql.String(100), mysql.ForeignKey("events.event_id", ondelete="CASCADE"), primary_key=True)
    member = mysql.relationship('Members', backref="events")
    event = mysql.relationship('Events', backref="members")
    
    role = mysql.Column(mysql.String(100))

    __table_args__ = (
        mysql.UniqueConstraint('member_id', 'event_id'),
      )


class member_department(mysql.Model):
    __tablename__ = "members__departments"
    id = mysql.Column(mysql.String(100), primary_key = True, unique=True , default=uuid.uuid4().hex)
    member_id = mysql.Column(mysql.String(100), mysql.ForeignKey("members.member_id", ondelete="CASCADE"), primary_key=True)
    department_id = mysql.Column(mysql.String(100), mysql.ForeignKey("departments.department_id", ondelete="CASCADE"), primary_key=True)
    member = mysql.relationship('Members', backref="departments")
    department = mysql.relationship('Departments', backref="members")

    is_comanager = mysql.Column(mysql.Boolean() , default=False)
	
    is_joined = mysql.Column(mysql.Boolean() , default=True)
    joined_time = mysql.Column(mysql.DateTime(timezone=True), default=mysql.func.now())
    exit_time = mysql.Column(mysql.DateTime(timezone=True), default=mysql.func.now())

    __table_args__ = (
        mysql.UniqueConstraint('member_id', 'department_id'),
      )
