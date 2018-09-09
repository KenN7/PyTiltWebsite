#!/usr/bin/python
from peewee import *
from marshmallow import Schema, fields, post_load

from sender import Sender

db = SqliteDatabase('datatilt.db')

class Tilt:
    def __init__(self, name, time, temp, gravity):
        self.dbitem = TiltDB(name=name, time=time, temp=temp, gravity=gravity)
        self.schema = TiltSchema()

    def get_dict(self):
        return self.schema.dump(self.dbitem).data

    def __str__(self):
        return "{}:{}:{}".format(self.name,self.time,self.gravity)

class TiltDB(Model):
    name = CharField()
    time = DateTimeField()
    temp = FloatField()
    gravity = FloatField()

    def __str__(self):
        return "{}:{}:{}".format(self.name,self.time,self.gravity)

    class Meta:
        database = db # This model uses the "datatilt.db" database.

class TiltSchema(Schema):
    name = fields.Str()
    time = fields.DateTime()
    temp = fields.Float()
    gravity = fields.Float()

    @post_load
    def make_tilt(self, data):
        return TiltDB(**data)


class Bubbler:
    def __init__(self, name, starttime, endtime, bubbles):
        self.dbitem = BubblerDB(name=name, starttime=starttime, endtime=endtime, bubbles=bubbles)
        self.schema = BubblerSchema()

    def get_dict(self):
        return self.schema.dump(self.dbitem).data

    def __str__(self):
        return "{}:{}:{}".format(self.name,self.starttime,self.bubbles)


class BubblerDB(Model):
    name = CharField()
    starttime = DateTimeField()
    endtime = DateTimeField()
    bubbles = IntegerField()

    def __str__(self):
        return "{}:{}:{}".format(self.name,self.starttime,self.bubbles)

    class Meta:
        database = db

class BubblerSchema(Schema):
    name = fields.Str()
    starttime = fields.DateTime()
    endtime = fields.DateTime()
    bubbles = fields.Int()

    @post_load
    def make_bubble(self, data):
        return BubblerDB(**data)


def initdb():
    db.connect()
    db.create_tables([TiltDB, BubblerDB], safe=True)

if __name__ == '__main__':
    initdb()
