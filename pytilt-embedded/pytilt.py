#!/usr/bin/python3
import time
import os
        
SIM = os.environ.get('PYTILT_SIMULATE', None)
if SIM == "FALSE":
    print("Using real device..")
    from classes.raspi_classes import BubblerRaspi as Bubbler
    from classes.raspi_classes import TiltRaspi as Tilt
    from classes.raspi_classes import init
else:
    print("Using simulation..")
    from classes.sim_classes import BubblerSim as Bubbler
    from classes.sim_classes import TiltSim as Tilt
    from classes.sim_classes import init

def monitor(btsock):
    bubbler = Bubbler(14)
    tilt = Tilt("Red", btsock)

    while True:
        tilt.monitor()
        bubbler.monitor()
        time.sleep(10)


if __name__ == '__main__':
    btsock = init()
    monitor(btsock)
