"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200

@app.route('/member' , methods=['POST'])
def add_member():
    age= request.json.get("age")
    first_name= request.json.get("first_name")
    lucky_numbers = request.json.get("lucky_numbers")
    
    if age is None:
        return "missing the age", 400
    if first_name is None:
        return "missing the first name ", 400
    if lucky_numbers is None:
        return "missing the lucky_number", 400
    
    
    jackson_family.add_member(
        {    
            "id": jackson_family._generateId(),
            "first_name": first_name,
            "last_name": jackson_family.last_name,
            "age":age,
            "lucky_number": lucky_numbers
        }
    )
    
    return "member has been added" ,200

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_family_member(id):
    jackson_family.delete_member(id)
    response={"family member has been deleted ": True}
    return jsonify(response), 200
   

@app.route('/member/<int:id>', methods=['GET'])
def get_individual_family_member(id):
    member = jackson_family.get_member(id)
    response= member
    return jsonify(response), 200



# @app.route('/member/<int:id>', methods=['GET'])
# def get_individual_family_member(id):
#     jackson_family.get_member(id)
#     response_body =add_member

#     return jsonify(response_body), 200
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
