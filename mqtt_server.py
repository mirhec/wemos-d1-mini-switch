from umqtt.simple import MQTTClient
from machine import Pin
from mqtt_cfg import TOPIC, SERVER
import os
import micropython
import time
import ubinascii
import machine

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
PIN_MAPPING = {
    0: 16,
    1: 5,
    2: 4,
    3: 0,
    4: 2,
    5: 14,
    6: 12,
    7: 13,
    8: 15
}

states = [1, 1, 1, 1, 1, 1, 1, 1, 1] 

def store_states():
    """This method stores the state of the digital outputs in a file called states.txt"""
    global states
    try:
        with open('states.txt', 'w') as f:
            f.write(str(states))
    except Exception as e:
        print('Exception while storing states: %s' % e)

def load_states():
    """Loads the states from the file states.txt"""
    global states
    try:
        with open('states.txt', 'r') as f:
            s = f.read()
            states = eval(s)
    except Exception as e:
        print('Exception while loading states: %s' % e)

def sub_cb(topic, msg):
    """The msg is in the following format: [gpio]=[command], while gpio is a
    number between 0 and 8, and command can be one of 'on|off|toggle'. If only
    a command is sent, the gpio number is 1, which is by default the gpio connected
    to the relay shield."""
    global states
    print((topic, msg))

    # This is the standard GPIO for the relay shield
    parts = msg.split(b'=')
    gpionum = 1
    if len(parts) == 2:
        gpionum = int(parts[0])
        msg = parts[1]

    gpio = Pin(PIN_MAPPING[gpionum], Pin.OUT, value=1)

    state = states[gpionum]
    if msg == b"on":
        state = 0
        gpio.value(state)
    elif msg == b"off":
        state = 1
        gpio.value(state)
    elif msg == b"toggle":
        state = 1 - state
        gpio.value(state)
    states[gpionum] = state

    store_states()

def start_server(server=SERVER):
    global states

    c = MQTTClient(CLIENT_ID, server)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(TOPIC)
    print("Connected to %s, subscribed to %s topic" % (server, TOPIC))

    load_states()
    gpionum = 0
    for state in states:
        gpio = Pin(PIN_MAPPING[gpionum], Pin.OUT, value=1)
        gpio.value(state)
        gpionum += 1

    return c

if __name__ == '__main__':
    start_server()
