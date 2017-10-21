from umqtt.simple import MQTTClient
from machine import Pin
from mqtt_cfg import TOPIC, SERVER
import micropython
import time
import ubinascii
import machine

CLIENT_ID = ubinascii.hexlify(machine.unique_id())

# ESP8266 ESP-12 modules have blue, active-low LED on GPIO2, replace
# with something else if needed.
led = Pin(2, Pin.OUT, value=1)
gpio = Pin(5, Pin.OUT, value=1)

state = 0

def sub_cb(topic, msg):
    global state
    print((topic, msg))
    if msg == b"on":
        led.value(0)
        state = 1
        gpio.value(state)
    elif msg == b"off":
        led.value(1)
        state = 0
        gpio.value(state)
    elif msg == b"toggle":
        # LED is inversed, so setting it to current state
        # value will make it toggle
        led.value(state)
        state = 1 - state
        gpio.value(state)

def start_server(server=SERVER):
    c = MQTTClient(CLIENT_ID, server)
    # Subscribed messages will be delivered to this callback
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(TOPIC)
    print("Connected to %s, subscribed to %s topic" % (server, TOPIC))

    led.value(1)
    gpio.value(0)

    try:
        while 1:
            # blocking wait for message
            c.wait_msg()
    finally:
        C.disconnect()

if __name__ == '__main__':
    start_server()
