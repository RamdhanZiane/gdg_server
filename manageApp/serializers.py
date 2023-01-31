from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import Activities

class ActivitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Activities
        # include_fk = True
        load_instance = True
        include_relationships = True