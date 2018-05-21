#!/usr/bin/python2
import sys
from datetime import datetime
from datetime import timedelta
import time
from Queue import Queue

import bluetooth._bluetooth as bluez # bluetooth

import blescan # bluetooth get
from gpiozero import Button #gpio of rpizero
#from sender import Sender

import models

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
    def __init__(self, pin, queue):
        self.pin = pin
        self.bubbler = Button(pin)
        self.bubbler.when_pressed = self.bubble()
        self.lastbubble = datetime.now()
        self.firstbubble = datetime.now()
        self.bubble = 0
        self.q = queue

    def bubble(self):
        if (bubble == 0):
            self.lastbubble = datetime.now()
            self.firstbubble = datetime.now()
        if (datetime.now() - self.lastbubble < timedelta(0, 20)):
            self.bubble += 1
        else:
            self.q.put(models.Bubbler(name="0", starttime=self.firstbubble, endtime=datetime.now(), bubbles=self.bubble))
            # r = models.Bubbler(name=0, starttime=self.firstbubble, endtime=datetime.now(), bubbles=self.bubble)
            # r.save()
            self.bubble = 0 #save and send data
        self.lastbubble = datetime.now()


class Tilt:
    def __init__(self, name, queue):
        self.name = name
        self.q = queue

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

    def monitor(self):
        beacons = self.distinct(blescan.parse_events(sock, 10))
        for beacon in beacons:
            if beacon['uuid'] in TILTS.keys():
                print(beacon['uuid'],to_celsius(beacon['major']),beacon['minor'])
                self.q.put(models.Tilt(name=TILTS[beacon['uuid']], time=datetime.now(), temp=to_celsius(beacon['major']), gravity=beacon['minor']))
                # r = models.Tilt(name=TILTS[beacon['uuid']], time=datetime.now(), temp=to_celsius(beacon['major']), gravity=beacon['minor'])
                # r.save()
                # sender.add_data({
                #     'color': TILTS[beacon['uuid']],
                #     'timestamp': datetime.datetime.now().isoformat(),
                #     'temp': to_celsius(beacon['major']),
                #     'gravity': beacon['minor']
                # })



def monitor():
    #sender = Sender()
    q = Queue()
    bubbler = Bubbler(14, q)
    tilt = Tilt("Red", q)

    while True:
        tilt.monitor()
        time.sleep(10)
        while(q.empty() != True):
            r = q.get()
            r.save()


if __name__ == '__main__':
    dev_id = 0
    try:
        sock = bluez.hci_open_dev(dev_id)
        print('Starting pytilt logger')
    except:
        print('error accessing bluetooth device...')
        sys.exit(1)

    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)
    monitor()
