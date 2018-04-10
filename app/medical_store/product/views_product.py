from . import products
from .models_product import *
from flask import *
from sqlalchemy import and_
from sqlalchemy import or_

@products.route('/add_product', methods=['POST']) #set the  route for the particular API to run
def add_product():
   requestObject =  request.get_json() #in postman body -raw -json application ,it expect  a json data from frontend
   try:
       product = Product_Info() #product is the object for product_info() class
       product.import_data(requestObject)
       db.session.add(product)
       db.session.commit()
       return jsonify({"message": "success"})
   except Exception as e:
       print str(e)
       db.session.rollback()
       return jsonify({"message": "error","error_info" : str(e)})


@products.route('/get_product', methods=['GET'])
def get_product():
   idb =  request.args["id"] #expects a value after ? in url corresponding to mentioned key(here key is id)
   try:

       reqs =  { #request these data from the search
           "id":"",
           "product_name" : "",
           "cost" : ""

       }
       prodq = Product_Info.query.get(idb) #search the mentioned key in table
       if prodq is None :
           return jsonify({"message": "Not found" })
       prod_details = {}
       for key in reqs: #creates a loop to fetch data
           prod_details[key] = getattr(prodq,key)

       return jsonify({"message": "success", "product" : prod_details})
   except Exception as e:
       print str(e)
       db.session.rollback()
       return jsonify({"message": "error","error_info" : str(e)})


@products.route('/add_product_specs', methods=['POST']) #set the  route for the particular API to run
def add_product_specs():
   requestObject =  request.get_json() #get the json data including id of master table
   try:
       prodq = Product_Info.query.get(requestObject["pro_id"])  # search the mentioned key in master table(product info)
       if prodq is None: #if not find the id match in master table
           return jsonify({"message": "Not found"})

       product = Product_Specs() #product is the object for product_info() class
       product.import_data(requestObject) #it fill the data in product specs table which came from frontend
       db.session.add(product) #it adds the data in buffer
       db.session.flush() #it makes the table available to use at the run tym for any other purpose
       prodq.set_specs_id(product.id) #it sets the f.k in master table
       db.session.commit()
       return jsonify({"message": "success"})
   except Exception as e:
       print str(e)
       db.session.rollback()
       return jsonify({"message": "error","error_info" : str(e)})


@products.route('/get_product_specs', methods=['GET'])
def get_product_specs():
   idb =  request.args["id"] #expects a value after ? in url corresponding to mentioned key(here key is id)
   try:

       reqs =  { #request these data from the search
           "quantity":"",
           "type" : "",
           "contents" : ""

       }
       prodq = Product_Info.query.get(idb) #search the mentioned key in table
       if prodq is None :
           return jsonify({"message": "Not found" })
       spec_id = prodq.specs_id
       ids=Product_Specs.query.get(spec_id)
       if ids is None :
           return jsonify({"message": "Not found" })

       prod_details = {}
       for key in reqs: #creates a loop to fetch data
           prod_details[key] = getattr(ids ,key)

       return jsonify({"message": "success", "product" : prod_details})
   except Exception as e:
       print str(e)
       db.session.rollback()
       return jsonify({"message": "error","error_info" : str(e)})


@products.route('/add_product_uses', methods=['POST']) #set the  route for the particular API to run
def add_product_uses():
   requestObject =  request.get_json() #in postman body -raw -json application ,it expect  a json data from frontend
   try:
       prodq = Product_Info.query.get(requestObject["pro_id"])  # search the mentioned key in master table(product info)
       if prodq is None:  # if not find the id match in master table
           return jsonify({"message": "Not found"})

       product = Product_Uses() #product is the object for product_info() class
       product.import_data(requestObject)
       db.session.add(product)
       product.set_product_id(requestObject["pro_id"])

       db.session.commit()
       return jsonify({"message": "success"})
   except Exception as e:
       print str(e)
       db.session.rollback()
       return jsonify({"message": "error","error_info" : str(e)})

@products.route('/get_product_uses', methods=['GET'])
def get_product_uses():
   idb =  request.args["id"] #expects a value after ? in url corresponding to mentioned key(here key is id)
   try:

       reqs =  { #request these data from the search
           "use":"",
           "level" : "",
           "product_id" : ""

       }
       prodq = Product_Uses.query.filter(Product_Uses.product_id==idb) #search the mentioned key in table
       result = []
       for prods in prodq:
           if prods is None :
               return jsonify({"message": "Not found" })
           prod_details = {}
           for key in reqs: #creates a loop to fetch data
               prod_details[key] = getattr(prods,key)
           result.append(prod_details)

       return jsonify({"message": "success", "product" : result})

   except Exception as e:
       print str(e)
       db.session.rollback()
       return jsonify({"message": "error","error_info" : str(e)})


@products.route('/get_costly_product', methods=['GET'])
def get_costly_product():
   idb =  request.args["cost"] #expects a value after ? in url corresponding to mentioned key(here key is id)
   try:

       reqs =  { #request these data from the search
           "id":"",
           "product_name" : "",
           "cost" : ""

       }
       prodq = Product_Info.query.filter(Product_Info.cost>=idb) #search the mentioned key in table
       result = []
       for prods in prodq:
           if prods is None :
               return jsonify({"message": "Not found" })
           prod_details = {}
           for key in reqs: #creates a loop to fetch data
               prod_details[key] = getattr(prods,key)
           result.append(prod_details)
       return jsonify({"message": "success", "products" : result})
   except Exception as e:
       print str(e)
       db.session.rollback()
       return jsonify({"message": "error","error_info" : str(e)})

@products.route('/get_costly_product_with_name', methods=['GET'])# multiple to multiple
def get_costly_product_with_name():
   idb =  request.args["cost"] # expects a value after ? in url corresponding to mentioned key(here key is id)
   name = request.args["name"] # 2nd entity
   try:

       reqs =  { #request these data from the search
           "id":"",
           "product_name" : "",
           "cost" : ""
       }
       conditions = []
       conditions.append(Product_Info.cost>idb)
       conditions.append(Product_Info.product_name==name)
       condition = or_(*conditions)
       prodq = Product_Info.query.filter(condition) #search the mentioned key in table
       result = []
       for prods in prodq:
           if prods is None :
               return jsonify({"message": "Not found" })
           prod_details = {}
           for key in reqs: #creates a loop to fetch data
               prod_details[key] = getattr(prods,key)
           result.append(prod_details)
       return jsonify({"message": "success", "products" : result})
   except Exception as e:
       print str(e)
       db.session.rollback()
       return jsonify({"message": "error","error_info" : str(e)})

@products.route('/get_product_order', methods=['GET'])
def get_product_order():
   idb =  request.args["id"] #expects a value after ? in url corresponding to mentioned key(here key is id)
   try:

       reqs =  { #request these data from the search
           "use":"",
           "level" : ""


       }

       prodq = Product_Uses.query.filter(Product_Uses.product_id==idb).order_by(Product_Uses.level.desc())#search the mentioned key in table
       result = []
       for prods in prodq:
           if prods is None:
               return jsonify({"message": "Not found"})
           prod_details = {}
           for key in reqs:  # creates a loop to fetch data
               prod_details[key] = getattr(prods, key)
           result.append(prod_details)




       return jsonify({"message": "success", "product" : result})
   except Exception as e:
       print str(e)
       db.session.rollback()
       return jsonify({"message": "error","error_info" : str(e)})


@products.route('/add_product_moderate', methods=['POST'])
def add_product_moderate() :
   requestObject = request.get_json()

   try:
       temp_prodq = Product_Info_Temp.query.get(requestObject['id'])
       if temp_prodq is None:
           return {"response": "failure", "msg": "product not exists"}


       if requestObject['approval_status'] == "Approved":
           product = Product_Info()#forming object of product info() class
           suman= temp_prodq.export_data()
           product.import_data(suman)
           db.session.add(product)
       db.session.commit()
       return jsonify({"message": "success"})
   except Exception as e:
       print str(e)
       db.session.rollback()
       return jsonify({"message": "error","error_info" : str(e)})



@products.route('/add_product_info_temp', methods=['POST']) #set the  route for the particular API to run
def add_product_info_temp():
   requestObject =  request.get_json() #in postman body -raw -json application ,it expect  a json data from frontend
   try:
       product = Product_Info_Temp() #product is the object for product_info() class
       product.import_data(requestObject)
       db.session.add(product)
       db.session.commit()
       return jsonify({"message": "success"})
   except Exception as e:
       print str(e)
       db.session.rollback()
       return jsonify({"message": "error","error_info" : str(e)})


