#!/usr/bin/python3

from influxdb import InfluxDBClient


class Influxdb:
    def __init__(self, host, port):
        self.host = host #8086
        self.port = port

    def connect(self, db):
        self.client = InfluxDBClient(host=self.host, port=self.port)
        self.client.switch_database(db)

    def write(self, json):
        self.client.write_points(json)

    def connect_write(self, db, json):
        self.connect(db)
        self.write(json)
        self.client.close()

def jsonBubbler(bubblelist):
    l = []
    for b in bubblelist:
        l.append(
            {
                "measurement": "bubble",
                "tags": {
                    "name": b["name"],
                },
                "time": b["endtime"],
                "fields": {
                    "number": b["bubbles"]
                }
            }
        )
    return l


def jsonTilt(tiltlist):
    l = []
    for b in tiltlist:
        l.append(
            {
                "measurement": "tilt",
                "tags": {
                    "name": b["name"],
                },
                "time": b["time"],
                "fields": {
                    "gravity": b["gravity"],
                    "temp": b["temp"]
                }
            }
        )
    return l
