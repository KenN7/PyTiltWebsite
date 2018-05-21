#!/usr/bin/python2

from __future__ import print_function
import sys
from datetime import datetime
from datetime import timedelta
import time
from Queue import Queue

import models_test as models


class Bubbler:
    def __init__(self, pin, queue):
        self.pin = pin
        self.q = queue

    def bubble(self):
        print('bubble')
        self.q.put(models.Test(name='{}'.format(self.pin)))

class Tilt:
    def __init__(self, name, queue):
        self.name = name
        self.q = queue

    def monitor(self):
        print("monitor tilt")
        self.q.put(models.Test(name=self.name))


def monitor():
    #sender = Sender()
    q = Queue()
    bubbler = Bubbler('gg', q)
    tilt = Tilt("a4", q)

    while True:
        tilt.monitor()
        bubbler.bubble()
        bubbler.bubble()
        time.sleep(1)
        print('saving')
        print(q.qsize())
        print(q.empty())
        while(q.empty() != True):
            r = q.get()
            print(r)
            r.save()
        print("saved")
        time.sleep(10)


if __name__ == '__main__':
    monitor()
