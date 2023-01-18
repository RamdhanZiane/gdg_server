from . import db as mysql
from flask_login import UserMixin
from sqlalchemy.sql import func


USERS_ROLES = ['lead' , 'hr' , 'comanager' , 'member' , 'alumni']
EVENTS_ROLES = ['team_leader' , 'organizer' , 'participant']



Users_Activities = mysql.Table(
    "members__activities",
    mysql.Column("id", mysql.String(100), mysql.ForeignKey("members.id", ondelete="CASCADE")),
    mysql.Column("activity_id", mysql.String(100), mysql.ForeignKey("activities.activity_id", ondelete="CASCADE")),
)



Users_Events = mysql.Table(
	"members__events",
	mysql.Column("id", mysql.String(100), mysql.ForeignKey("members.id", ondelete="CASCADE")),
	mysql.Column("event_id", mysql.String(100), mysql.ForeignKey("events.event_id", ondelete="CASCADE")),

	mysql.Column('event_role', mysql.String(100))
)



Users_Departments = mysql.Table(
	"members__departments",
	mysql.Column("id", mysql.String(100), mysql.ForeignKey("members.id", ondelete="CASCADE")),
	mysql.Column("department_id", mysql.String(100), mysql.ForeignKey("departments.department_id", ondelete="CASCADE")),

	mysql.Column('is_comanager',mysql.Boolean() , default=False),
	
	mysql.Column('is_joined',mysql.Boolean() , default=True),
	mysql.Column('joined_time',mysql.DateTime(timezone=True), default=mysql.func.now()),
	mysql.Column('exit_time',mysql.DateTime(timezone=True), default=mysql.func.now())
)



# ACCOUNTS DATABASE CLASS
class Members(UserMixin, mysql.Model):
	__tablename__ = 'members' 
	
	id = mysql.Column(mysql.Integer, primary_key=True , unique=True) 
	full_name = mysql.Column(mysql.String(100) , default='') 
	email = mysql.Column(mysql.String(100) , default='') 
	joined_time = mysql.Column(mysql.DateTime(timezone=True) , default='') 
	discord_id = mysql.Column(mysql.String(100) , unique=True , default='') 

	role = mysql.Column(mysql.String(100) , unique=True , default='') 
	password = mysql.Column(mysql.String(100) , default='')
	
	member_activities = mysql.relationship('Activities', secondary=Users_Activities, backref='member',cascade="all, delete",passive_deletes=True)
	member_events = mysql.relationship('Events', secondary=Users_Events, backref='member',cascade="all, delete",passive_deletes=True)
	member_departments = mysql.relationship('Departments', secondary=Users_Departments, backref='member',cascade="all, delete",passive_deletes=True)

	def __repr__(self):
		return '<member {}>'.format(self.full_name)
	#mysql.Column(mysql.DateTime(timezone=True), default=mysql.func.now())
# user_manager = UserManager(app, db, Client)



class Activities(mysql.Model):
	__tablename__ = 'activities' 
	
	activity_id = mysql.Column(mysql.String(100), primary_key=True , unique=True) 
	activity_name = mysql.Column(mysql.String(100) , default='') 
	created_time = mysql.Column(mysql.DateTime(timezone=True) , default='') 
	
	activity_members = mysql.relationship('Members', secondary=Users_Activities, backref='activity' ,cascade="all, delete",passive_deletes=True)


class Events(mysql.Model):
	__tablename__ = 'events'

	event_id = mysql.Column(mysql.Integer, primary_key=True , unique=True)
	event_title = mysql.Column(mysql.String(100) , default='') 
	started_time = mysql.Column(mysql.DateTime(timezone=True), default=mysql.func.now())
	ended_time = mysql.Column(mysql.DateTime(timezone=True), default=mysql.func.now())
	
	event_members = mysql.relationship('Members', secondary=Users_Events, backref='event' ,cascade="all, delete",passive_deletes=True)



class Departments(mysql.Model):
	__tablename__ = 'departments'

	department_id = mysql.Column(mysql.String(100), primary_key=True , unique=True)
	departments_name = mysql.Column(mysql.String(100) , default='') 
	
	department_members = mysql.relationship('Members', secondary=Users_Departments, backref='department' ,cascade="all, delete",passive_deletes=True)


