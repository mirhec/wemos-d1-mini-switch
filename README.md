# Wemos D1 Mini Switch
Wemos D1 Mini based 230V switch programmed with Micropython


- Download the latest firmware from https://github.com/espressif/esptool/
- `sudo pip install esptool`
- `esptool.py --port /dev/tty.wchusbserial1420 --baud 460800 write_flash --flash_size=detect 0 <downloaded-firmware>`
- Connect to Wemos D1 with screen: `screen /dev/tty.wchusbserial1420 115200`
- Start the WebREPL by typing in `import webrepl_setup`
- Open your Browser at http://micropython.org/webrepl/
- Then connect your PC to the WLAN `MicroPython-xxxxxx`. The password is `micropythoN`
- Now in the WebREPL in your browser click connect, type in your password and upload the following files from this repository:
  - boot.py
  - main.py
  - mqtt_server.py
- Restart your D1 mini and connect again via screen: `screen /dev/tty.wchusbserial1420 115200`
- Now you can setup your switch
