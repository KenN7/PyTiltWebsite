#!/usr/bin/python
from __future__ import absolute_import
from classes.classes import TiltBase, BubblerBase
from gpiozero import Button #gpio of rpizero

import bluetooth._bluetooth as bluez # bluetooth
import blescan # bluetooth get

class BubblerRaspi(BubblerBase):
    def __init__(self, *args, **kwargs):
        super(BubblerRaspi, self).__init__(*args, **kwargs)
        self.bubbler = Button(self.pin)
        self.bubbler.when_pressed = self.DoBubble()


class TiltRaspi(TiltBase):
    def __init__(self, *args, **kwargs):
        super(TiltRaspi, self).__init__(*args, **kwargs)

    def get_data(self):
        return self.distinct(blescan.parse_events(sock, 10))

def init():
    dev_id = 0
    try:
        sock = bluez.hci_open_dev(dev_id)
        print('Starting pytilt logger')
    except:
        print('error accessing bluetooth device...')
        sys.exit(1)
    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)
    print("Started physical device..")
