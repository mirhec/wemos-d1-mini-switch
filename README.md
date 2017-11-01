# Wemos D1 Mini Switch
Wemos D1 Mini based 230V switch programmed with Micropython


- Download the latest firmware from https://github.com/espressif/esptool/
- `sudo pip install esptool`
- `esptool.py --port /dev/tty.wchusbserial1420 --baud 460800 write_flash --flash_size=detect 0 <downloaded-firmware>`
- Connect to Wemos D1 with screen: `screen /dev/tty.wchusbserial1420 115200`. Note: You can exit the session with `CTRL+A K`
- Start the WebREPL by typing in `import webrepl_setup`
- Open your Browser at http://micropython.org/webrepl/
- Then connect your PC to the WLAN `MicroPython-xxxxxx`. The password is `micropythoN`
- Now in the WebREPL in your browser click connect, type in your password and upload the following files from this repository:
  - boot.py
  - main.py
  - mqtt_server.py
- Restart your D1 mini and connect again via screen: `screen /dev/tty.wchusbserial1420 115200`
- Now you can setup your switch

Note: You could also use adafruits ampy tool in order to upload the files to your Wemos (installation instructions are [here](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy)). If you encounter problems, try this solution: https://github.com/adafruit/ampy/issues/19#issuecomment-317126363
