from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import os

"""
Features: Add, update, delete and list contacts.
You can store, view and update information such as name, 
surname and phone number in MongoDB.
"""

app = Flask(__name__)
api = Api(app)

mongo_uri = os.getenv('MONGO_URI', 'mongodb://db:27017')
client = MongoClient(mongo_uri)

db = client.PersonDatabase
people = db["People"]

class AddInfo(Resource):
    def post(self):
        posted_data = request.get_json()
    
        if not all(k in posted_data for k in ("name", "surname", "phone_number")):
            return jsonify({"status": 400, "msg": "Missing parameters"})
        
        name = posted_data["name"]
        surname = posted_data["surname"]
        phone_number = posted_data["phone_number"]

        result = people.insert_one({
            "Name": name,
            "Surname": surname,
            "Phone": phone_number
        })


        if result.inserted_id:
            retJson = {
                "status": 200,
                "msg": "Successful"
            }
        else:
            retJson = {
                "status": 500,
                "msg": "Insertion failed"
            }

        return jsonify(retJson)
    

class UpdateInfo(Resource):
    def put(self):
        posted_data = request.get_json()


        if not all(k in posted_data for k in ("name", "surname", "phone_number")):
            return jsonify({"status": 400, "msg": "Missing parameters"})
        
        name = posted_data["name"]
        surname = posted_data["surname"]
        phone_number = posted_data["phone_number"]

        query = {"Name": name, "Surname": surname}
        person = people.find_one(query)

        if person:
            result = people.update_one(
                query,
                {"$set": {"Phone": phone_number}}
            )
            
            if result.matched_count > 0:
                if result.modified_count > 0:
                    retJson = {"status": 200, "msg": "Update successful"}
                else:
                    retJson = {"status": 304, "msg": "No changes made"}
            else:
                retJson = {"status": 404, "msg": "Person not found"}
            
            return jsonify(retJson)
        else:
            retJson = {"status": 404, "msg": "Person not found"}
            return jsonify(retJson)

            
class DeleteInfo(Resource):
    def delete(self):
        posted_data = request.get_json()


        if not all(k in posted_data for k in ("name", "surname", "phone_number")):
            return jsonify({"status": 400, "msg": "Missing parameters"})
        
        name = posted_data["name"]
        surname = posted_data["surname"]
        phone_number = posted_data["phone_number"]

        result = people.delete_one({ "Name":name,
                                     "Surname":surname,
                                     "Phone": phone_number })
        
        if result.deleted_count > 0:
            retJson = {"status": 200, "msg": "Delete successful"}
        else:
            retJson = {"status": 404, "msg": "Person not found"}

        return jsonify(retJson)

class GetInfo(Resource):
    def get(self):
        posted_data = request.get_json()

    
        if not all(k in posted_data for k in ("name", "surname")):
            return jsonify({"status": 400, "msg": "Missing parameters"})
        
        name = posted_data["name"]
        surname = posted_data["surname"]

        result = people.find_one({ "Name": name, "Surname": surname })
        
        if result:
            phone_number = result.get("Phone", "No phone number available")

            retJson = {
                "status": 200,
                "msg": "Person found",
                "Number": phone_number
            } 

        else:
            retJson = {
                "status": 404,
                "msg": "Person not found"
            }

        return jsonify(retJson)


api.add_resource(AddInfo,"/add")
api.add_resource(UpdateInfo,"/update")
api.add_resource(DeleteInfo,"/delete")
api.add_resource(GetInfo,"/get")

if __name__=="__main__":
    app.run(host='0.0.0.0')
