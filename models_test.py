from peewee import *

db = SqliteDatabase('datatest_test.db')

class Test(Model):
    idt = IntegerField()
    name = CharField()

    class Meta:
        database = db


def initdb():
    db.connect()
    db.create_tables([Test], safe=True)

if __name__ == '__main__':
    initdb()
