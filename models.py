from peewee import *

db = SqliteDatabase('datatilt.db')

class Tilt(Model):
    name = CharField()
    time = DateTimeField()
    temp = FloatField()
    gravity = FloatField()

    class Meta:
        database = db # This model uses the "datatilt.db" database.


def initdb():
    db.connect()
    db.create_tables([Tilt], safe=True)
