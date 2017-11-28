#!/usr/bin/env python

import argparse

try:

    # Imports the IotFetcher
    from iot_fetcher import IotFetcher

except ImportError:
    exit("This script requires to import the IoT shared functions\nThe file iot_fetcher.py was not found")


__author__ = 'https://github.com/fejao'


def getFilesAdresses(default_folder_config):
    '''A'''

    filesAddresses = default_folder_config + 'config_file_names.json'
    fetcher = IotFetcher('Files Addresses', filesAddresses, False)
    return fetcher.loadConfig()

def getModulesEnable(default_folder_config):
    '''A'''

    filesAddresses = default_folder_config + 'config_modules_enable.json'
    fetcher = IotFetcher('Modules Enable', filesAddresses, False)
    return fetcher.loadConfig()

def setParser(args):
    '''Sets all the paramaters for the argparser'''

    default_button_refresh = args.get('default_button_refresh')
    default_folder_config = args.get('default_folder_config')

    files_addresses = getFilesAdresses(default_folder_config)
    default_enable = getModulesEnable(default_folder_config)

    #
    # Sets parser
    #
    parser = argparse.ArgumentParser(description='Script for using with your Raspberry Pi as an IoT with many functionalities.')

    # Verbose
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")

    # Refresh rate
    parser.add_argument('-br','--button-refresh',
        help="Button refresh rate, default: %s" % default_button_refresh,
        default=default_button_refresh,
        type=float)

    # OLED DISPLAY
    parser.add_argument('-o','--oled-display',
        help="Add the OLED Display functionality, default: %s" % default_enable.get('oled') == 'True',
        default=(default_enable.get('oled') == 'True'),
        type=bool)
    parser.add_argument('-op','--oled-pin',
        help="Sets the OLED Display GPIO pin, default: from the configuration file '%s'" % files_addresses['oled_display'],
        type=int)
    parser.add_argument('-os','--oled-size',
        help="Sets the OLED Display size, default: from the configuration file '%s'" % files_addresses['oled_display'],
        type=str)

    # TEMPERATURE SENSOR
    parser.add_argument('-t','--temperature',
        help="Add the functionality of the temperature sensor, default: %s" % default_enable.get('temperature') == 'True',
        default=(default_enable.get('temperature') == 'True'),
        type=bool)
    parser.add_argument('-tsm','--temperature-sensure-model',
        help="Sets the Temperature Sensor Model, default: from the configuration file '%s'" % files_addresses['temperature_sensor'],
        type=str)
    parser.add_argument('-tsp','--temperature-sensure-pin',
        help="Sets the Temperature Sensor GPIO pin, default: from the configuration file '%s'" % files_addresses['temperature_sensor'],
        type=str)

    # HUE
    parser.add_argument('-ph','--philips-hue',
        help="Add the Philips-Hue functionality, default: %s" % default_enable.get('hue') == 'True',
        default=(default_enable.get('hue') == 'True'),
        type=bool)
    parser.add_argument('-phu','--philips-hue-user',
        help="Sets the Philips-Hue user, default: from the configuration file '%s'" % files_addresses['hue'],
        type=str)
    parser.add_argument('-phi','--philips-hue-ip',
        help="Sets the Philips-Hue Bridge IP address, default: from the configuration file '%s'" % files_addresses['hue'],
        type=str)

    # TWITTER
    parser.add_argument('-tw','--twitter',
        help="Add the twitter functionality, default: %s" % default_enable.get('twitter') == 'True',
        default=(default_enable.get('twitter') == 'True'),
        type=bool)
    parser.add_argument('-tu','--twitter-user',
        help="Sets the default twitter user, default: from the configuration file '%s'" % files_addresses['twitter'],
        type=str)
    parser.add_argument('-tc','--tweets-count',
        help="Sets the default tweets to be displayed, default: from the configuration file '%s'" % files_addresses['twitter'],
        type=int)

    # NETWORK_SCAN
    parser.add_argument('-ns','--network-scan',
        help="Add the Network Scanner functionality, default: %s" % default_enable.get('net_scan') == 'True', default=(default_enable.get('net_scan') == 'True'),
        type=bool)

    # INFRA-RED
    parser.add_argument('-ir','--infra-red',
        help="Add the Infra-Red functionality, default: %s" % default_enable.get('infra_red') == 'True', default=(default_enable.get('infra_red') == 'True'),
        type=bool)

    # RELAY
    parser.add_argument('-r','--relay',
        help="Add the functionality of a relay, default: %s" % default_enable.get('relay') == 'True', default=(default_enable.get('relay') == 'True'),
        type=bool)

    # BUTTONS
    parser.add_argument('-b','--buttons',
        help="Add the functionality for buttons, default: %s" % default_enable.get('buttons') == 'True',
        default=(default_enable.get('buttons') == 'True'),
        type=bool)

    return parser.parse_args()
