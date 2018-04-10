from app import db
from app.models import *


class Product_Specs(Base):
    __tablename__ = 'product_specs'
    id=              db.Column(db.Integer,primary_key=True,autoincrement=True)
    type=            db.Column(db.String(64))
    quantity=        db.Column(db.Integer,nullable=False)
    manfact_by=      db.Column(db.String(128))
    contents=        db.Column(db.String(128))

    def import_data(self, data):
        self.updated_by = "Suman"
        self.type = data.get('type',None)
        self.quantity = data['quantity']
        self.manfact_by = data.get('manfact_by',None)
        self.contents=data.get('contents',None)

        return self


class Product_Info(Base):
    __tablename__ = 'product_info'
    id =     db.Column(db.Integer,primary_key=True,autoincrement=True)
    product_name=    db.Column(db.String(128),nullable=False)
    made_on=         db.Column(db.String(64),nullable=False)
    expires_on=      db.Column(db.String(64),nullable=False)
    cost=            db.Column(db.BigInteger,nullable=False)
    specs_id=        db.Column(db.Integer,db.ForeignKey('product_specs.id'),index=True)

    def import_data(self, data): #self is object nd data is json data coming from frontend
        self.updated_by = "Suman"
        self.product_name = data['product_name'] #the variable product name is called by object whose data is coming from frontend
        self.made_on = data['made_on']
        self.expires_on = data['expires_on']
        self.cost = data['cost']

        return self

    def set_specs_id(self, specs_id):
        try:
            self.specs_id = specs_id #here we assiged the value to f.k in master table
            return self
        except Exception as e:
            return str(e)




class Product_Uses(Base):
    __tablename__ = 'product_uses'
    id=              db.Column(db.Integer,primary_key=True)
    use=             db.Column(db.String(64),nullable=False)
    level=           db.Column(db.Enum('1','2','3','4','5'),nullable=False)
    product_id=      db.Column(db.Integer,db.ForeignKey('product_info.id'),index=True)

    def import_data(self, data):
        self.updated_by = "Suman"
        self.use = data['use']
        self.level = data['level']


        return self

    def set_product_id(self, product_id):
        try:
            self.product_id = product_id  # here we assiged the value to f.k in master table
            return self
        except Exception as e:
            return str(e)


class Product_Info_Temp(Base):
    __tablename__ = 'product_info_temp'
    id =     db.Column(db.Integer,primary_key=True,autoincrement=True)
    product_name=    db.Column(db.String(128),nullable=False)
    made_on=         db.Column(db.String(64),nullable=False)
    expires_on=      db.Column(db.String(64),nullable=False)
    cost=            db.Column(db.BigInteger,nullable=False)


    def import_data(self, data): #self is object nd data is json data coming from frontend
        self.updated_by = "Suman"
        self.product_name = data['product_name'] #the variable product name is called by object whose data is coming from frontend
        self.made_on = data['made_on']
        self.expires_on = data['expires_on']
        self.cost = data['cost']

        return self

    def export_data(self):
        try:
            return {
                "product_name": self.product_name,
                "made_on": self.made_on,
                "suman": self.updated_by,
                "expires_on": self.expires_on,
                "cost": self.cost


            }
        except Exception as e:
            return str(e)


