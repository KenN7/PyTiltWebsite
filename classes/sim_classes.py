#!/usr/bin/python
from __future__ import absolute_import
from classes.classes import TiltBase, BubblerBase
from random import randint
import threading
import socket

class BubblerSim(BubblerBase):
    def __init__(self, *args, **kwargs):
        super(BubblerSim, self).__init__(*args, **kwargs)
        self.server_thread = threading.Thread(target=self.simulator)
        self.server_thread.daemon = True
        self.server_thread.start()

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


class TiltSim(TiltBase):
    def __init__(self, *args, **kwargs):
        super(TiltSim, self).__init__(*args, **kwargs)

    def simulator(self):
        g = randint(1000,1060)
        t = randint(100,160)
        beacons = [{'uuid':'a495bb10c5b14b44b5121370f02d74de','major':t,'minor':g}]
        return beacons

    def get_data(self):
        return self.simulator()


def init():
    print("Started Simulator device..")