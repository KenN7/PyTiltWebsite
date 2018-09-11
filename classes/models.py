#!/usr/bin/python
from __future__ import absolute_import
from peewee import *
from marshmallow import Schema, fields, post_load, pre_dump, utils

from classes.sender import Sender

db = SqliteDatabase('datatilt.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64,  # 64MB
    'foreign_keys': 1,  # Enforce foreign-key constraints
})

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

    def __repr__(self):
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

    @pre_dump(pass_many=True)
    def rewrite_datetime(self, data, many):
        if many:
            for d in data:
                d.time = utils.from_iso(d.time)
        else:
            data.time = utils.from_iso(data.time)


class Bubbler:
    def __init__(self, name, starttime, endtime, bubbles):
        self.dbitem = BubblerDB(name=name, starttime=starttime, endtime=endtime, bubbles=bubbles)
        self.schema = BubblerSchema()

    def get_dict(self):
        return self.schema.dump(self.dbitem).data

    def __repr__(self):
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

    @pre_dump(pass_many=True)
    def rewrite_datetime(self, data, many):
        if many:
            for d in data:
                d.starttime = utils.from_iso(d.starttime)
                d.endtime = utils.from_iso(d.endtime)
        else:
            data.starttime = utils.from_iso(data.starttime)
            data.endtime = utils.from_iso(data.endtime)


def initdb():
    db.connect()
    db.create_tables([TiltDB, BubblerDB], safe=True)

if __name__ == '__main__':
    # Read the value of several pragmas:
    initdb()
    print('cache_size:', db.cache_size)
    print('foreign_keys:', db.foreign_keys)
    print('journal_mode:', db.journal_mode)
    print('page_size:', db.page_size)
