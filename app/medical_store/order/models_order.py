from app import db
from app.models import *


class Order_Info(Base):
    __tablename__ = 'order_info'
    id =        db.Column(db.Integer,primary_key=True)

    def import_data(self,data):
        try:
            return self

        except Exception as e:
            return str(e)