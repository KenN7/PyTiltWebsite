#!/usr/bin/python3
from datetime import datetime
from functools import wraps

from flask import Flask,request,jsonify,abort
from flask_restful import Resource, Api
from flask_cors import CORS
#from classes.models import TiltSchema, BubblerSchema
#import classes.models as models
from influxmodels import Influxdb,jsonBubbler,jsonTilt
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)

influxdb = Influxdb("influxdb", 8086)

def check_apikey(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if (request.headers.get('X-PYTILT-KEY', None) == os.environ.get('PYTILT_KEY', None)):
            return f(*args, **kwargs)
        else:
            return abort(401)
    return wrapper


class Tilt(Resource):
    method_decorators = [check_apikey]
    def get(self, begindate=None, enddate=None):
        pass
        # d1 = datetime.strptime(begindate, '%Y-%m-%d')
        # d2 = datetime.strptime(enddate, '%Y-%m-%d')
        # period = models.Tilt.select().where(models.Tilt.time > d1).where(models.Tilt.time <= d2)
        # schema = TiltSchema(many=True)
        # items,e = schema.dump(list(period))
        # return jsonify(items)

    def post(self):
        # schema = TiltSchema(many=True)
        user_data = request.get_json()
        #res = schema.load(user_data)
        # print(user_data)
        #print(res)
        influxdb.connect_write('hoplab',jsonTilt(user_data))
        #for r in res.data:
        #    r.save()
        print(request.headers)
        return 200

class Bubbler(Resource):
    method_decorators = [check_apikey]
    def get(self, begindate, enddate):
        pass
        # d1 = datetime.strptime(begindate, '%Y-%m-%d')
        #d2 = datetime.strptime(enddate, '%Y-%m-%d')
        #period = models.Bubbler.select().where(models.Bubbler.starttime > d1).where(models.Bubbler.starttime <= d2)
        #schema = BubblerSchema(many=True)
        #items,e = schema.dump(list(period))
        ##print(e)
        #return jsonify(items)

    def post(self):
        # schema = BubblerSchema(many=True)
        user_data = request.get_json()
        #res = schema.load(user_data)
        # print(user_data)
        #print(res)

        influxdb.connect_write('hoplab',jsonBubbler(user_data))
        #for r in res.data:
        #    r.save()
        print(request.headers)
        return 200

api.add_resource(Tilt, '/tilt/<begindate>/<enddate>', '/tilt')
api.add_resource(Bubbler, '/bubbler/<begindate>/<enddate>', '/bubbler')


if __name__ == '__main__':
    app.run(debug=True)
