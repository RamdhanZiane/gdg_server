from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import Activities, Events, Departments
from marshmallow.fields import DateTime

class ActivitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Activities
        # include_fk = True
        load_instance = True
        include_relationships = True
    created_time = DateTime(format="%d/%m/%Y")


class EventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Events
        # include_fk = True
        load_instance = True
        include_relationships = True
    started_time = DateTime(format="%d/%m/%Y")
    ended_time = DateTime(format="%d/%m/%Y")


class DepartmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Departments
        # include_fk = True
        load_instance = True
        include_relationships = True