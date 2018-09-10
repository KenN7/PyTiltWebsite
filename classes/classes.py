#!/usr/bin/python
from __future__ import print_function
from __future__ import absolute_import
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
        self.lastbubble = datetime.now()
        self.firstbubble = datetime.now()
        self.bubble = 0

        self.sender = Sender('bubbler',2)

    def DoBubble(self):
        if (self.bubble == 0):
            self.lastbubble = datetime.now()
            self.firstbubble = datetime.now()
        self.bubble += 1
        #print('bb nb:', self.bubble)
        self.lastbubble = datetime.now()

    def monitor(self):
        if ( self.bubble > 0 ):
            m = models.Bubbler(name="0", starttime=self.firstbubble, endtime=datetime.now(), bubbles=self.bubble)
            self.sender.add_data(m.get_dict())
            self.bubble = 0
            #print('put in q')



class TiltBase(object):
    def __init__(self, name):
        self.name = name
        self.sender = Sender('tilt',2)

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
                m = models.Tilt(name=TILTS[beacon['uuid']], time=datetime.now(), temp=self.to_celsius(beacon['major']), gravity=beacon['minor'])
                self.sender.add_data(m.get_dict())#, self.schema.dump(m).data))