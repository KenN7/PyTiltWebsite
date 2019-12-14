#!/usr/bin/python3
import sys
from datetime import datetime
from classes.sender import Sender
import classes.models as models

TILTS = {
        'a495bb10c5b14b44b5121370f02d74de': 'Red',
        'a495bb20c5b14b44b5121370f02d74de': 'Green',
        'a495bb30c5b14b44b5121370f02d74de': 'Black',
        'a495bb40c5b14b44b5121370f02d74de': 'Purple',
        'a495bb50c5b14b44b5121370f02d74de': 'Orange',
        'a495bb60c5b14b44b5121370f02d74de': 'Blue',
        'a495bb70c5b14b44b5121370f02d74de': 'Yellow',
        'a495bb80c5b14b44b5121370f02d74de': 'Pink',
}

class BubblerBase(object):
    def __init__(self, pin):
        self.pin = pin
        self.lastbubble = datetime.utcnow()
        self.firstbubble = datetime.utcnow()
        self.bubble = 0

        self.sender = Sender('bubbler',10)
        self.schema = models.BubblerSchema()

    def DoBubble(self):
        if (self.bubble == 0):
            self.lastbubble = datetime.utcnow()
            self.firstbubble = datetime.utcnow()
        self.bubble += 1
        self.lastbubble = datetime.utcnow()

    def monitor(self):
        if ( self.bubble > 0 ):
            # m = models.Bubbler(name="0", starttime=self.firstbubble, endtime=datetime.utcnow(), bubbles=self.bubble)
            m = dict(name="0", starttime=self.firstbubble, endtime=datetime.utcnow(), bubbles=self.bubble)
            self.sender.add_data(self.schema.dump(m))
            self.bubble = 0
            #print('put in q')


class TiltBase(object):
    def __init__(self, name):
        self.name = name
        self.sender = Sender('tilt',10)
        self.schema = models.TiltSchema()

    def distinct(self, objects):
        seen = set()
        unique = []
        for obj in objects:
            if obj['uuid'] not in seen:
                unique.append(obj)
                seen.add(obj['uuid'])
        return unique

    def to_celsius(self, fahrenheit):
        return round((fahrenheit - 32.0) / 1.8, 2)

    def get_data(self):
        print('Must define')

    def monitor(self):
        beacons = self.get_data()
        for beacon in beacons:
            if beacon['uuid'] in TILTS.keys():
                print(beacon['uuid'],self.to_celsius(beacon['major']),beacon['minor'])
                # m = models.Tilt(name=TILTS[beacon['uuid']], time=datetime.utcnow(), temp=self.to_celsius(beacon['major']), gravity=beacon['minor'])
                m = dict(name=TILTS[beacon['uuid']], time=datetime.utcnow(), temp=self.to_celsius(beacon['major']), gravity=beacon['minor'])
                print(self.schema.dump(m))
                self.sender.add_data(self.schema.dump(m))
