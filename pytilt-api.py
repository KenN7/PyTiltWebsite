#!/usr/bin/python3
from datetime import datetime

from flask import Flask,request,jsonify
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from marshmallow import Schema, fields, post_load
#from bs4 import BeautifulSoup

#import models
import models_test as models

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('X-PYTILT-KEY', location='headers')

class TesterSchema(Schema):
    name = fields.Str()
    #starttime = fields.DateTime()
    #endtime = fields.DateTime()
    idt = fields.Int()

    @post_load
    def make_bubble(self, data):
        return models.Test(**data)


class TestPut(Resource):
    def get(self):
        user = models.Test.select()
        schema = TesterSchema(many=True)
        result = schema.dump(user)
        return result

    def post(self):
        schema = TesterSchema(many=True)
        user_data = request.get_json()
        print(user_data)
        res = schema.load(user_data)
        print("-----")
        print(res)
        print("-----")
        for r in res.data:
            print(r.name)
            print(r.idt)
            r.save()
        print(request.headers)
        return 200
        #print(args)



class Tilt(Resource):
    def get(self, begindate, enddate):
        d1 = datetime.strptime(begindate, '%Y-%m-%d')
        d2 = datetime.strptime(enddate, '%Y-%m-%d')
        period = models.Tilt.select().where(Tilt.time > d1).where(Tilt.time <= d2)
        return period

class TiltPut(Resource):
    def post(self):
        pass

class Bubbler(Resource):
    def get(self, begindate, enddate):
        d1 = datetime.strptime(begindate, '%Y-%m-%d')
        d2 = datetime.strptime(enddate, '%Y-%m-%d')
        period = models.Tilt.select().where(Tilt.time > d1).where(Tilt.time <= d2)
        return jsondata

class BubblerPut(Resource):
    def post(self):
        pass


api.add_resource(Tilt, '/tilt/<begindate>/<enddate>')
api.add_resource(TiltPut, '/tilt')
api.add_resource(Bubbler, '/bubbler/<begindate>/<enddate>')
api.add_resource(BubblerPut, '/bubbler')

api.add_resource(TestPut, '/test')


if __name__ == '__main__':
    app.run(debug=True)
