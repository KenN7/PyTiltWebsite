#!/usr/bin/python2
from __future__ import print_function
import sys
from datetime import datetime
from datetime import timedelta
import time
from Queue import Queue
from random import randint
from sender import Sender

from models import TiltSchema, BubblerSchema

import threading
import socket

import models as models

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


class Bubbler:
    def __init__(self, pin):
        self.pin = pin
        self.lastbubble = datetime.now()
        self.firstbubble = datetime.now()
        self.bubble = 0
        self.server_thread = threading.Thread(target=self.simulator)
        self.server_thread.daemon = True
        self.server_thread.start()

        self.sender = Sender('bubbler',2)

    def simulator(self):
        HOST = '127.0.0.1'
        PORT = 3999
        s = socket.socket()
        s.bind((HOST,PORT))

        s.listen(5)
        while True:
            c, a = s.accept()
            msg = str(c.recv(1024))
            c.send(bytes('GOT: {0}'.format(msg)))
            c.close()
            if msg=="bbbb":
                print('do bubble')
                self.DoBubble()

    def DoBubble(self):
        if (self.bubble == 0):
            self.lastbubble = datetime.now()
            self.firstbubble = datetime.now()
        self.bubble += 1
        print('bb nb:', self.bubble)
        self.lastbubble = datetime.now()

    def monitor(self):
        if ( self.bubble > 0 ):
            m = models.Bubbler(name="0", starttime=self.firstbubble, endtime=datetime.now(), bubbles=self.bubble)
            self.sender.add_data(m.get_dict())
            self.bubble = 0
            print('put in q')



class Tilt:
    def __init__(self, name):
        self.name = name
        self.sender = Sender('tilt',2)

    def simulator(self):
        g = randint(1000,1060)
        t = randint(100,160)
        beacons = [{'uuid':'a495bb10c5b14b44b5121370f02d74de','major':t,'minor':g}]
        return beacons

    def to_celsius(self, fahrenheit):
        return round((fahrenheit - 32.0) / 1.8, 2)

    def monitor(self):
        beacons = self.simulator()
        for beacon in beacons:
            if beacon['uuid'] in TILTS.keys():
                print(beacon['uuid'],self.to_celsius(beacon['major']),beacon['minor'])
                m = models.Tilt(name=TILTS[beacon['uuid']], time=datetime.now(), temp=self.to_celsius(beacon['major']), gravity=beacon['minor'])
                self.sender.add_data(m.get_dict())#, self.schema.dump(m).data))


def monitor():
    bubbler = Bubbler(14)
    tilt = Tilt("Red")

    while True:
        tilt.monitor()
        bubbler.monitor()
        time.sleep(10)


if __name__ == '__main__':
    print('Starting pytilt logger')
    monitor()
