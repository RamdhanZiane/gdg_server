from main import *



# ACCOUNTS DATABASE CLASS
class Users(UserMixin, mysql.Model):
	__tablename__ = 'users' 
	
	user_id = mysql.Column(mysql.String(100), primary_key=True , unique=True , default=uuid.uuid4().hex) 
	created_time = mysql.Column(mysql.DateTime(timezone=True), default=mysql.func.now())
	full_name = mysql.Column(mysql.String(100) , default='') 
	
	is_su = mysql.Column(mysql.Boolean() , default=False)
	is_admin = mysql.Column(mysql.Boolean() , default=False)
	password = mysql.Column(mysql.String(100) , default='')
	
	discord_id = mysql.Column(mysql.String(100) , unique=True , default='') 
	discord_nick_name = mysql.Column(mysql.String(100) , default='') 
	discord_description = mysql.Column(mysql.Text , default='') 
	discord_joined_time = mysql.Column(mysql.String(100) , default='') 
	discord_gdg_joined_time = mysql.Column(mysql.String(100) , default='') 
	
	user_events = mysql.relationship('UsersEvents', backref='user',cascade="all, delete",passive_deletes=True)
	
	#mysql.Column(mysql.DateTime(timezone=True), default=mysql.func.now())



class UsersEvents(mysql.Model):
	__tablename__ = 'users_events'

	user_event_id = mysql.Column(mysql.String(100), primary_key=True , unique=True , default=uuid.uuid4().hex)
	created_time = mysql.Column(mysql.DateTime(timezone=True), default=mysql.func.now())
	
	event_title = mysql.Column(mysql.String(100) , default='') 
	event_joined_time = mysql.Column(mysql.String(100) , default='') 

	user_id = mysql.Column(mysql.String(100), mysql.ForeignKey('users.user_id', ondelete="CASCADE"))


