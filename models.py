from peewee import *

db = SqliteDatabase('datatilt.db')

class Tilt(Model):
    name = CharField()
    time = DateTimeField()
    temp = FloatField()
    gravity = FloatField()

    class Meta:
        database = db # This model uses the "datatilt.db" database.

class Bubbler(Model):
    name = CharField()
    starttime = DateTimeField()
    endtime = DateTimeField()
    bubbles = IntegerField()

    class Meta:
        database = db


def initdb():
    db.connect()
    db.create_tables([Tilt, Bubbler], safe=True)
