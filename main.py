import machine
import time
import network
from mqtt_server import start_server, send_temp
import micropython

micropython.alloc_emergency_exception_buf(100)

def wlan_config():
    try:
        from wlan_cfg import SSID, SSID_PWD, HOSTNAME

        sta_ap = network.WLAN(network.AP_IF)
        sta_ap.active(False)

        return True
    except Exception as e:
        print(e)
        return False

def mqtt_config():
    try:
        # Try getting the mqtt settings
        from mqtt_cfg import SERVER, TOPIC
        print('Loaded mqtt config ...')
        return True
    except:
        return False

def webrepl_config():
    try:
        from webrepl_cfg import PASS
        print('Loaded webrepl config ...')
        return True
    except:
        return False


if not wlan_config():
    print('could not connect to WLAN!')
elif not mqtt_config():
    print('could not load MQTT config!')
elif not webrepl_config():
    print('could not load WebREPL config!')
else:
    try:
        sta_if = network.WLAN(network.STA_IF)

        server = None
        while 1:
            try:
                if not sta_if.isconnected():
                    print('connecting to network...')
                    from wlan_cfg import SSID, SSID_PWD, HOSTNAME
                    sta_if.active(True)
                    sta_if.connect(SSID, SSID_PWD)
                    sta_if.config(dhcp_hostname=HOSTNAME)
                    count = 0
                    while not sta_if.isconnected() and count < 50:
                        time.sleep(.1)
                        count += 1
                    if not sta_if.isconnected():
                        raise Exception('could not connect to WLAN!')

                if server is None:
                    print('connecting to mosquitto ...')
                    server = start_server()
                    if server is not None:
                        print('done!')
                else:
                    server.check_msg()
                    send_temp(server)
            except Exception as e:
                print(e)

            time.sleep(.1)
    except Exception as e:
        raise e
