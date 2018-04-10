from . import user_register
from .models_register import *
from flask import *
from sqlalchemy import and_
from sqlalchemy import or_




@user_register.route('/login', methods=['POST'])
def login():
   try:
       user = Users.query.filter_by(email=request.json['email']).first()
       if not user or not user.check_password(request.json['password']):
           response = jsonify(response = 'error', message='Wrong Email or Password')
           #response.status_code = 401
           return response

       return jsonify( response="success")

   except Exception as e:
       return jsonify({"response" : "error","message" : "Try Again"})


@user_register.route('/signup', methods=['POST'])
def signup():
   try:
       RequestObject = request.get_json()

       if Users.query.filter(Users.email == RequestObject['email']).count() > 0 or \
                       Users.query.filter(Users.mobile == RequestObject['mobile']).count() > 0:
           response = jsonify({"response" : "error", "message" : "There already exists a User with the Entered Email or Mobile"})
           #response.status_code = 401
           return response

       user = Users()
       user.import_data(RequestObject)
       db.session.add(user)
       db.session.commit()

       return jsonify(response = "success")

   except Exception as e:
       db.session.rollback()
       print str(e)
       return jsonify({"response": "error", "message" : "Try Again"})