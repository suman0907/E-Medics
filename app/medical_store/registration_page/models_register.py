from app import db
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model):
   __tablename__ = 'users'
   id =           db.Column(db.Integer, primary_key=True, autoincrement=True)
   email =        db.Column(db.String(120), unique=True)
   mobile =       db.Column(db.String(16), unique=True)
   password =     db.Column(db.String(120))
   display_name = db.Column(db.String(120))
   display_image= db.Column(db.String(512))
   cover_image =  db.Column(db.String(512))

   def set_password(self, passw):
       self.password = generate_password_hash(passw) #encrypt the password which is coming from the frontendas passw

   def import_data(self, data):
           try:

               self.id = data.get('id', None)
               self.email = data.get('email', None)
               self.mobile = data.get('mobile', None)
               self.password = generate_password_hash(data.get('password', None))
               self.display_name = data.get('display_name', None)
               self.display_image = data.get('display_image', None)
               self.cover_image = data.get('cover_image', None)

               return self

           except Exception as e:

               return str(e)

   def check_password(self, passwrd):
       return check_password_hash(self.password, passwrd) #decrypt the passwrd nd matches wid the frontend passw
