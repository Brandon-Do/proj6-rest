# Laptop Service

from flask import Flask, request
from flask_restful import Resource, Api
from pymongo import MongoClient
import pymongo
import csv
import time
import os

# Instantiate the app
app = Flask(__name__)
client = MongoClient("db", 27017)
db = client.tododb
api = Api(app)
DEFAULT_TOP = -1 #Any negative integer => limitless

def retrieve_json(top = DEFAULT_TOP, fields = ["km", "open", "close"]):
    """
        The data within the MongoDB is structured to have fields 'km', 'open', 'close'.
        Pass this function a list of fields that are wanted, returns dictionary with corresponding fields.
    """
    data = db.tododb.find().sort("open", pymongo.ASCENDING)
    results = {}
    for field in fields:
        results[field] = []
    for d in data:
        if top == 0:
            break
        top -= 1

        for field in fields:
            results[field].append(d[field])

    return results

def retrieve_csv(top = DEFAULT_TOP, fields = ["km", "open", "close"]):
    """
        The data within the MongoDB is structured to have fields 'km', 'open', 'close'.
        Pass this function a list of fields that are wanted, returns dictionary with corresponding fields.
    """
    data = db.tododb.find().sort("open", pymongo.ASCENDING)
    results = ""
    for field in fields:
        results += field + ","
    results  += os.linesep

    for d in data:
        if top == 0:
            break
        top -= 1

        for field in fields:
            results += d[field] + ","
        results  += os.linesep

    return results.strip(os.linesep)

def handle(arg_str):
    if arg_str == None or not arg_str.isdigit():
        global DEFAULT_TOP
        top = DEFAULT_TOP
    else:
        top = int(arg_str)
    return top

class listAll(Resource):
    def get(self):
        top = handle(request.args.get("top"))
        return retrieve_json(top)

class listAll_json(Resource):
    def get(self):
        top = handle(request.args.get("top"))
        return retrieve_json(top)

class listAll_csv(Resource):
    def get(self):
        top = handle(request.args.get("top"))
        return retrieve_csv(top)

class listOpen(Resource):
    def get(self):
        top = handle(request.args.get("top"))
        return retrieve_json(top, ["open"])

class listOpen_json(Resource):
    def get(self):
        top = handle(request.args.get("top"))
        return retrieve_json(top, ["open"])

class listOpen_csv(Resource):
    def get(self):
        top = handle(request.args.get("top"))
        return retrieve_csv(top, ["open"])

class listClose(Resource):
    def get(self):
        top = handle(request.args.get("top"))
        return retrieve_json(top, ["close"])

class listClose_json(Resource):
    def get(self):
        top = handle(request.args.get("top"))
        return retrieve_json(top, ["close"])

class listClose_csv(Resource):
    def get(self):
        top = handle(request.args.get("top"))
        return retrieve_csv(top, ["close"])

api.add_resource(listAll, '/listAll')
api.add_resource(listAll_json, '/listAll/json')
api.add_resource(listAll_csv, '/listAll/csv')

api.add_resource(listOpen, '/listOpenOnly')
api.add_resource(listOpen_json, '/listOpenOnly/json')
api.add_resource(listOpen_csv, '/listOpenOnly/csv')

api.add_resource(listClose, '/listCloseOnly')
api.add_resource(listClose_json, '/listCloseOnly/json')
api.add_resource(listClose_csv, '/listCloseOnly/csv')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
