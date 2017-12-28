from __future__ import print_function
import os
import click
import platform
from ampy import pyboard, files

def windows_full_port_name(portname):
    # Helper function to generate proper Windows COM port paths.  Apparently
    # Windows requires COM ports above 9 to have a special path, where ports below
    # 9 are just referred to by COM1, COM2, etc. (wacky!)  See this post for
    # more info and where this code came from:
    # http://eli.thegreenplace.net/2009/07/31/listing-all-serial-ports-on-windows-with-python/
    m = re.match('^COM(\d+)$', portname)
    if m and int(m.group(1)) < 10:
        return portname
    else:
        return '\\\\.\\{0}'.format(portname)

def wlan_config():
    try:
        from wlan_cfg import SSID, SSID_PWD
        print('Loaded wlan config ...')
        return True
    except:
        print('Need to setup WLAN configuration:')
        ssid = input(' -> SSID to connect to: ')
        pwd = input(' -> Password for this SSID: ')
        hostname = input(' -> Hostname: ')

        with open('wlan_cfg.py', 'w') as f:
            f.write("SSID='%s'\n" % ssid)
            f.write("SSID_PWD='%s'\n" % pwd)
            f.write("HOSTNAME='%s'\n" % hostname)
        
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

def temp_config():
    try:
        # Try getting the temp settings
        from temp_cfg import TOPIC, PIN
        print('Loaded temp config ...')
        return True
    except:
        # do first initialization
        yesno = input('Do you want to setup the temperature config (y/n)? ')
        print(yesno)
        if yesno is 'y':
            topic = input(' -> MQTT topic to send temperature to: ')
            pin = input(' -> Pin the DS18B20 is connected to: ')

            with open('temp_cfg.py', 'w') as f:
                f.write("TOPIC=b'%s'\n" % topic)
                f.write("PIN='%s'\n" % pin)
        
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

def upload(locals):
    for local in locals:
        print('upload %s ... ' % local, end='')

        # Use the local filename if no remote filename is provided.
        remote = os.path.basename(os.path.abspath(local))

        # Check if path is a folder and do recursive copy of everything inside it.
        # Otherwise it's a file and should simply be copied over.
        if os.path.isdir(local):
            # Directory copy, create the directory and walk all children to copy
            # over the files.
            board_files = files.Files(_board)
            for parent, child_dirs, child_files in os.walk(local):
                # Create board filesystem absolute path to parent directory.
                remote_parent = posixpath.normpath(posixpath.join(remote, os.path.relpath(parent, local)))
                try:
                    # Create remote parent directory.
                    board_files.mkdir(remote_parent)
                    # Loop through all the files and put them on the board too.
                    for filename in child_files:
                        with open(os.path.join(parent, filename), 'rb') as infile:
                            remote_filename = posixpath.join(remote_parent, filename)
                            board_files.put(remote_filename, infile.read())
                except files.DirectoryExistsError:
                    # Ignore errors for directories that already exist.
                    pass

        elif os.path.exists(local):
            # File copy, open the file and copy its contents to the board.
            # Put the file on the board.
            with open(local, 'rb') as infile:
                board_files = files.Files(_board)
                board_files.put(remote, infile.read())
        print('done.')

@click.command()
@click.option('--port', '-p', envvar='AMPY_PORT', required=True, type=click.STRING,
              help='Name of serial port for connected board.  Can optionally specify with AMPY_PORT environemnt variable.',
              metavar='PORT')
@click.option('--baud', '-b', envvar='AMPY_BAUD', default=115200, type=click.INT,
              help='Baud rate for the serial connection (default 115200).  Can optionally specify with AMPY_BAUD environment variable.',
              metavar='BAUD')
@click.version_option()
def cmd(port, baud):
    """upload - Uploads all files for the wemos switch."""
    global _board
    # On Windows fix the COM port path name for ports above 9 (see comment in
    # windows_full_port_name function).
    if platform.system() == 'Windows':
        port = windows_full_port_name(port)
    _board = pyboard.Pyboard(port, baudrate=baud)

    main()


def main():
    global _board

    # Read configuration or create a new one
    wlan_config()
    mqtt_config()
    webrepl_config()
    temp_config()

    # Upload the necessary files
    upload(['wlan_cfg.py', 'mqtt_cfg.py', 'webrepl_cfg.py', 'temp_cfg.py', 'boot.py', 'mqtt_server.py', 'main.py'])


if __name__ == '__main__':
    cmd()
    # global _board
    # if platform.system() == 'Windows':
    #     port = windows_full_port_name(port)
    # _board = pyboard.Pyboard('/dev/tty.wchusbserial1420', baudrate=115200)

    # main()
