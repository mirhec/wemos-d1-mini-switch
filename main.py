import machine

def wlan_config():
    try:
        from wlan_cfg import SSID, SSID_PWD
        import network

        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            print('connecting to network...')
            sta_if.active(True)
            sta_if.connect(SSID, SSID_PWD)
            while not sta_if.isconnected():
                pass
        print('network config:', sta_if.ifconfig())

        return True
    except:
        print('Need to setup WLAN configuration:')
        ssid = input(' -> SSID to connect to: ')
        pwd = input(' -> Password for this SSID: ')

        with open('wlan_cfg.py', 'w') as f:
            f.write("SSID='%s'\n" % ssid)
            f.write("SSID_PWD='%s'\n" % pwd)
        
        return False

def mqtt_config():
    try:
        # Try getting the mqtt settings
        from mqtt_cfg import SERVER, TOPIC
        print('Loaded mqtt config ...')
        return True
    except:
        # do first initialization
        print('Need to setup MQTT configuration:')
        server = input(' -> MQTT Server: ')
        topic = input(' -> MQTT topic to subscribe to: ')

        with open('mqtt_cfg.py', 'w') as f:
            f.write("SERVER='%s'\n" % server)
            f.write("TOPIC=b'%s'\n" % topic)
        
        return False

def webrepl_config():
    try:
        from webrepl_cfg import PASS
        print('Loaded webrepl config ...')
        return True
    except:
        print('Need to setup WebREPL configuration:')

        webreplpass = input(' -> WebREPL password: ')

        with open('webrepl_cfg.py', 'w') as f:
            f.write("PASS = '%s'\n" % webreplpass)
        
        return False


result1 = wlan_config()
result2 = mqtt_config()
result3 = webrepl_config()

if not result1 or not result2 or not result3:
    # Do a hard reset
    machine.reset()
else:
    from mqtt_server import start_server
    start_server()
