import sys
import os
import random
import csv
import codecs
import configparser

CONF_FILE = 'openpaygo_csv_generator.conf'


def raw_input():
    return sys.stdin.readline().replace('\n', '')


def number_to_serial(manufacturer_prefix, number):
    return manufacturer_prefix + str(number).zfill(9)


def generate_csv(serial_start, number_of_devices, config):
    base_config = config['BASE_CONFIG']
    # We load the config
    manufacturer_prefix = base_config['manufacturer_prefix']
    count = 1
    time_divider = base_config['time_divider']
    restricted_digit_set = base_config['restricted_digit_set']
    hardware_model = base_config['hardware_model']
    firmware_version = base_config['firmware_version']
    filename = 'openpaygo_batch_' + number_to_serial(manufacturer_prefix, serial_start+1) + '-' + \
               number_to_serial(manufacturer_prefix, serial_start+number_of_devices) + '.csv'
    with open(filename, 'w') as csvfile:
        device_list_csv = csv.writer(csvfile, delimiter=',')
        headers = ['Serial Number', 'Starting Code', 'Key', 'Count', 'Time Divider', 'Restricted Digit Mode',
                   'Hardware Model', 'Firmware Version']
        device_list_csv.writerow(headers)
        for number in range(1, number_of_devices+1):
            device_serial = number_to_serial(manufacturer_prefix, number)
            starting_code = random.randint(1, 999999999)
            key = codecs.encode(os.urandom(16), 'hex').decode('utf-8')
            device_data = [device_serial, starting_code, key, count, time_divider, restricted_digit_set,
                           hardware_model, firmware_version]
            device_list_csv.writerow(device_data)


def setup_conf_menu():
    config = configparser.ConfigParser()
    config.read(CONF_FILE)
    if 'BASE_CONFIG' in config:
        return  # Already configured
    print('--- Setup ---')
    config['BASE_CONFIG'] = {}
    config['BATCH_CONFIG'] = {'last_generated': 0}
    base_config = config['BASE_CONFIG']
    print('Enter your manufacturer serial number prefix: ')
    base_config['manufacturer_prefix'] = raw_input()
    print('Enter the time divider setup for your devices (Default: 1): ')
    base_config['time_divider'] = raw_input()
    print('Are your devices using Restricted Digit set (Y/N)? (Default: N)')
    base_config['restricted_digit_set'] = str(1 if raw_input() == 'Y' else 0)
    print('Enter your device hardware model: ')
    base_config['hardware_model'] = raw_input()
    print('Enter your device firmware version (optional): ')
    base_config['firmware_version'] = raw_input()
    with open(CONF_FILE, 'w') as configfile:
        config.write(configfile)


def generate_csv_menu():
    config = configparser.ConfigParser()
    config.read(CONF_FILE)
    last_generated = config['BATCH_CONFIG']['last_generated']
    print('--- Batch Generation ---')
    print('Enter the last serial number that you generated without prefix (Last Generated: '+str(last_generated)+'): ')
    serial_start = int(raw_input())
    print('Enter the number of units you want to generate serial numbers for: ')
    number_of_devices = int(raw_input())
    print('Generating CSV...')
    generate_csv(serial_start, number_of_devices, config)
    config['BATCH_CONFIG']['last_generated'] = str(serial_start+number_of_devices)
    with open(CONF_FILE, 'w') as configfile:
        config.write(configfile)
    print('CSV generated! ')


if __name__ == '__main__':
    print('--- OpenPAYGO Token - CSV Generator ---')
    setup_conf_menu()
    generate_csv_menu()
