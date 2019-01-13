#!/usr/bin/python
from __future__ import absolute_import
from peewee import *
from marshmallow import Schema, fields, post_load, pre_dump, utils
import datetime

from classes.sender import Sender

db = SqliteDatabase('datatilt.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64,  # 64MB
    'foreign_keys': 1,  # Enforce foreign-key constraints
})

dbbeer = SqliteDatabase('databeers.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64,  # 64MB
    'foreign_keys': 1,  # Enforce foreign-key constraints
})

class Beer(Model):
    name = CharField()
    comment = CharField()
    begin = DateTimeField()
    end = DateTimeField()
    bflink = CharField()

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        database = dbbeer # This model uses the "datatilt.db" database.


class Tilt(Model):
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
        return Tilt(**data)

    @pre_dump(pass_many=True)
    def rewrite_datetime(self, data, many):
        if many:
            for d in data:
                if type(d.time) is not datetime.datetime:
                    d.time = utils.from_iso(d.time)
        elif type(data.time) is not datetime.datetime:
                data.time = utils.from_iso(data.time)


class Bubbler(Model):
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
        return Bubbler(**data)

    @pre_dump(pass_many=True)
    def rewrite_datetime(self, data, many):
        if many:
            for d in data:
                if type(d.starttime) is not datetime.datetime:
                    d.starttime = utils.from_iso(d.starttime)
                if type(d.endtime) is not datetime.datetime:
                    d.endtime = utils.from_iso(d.endtime)
        elif type(data.starttime) is not datetime.datetime:
            data.starttime = utils.from_iso(data.starttime)
        elif type(data.endtime) is not datetime.datetime:
            data.endtime = utils.from_iso(data.endtime)


def initdb():
    db.connect()
    db.create_tables([Tilt, Bubbler], safe=True)
    dbbeer.connect()
    dbbeer.create_tables([Beer], safe=True)

if __name__ == '__main__':
    # Read the value of several pragmas:
    initdb()
    print('cache_size:', db.cache_size)
    print('foreign_keys:', db.foreign_keys)
    print('journal_mode:', db.journal_mode)
    print('page_size:', db.page_size)
