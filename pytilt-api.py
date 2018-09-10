#!/usr/bin/python3
from datetime import datetime
from functools import wraps

from flask import Flask,request,jsonify,abort
from flask_restful import Resource, Api
from flask_cors import CORS
#from bs4 import BeautifulSoup
from classes.models import TiltSchema, BubblerSchema

import classes.models as models

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)
#parser = reqparse.RequestParser()
#parser.add_argument('X-PYTILT-KEY', location='headers')

def check_apikey(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if (request.headers.get('X-PYTILT-KEY', None) == '1234'):
            return f(*args, **kwargs)
        else:
            return abort(401) 
    return wrapper


class Tilt(Resource):
    def get(self, begindate, enddate):
        d1 = datetime.strptime(begindate, '%Y-%m-%d')
        d2 = datetime.strptime(enddate, '%Y-%m-%d')
        period = models.Tilt.select().where(Tilt.time > d1).where(Tilt.time <= d2)
        return period

class TiltPut(Resource):
    method_decorators = [check_apikey]
    def post(self):
        schema = TiltSchema(many=True)
        user_data = request.get_json()
        print('uD: ', user_data)
        res = schema.load(user_data)
        print("-----")
        print(res)
        print("-----")
        for r in res.data:
            r.save()
        print(request.headers)
        return 200
        #print(args)

class Bubbler(Resource):
    def get(self, begindate, enddate):
        d1 = datetime.strptime(begindate, '%Y-%m-%d')
        d2 = datetime.strptime(enddate, '%Y-%m-%d')
        period = models.Tilt.select().where(Tilt.time > d1).where(Tilt.time <= d2)
        return jsondata

class BubblerPut(Resource):
    method_decorators = [check_apikey]
    def post(self):
        schema = BubblerSchema(many=True)
        user_data = request.get_json()
        res = schema.load(user_data)
        print("-----")
        print(user_data)
        print(res)
        print("-----")
        for r in res.data:
            r.save()
        print(request.headers)
        return 200
        #print(args)


api.add_resource(Tilt, '/tilt/<begindate>/<enddate>')
api.add_resource(TiltPut, '/tilt')
api.add_resource(Bubbler, '/bubbler/<begindate>/<enddate>')
api.add_resource(BubblerPut, '/bubbler')


if __name__ == '__main__':
    app.run(debug=True)
