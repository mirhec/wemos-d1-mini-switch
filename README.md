# Wemos D1 Mini Switch
Wemos D1 Mini based 230V switch programmed with Micropython


- Download the latest firmware from https://github.com/espressif/esptool/
- `sudo pip install esptool`
- `esptool.py --port /dev/tty.wchusbserial1420 --baud 460800 write_flash --flash_size=detect 0 <downloaded-firmware>`
- `pip install click`
- Clone this repo with git or download and extract the source
- Running `python upload.py --port /dev/tty.wchusbserial1420` will start a wizard to upload the necessary files

## After reinstalling OpenHABianPi
Three things need to be done to make it work with the Wemos MQTT server:

1. The IP-Address of the OpenHAB2 server must be the same as before (for static ip edit `/etc/dhcpcd.conf`)
2. The Mosquitto optional component must be installed (with `sudo openhabian-config`)
3. The Mosquitto server must allow anonymous connections. Therefore edit `/etc/mosquitto/mosquitto.conf` and set the last line to `allow_anonymous true`