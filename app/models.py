
#Add all common models/tables in this file.

from app import db
from sqlalchemy import *

class Base(db.Model):#base is  abstract class name nd db.model is writthen when no inheritance is to be made
    __abstract__ = True
    created_on = db.Column(db.DateTime, server_default=func.now())
    updated_on = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    updated_by = db.Column(db.String(512), nullable=False)

