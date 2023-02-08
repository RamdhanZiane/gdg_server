from . import db
from .models import Departments, Members, Activities, Events


db.drop_all()
db.create_all()

# initial departments
hr_department = Departments('Human Resources')
admin_department = Departments('Adminstration')

# initial members
m1 = Members()

db.session.add_all(hr_department, admin_department)
db.session.commit()