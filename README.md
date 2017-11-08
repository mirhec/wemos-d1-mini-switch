# Wemos D1 Mini Switch
Wemos D1 Mini based 230V switch programmed with Micropython


- Download the latest firmware from https://github.com/espressif/esptool/
- `sudo pip install esptool`
- `esptool.py --port /dev/tty.wchusbserial1420 --baud 460800 write_flash --flash_size=detect 0 <downloaded-firmware>`
- `pip install click`
- Clone this repo with git or download and extract the source
- Running `python upload.py --port /dev/tty.wchusbserial1420` will start a wizard to upload the necessary files
