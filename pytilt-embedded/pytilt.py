#!/usr/bin/python3
import threading
import time
import os

TIMELOOP = 60
        
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

    tilt_thread = threading.Thread(target=tilt.loop, args=(TIMELOOP,))
    tilt_thread.start()
    # tilt.monitor()
    bubbler_thread = threading.Thread(target=bubbler.loop, args=(TIMELOOP,))
    bubbler_thread.start() 
    # bubbler.monitor()


if __name__ == '__main__':
    btsock = init()
    monitor(btsock)
