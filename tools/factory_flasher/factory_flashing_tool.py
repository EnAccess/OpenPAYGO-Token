import sys
import csv
import serial
from serial.tools import list_ports
import time
import configparser

CONF_FILE = 'factory_flashing_tool.conf'


def raw_input():
    return sys.stdin.readline().replace('\n', '')


def flash_device(serial_number, starting_code, key, port, baud):
    clean_key = " ".join(key[i:i+2] for i in range(0, len(key), 2))
    print('Flashing device with serial number: '+serial_number+', starting_code: '+str(starting_code)+', key: '+str(clean_key))
    flashed = False
    with serial.Serial(port, baud, timeout=5) as uart:
        uart.write(('#'+str(serial_number)+';'+str(starting_code)+';'+clean_key).encode('ascii'))
        time.sleep(0.25)
        flashed = True
    if flashed:
        print('Finished Flashing! Check that the device is correctly setup. \n')
    else:
        print('ERROR: Could not connect to the device, please try again! \n')


def setup_conf(config):
    print('--- Setup ---')
    config['BASE_CONFIG'] = {}
    base_config = config['BASE_CONFIG']
    print('Available UART interfaces: ')
    list_ports.main()
    time.sleep(1)
    print('Enter the name of the UART interface to use (copy paste from list above): ')
    port = raw_input()
    print('Enter the baud rate to use (e.g. 9600): ')
    baud = raw_input()
    base_config['port'] = port
    base_config['baud'] = baud
    with open(CONF_FILE, 'w') as configfile:
        config.write(configfile)


if __name__ == '__main__':
    print('--- OpenPAYGO Token - Factory Flashing Tool ---')
    print('This is meant to be used with the OpenPAYGO Arduino example or a device using the same UART protocol.')
    config = configparser.ConfigParser()
    config.read(CONF_FILE)
    if not 'BASE_CONFIG' in config:
        setup_conf(config)
    base_config = config['BASE_CONFIG']
    port = base_config['port']
    baud = int(base_config['baud'])
    print('Enter the path to the csv file you want to load: ')
    csv_file = raw_input()
    with open(csv_file, newline='') as csvfile:
        device_list_csv = csv.reader(csvfile)
        device_data_dict = {serial_number: (starting_code, key) for
                            serial_number, starting_code, key, c, t, r, h, f in list(device_list_csv)}
    print('CSV file loaded! ')
    while(1):
        print('To flash a device, make sure the device is connected and enter the serial number of the device you want to flash: ')
        print('You can press Ctrl+C to quit. ')
        serial_number = raw_input()
        this_device_data = device_data_dict.get(serial_number)
        if not this_device_data:
            print('ERROR: Device is not in list!')
        else:
            flash_device(serial_number, this_device_data[0], this_device_data[1], port, baud)