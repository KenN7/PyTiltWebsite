from peewee import *

db = SqliteDatabase('/home/pi/pytilt/datatilt.db')

class Tilt(Model):
    name = CharField()
    time = DateTimeField()
    temp = FloatField()
    gravity = FloatField()

    class Meta:
        database = db # This model uses the "datatilt.db" database.
