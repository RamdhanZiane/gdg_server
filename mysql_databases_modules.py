from main import *




USERS_ROLES = ['lead' , 'hr' , 'comanager' , 'member' , 'alumni']
EVENTS_ROLES = ['team_leader' , 'organizer' , 'participant']



# ACCOUNTS DATABASE CLASS
class Users(UserMixin, mysql.Model):
	__tablename__ = 'users' 
	
	user_id = mysql.Column(mysql.String(100), primary_key=True , unique=True , default=uuid.uuid4().hex) 
	full_name = mysql.Column(mysql.String(100) , default='') 
	email = mysql.Column(mysql.String(100) , default='') 
	joined_time = mysql.Column(mysql.DateTime(timezone=True) , default='') 
	discord_id = mysql.Column(mysql.String(100) , unique=True , default='') 

	role = mysql.Column(mysql.String(100) , unique=True , default='') 
	password = mysql.Column(mysql.String(100) , default='')
	
	user_activities = mysql.relationship('Activities', secondary=Users_Activities, backref='user',cascade="all, delete",passive_deletes=True)
	user_events = mysql.relationship('Events', secondary=Users_Events, backref='user',cascade="all, delete",passive_deletes=True)
	user_departments = mysql.relationship('Departments', secondary=Users_Departments, backref='user',cascade="all, delete",passive_deletes=True)

	#mysql.Column(mysql.DateTime(timezone=True), default=mysql.func.now())


Users_Activities = mysql.Table(
    "users__activities",
    mysql.Column("user_id", mysql.String(100), mysql.ForeignKey("users.user_id", ondelete="CASCADE")),
    mysql.Column("activity_id", mysql.String(100), mysql.ForeignKey("activities.activity_id", ondelete="CASCADE")),
)


class Activities(mysql.Model):
	__tablename__ = 'activities' 
	
	activity_id = mysql.Column(mysql.String(100), primary_key=True , unique=True , default=uuid.uuid4().hex) 
	activity_name = mysql.Column(mysql.String(100) , default='') 
	created_time = mysql.Column(mysql.DateTime(timezone=True) , default='') 
	
	activity_users = mysql.relationship('Users', secondary=Users_Activities, backref='activity' ,cascade="all, delete",passive_deletes=True)


Users_Events = mysql.Table(
	"users__events",
	mysql.Column("user_id", mysql.String(100), mysql.ForeignKey("users.user_id", ondelete="CASCADE")),
	mysql.Column("event_id", mysql.String(100), mysql.ForeignKey("events.event_id", ondelete="CASCADE")),

	mysql.Column('event_role', mysql.String(100))
)


class Events(mysql.Model):
	__tablename__ = 'events'

	event_id = mysql.Column(mysql.String(100), primary_key=True , unique=True , default=uuid.uuid4().hex)
	event_title = mysql.Column(mysql.String(100) , default='') 
	started_time = mysql.Column(mysql.DateTime(timezone=True), default=mysql.func.now())
	ended_time = mysql.Column(mysql.DateTime(timezone=True), default=mysql.func.now())
	
	event_users = mysql.relationship('Users', secondary=Users_Events, backref='event' ,cascade="all, delete",passive_deletes=True)



Users_Departments = mysql.Table(
	"users__departments",
	mysql.Column("user_id", mysql.String(100), mysql.ForeignKey("users.user_id", ondelete="CASCADE")),
	mysql.Column("department_id", mysql.String(100), mysql.ForeignKey("departments.department_id", ondelete="CASCADE")),

	mysql.Column('is_comanager',mysql.Boolean() , default=False)
	
	mysql.Column('is_joined',mysql.Boolean() , default=True)
	mysql.Column('joined_time',mysql.DateTime(timezone=True), default=mysql.func.now())
	mysql.Column('exit_time',mysql.DateTime(timezone=True), default=mysql.func.now())
)


class Departments(mysql.Model):
	__tablename__ = 'departments'

	department_id = mysql.Column(mysql.String(100), primary_key=True , unique=True , default=uuid.uuid4().hex)
	departments_name = mysql.Column(mysql.String(100) , default='') 
	
	department_users = mysql.relationship('Users', secondary=Users_Departments, backref='department' ,cascade="all, delete",passive_deletes=True)


