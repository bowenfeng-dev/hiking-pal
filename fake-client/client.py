from pubnub import Pubnub
from threading import Timer

import json;
import random;
import requests;


SEND_INTERVAL = 1  # 1 msg/s

pubnub = Pubnub(
    publish_key="pub-c-8d79e7cc-4b74-4696-b150-ff4f13b0215a",
    subscribe_key="sub-c-aaa49242-c57e-11e6-b8a7-0619f8945a4f")

random.seed()

hid = 1482469716790
sid = 0
sname = 'pyclient-{0}'.format(random.randint(100, 999))

lat = 40.705311
lng = -74.258188

def callback(message, channel):
    print(message)


def error(message):
    print("ERROR : " + str(message))


def connect(message):
    print("CONNECTED")
    send_location()



def send_location():
    global lat
    global lng
    lat = lat + (random.randint(100, 999) - 300) / 1000000.0
    lng = lng + (random.randint(100, 999) - 400) / 1000000.0

    print pubnub.publish(
        channel='moves',
        message={
            'hiking': str(hid),
            'session': str(sid),
            'name': sname,
            'gps': {
                'lat': lat,
                'lng': lng}})
    Timer(SEND_INTERVAL, send_location).start()

def reconnect(message):
    print("RECONNECTED")


def disconnect(message):
    print("DISCONNECTED")


def join_hiking():
    base_url = 'http://run-west.att.io'
    flow_path = '/d591dcc0c690f/e8a5c1efc6e6/408869f220ca798/in/flow'
    endpoint = '/hikings/{0}/sessions'.format(hid)
    join_url = base_url + flow_path + endpoint
    r = requests.put(join_url, data={'name': sname})
    print(r.json())
    global sid
    sid = r.json()['id']



join_hiking()

pubnub.subscribe(channels='moves', callback=callback, error=callback,
                 connect=connect, reconnect=reconnect, disconnect=disconnect)


