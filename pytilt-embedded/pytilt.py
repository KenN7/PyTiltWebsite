#!/usr/bin/python2
from __future__ import print_function
import time

## for real device
# from classes.raspi_classes import BubblerRaspi as Bubbler
# from classes.raspi_classes import TiltRaspi as Tilt
# from classes.raspi_classes import init

## for simulation
from classes.sim_classes import BubblerSim as Bubbler
from classes.sim_classes import TiltSim as Tilt
from classes.sim_classes import init


def monitor():
    bubbler = Bubbler(14)
    tilt = Tilt("Red")

    while True:
        tilt.monitor()
        bubbler.monitor()
        time.sleep(10)


if __name__ == '__main__':
    init()
    monitor()
