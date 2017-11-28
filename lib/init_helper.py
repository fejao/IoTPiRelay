#!/usr/bin/env python

try:

    # Imports the IotFetcher
    from iot_fetcher import IotFetcher

except ImportError:
    exit("This script requires to import the IoT shared functions\nThe file iot_fetcher.py was not found")

__author__ = 'https://github.com/fejao'

class IoTPiRelayInitHelper(object):
    '''Class used to '''

    def __init__(self, config, parsedArgs):

        self.args = parsedArgs
        self.verbose = self.args.verbose

        self.addressConfig = config.get('addressConfig')
        self.addressModules = config.get('addressModules')

        self.filesAddresses = self.getFilesAdresses()
        self.functionsDict = self.getFunctions()

    def getFunctions(self):
        '''A'''

        configFileAddress = self.addressConfig + self.filesAddresses['functions']
        fetcher = IotFetcher('Functions Dictionary', configFileAddress, self.verbose)
        # Parse the keys to int
        out = {int(key): value for key, value in fetcher.loadConfig().iteritems()}
        return out

    def getFilesAdresses(self):
        '''A'''

        filesAddresses = self.addressConfig + 'config_file_names.json'
        fetcher = IotFetcher('Files Addresses', filesAddresses, self.verbose)
        return fetcher.loadConfig()

    def oled(self):
        '''
        Initializes the hue and the hueNameLights objects with it's parsed values
        Updates the functionsDict with the Philips-Hue module

        Notes:
        --------
            If no parameters is parsed, it will use the ones defined at the configuration file
        '''

        if self.args.oled_display:

            if self.verbose:
                print("\nAdding the OLED Display Module...")

            # Imports the IotOledDisplay
            try:
                from oled import IotOledDisplay

            except ImportError:
                exit("This script requires to import the OLED Display functions\nThe file oled.py was not found")

            # Dictionary with parameters for object initialization
            configOled = {
                'verbose': self.verbose,
                'configFileAddress': self.addressConfig + self.filesAddresses['oled_display'],
                'functionsDict': self.functionsDict,
                'rst_pin': self.args.oled_pin,
                'size': self.args.oled_size,
            }

            # Return the Philips-Hue object initialized
            return IotOledDisplay(configOled)

        else:
            if self.verbose:
                print("\nOLED Display not selected, not adding module...")

            return None

    def hue(self):
        '''
        Initializes the hue and the hueNameLights objects with it's parsed values
        Updates the functionsDict with the Philips-Hue module

        Notes:
        --------
            If no parameters is parsed, it will use the ones defined at the configuration file
        '''

        if self.args.philips_hue:

            if self.verbose:
                print("\nAdding the Philips-Hue Module...")

            # Imports the IotPhilipsHue
            try:
                from hue import IotPhilipsHue

            except ImportError:
                exit("This script requires to import the Philips-Hue functions\nThe file hue.py was not found")

            # Dictionary with parameters for object initialization
            configHue = {
                'verbose': self.verbose,
                'configFileAddress': self.addressConfig + self.filesAddresses['hue'],
                'functionsDict': self.functionsDict,
                'bridgeIP': self.args.philips_hue_ip,
                'username': self.args.philips_hue_user
            }

            # Return the Philips-Hue object initialized
            return IotPhilipsHue(configHue)

        else:
            if self.verbose:
                print("\nPhilips-Hue not selected, not adding module...")

            return None

    def temperatureSensor(self):
        '''
        Initializes the sensor object with it's parsed values
        Updates the functionsDict with the Temperature Sensor module

        Notes:
        --------
            If no parameters is parsed, it will use the ones defined at the configuration file
        '''

        if self.args.temperature:
            if self.verbose:
                print("\nAdding the Temperature Sensor Module...")

            # Imports the IotTemperatureSensor
            try:
                from temperature_sensor import IotTemperatureSensor

            except ImportError:
                exit("This script requires to import the Temperature Sensor functions\nThe file temperature_sensor.py was not found")

            # Dictionary with parameters for object initialization
            configSensor = {
                'verbose': self.verbose,
                'configFileAddress': self.addressConfig + self.filesAddresses['temperature_sensor'],
                'functionsDict': self.functionsDict,
                "model": self.args.temperature_sensure_model,
                "gpio_pin": self.args.temperature_sensure_pin,
            }

            # Return the Temperature Sensor object initialized
            return IotTemperatureSensor(configSensor)

        else:
            if self.verbose:
                print("\nTemperature Sensor not selected, not adding module...")

            return None

    def twitter(self):
        '''
        Initializes the twitter object with it's parsed values
        Updates the functionsDict with the Temperature Sensor module

        Notes:
        --------
            If no parameters is parsed, it will use the ones defined at the configuration file
        '''

        if self.args.twitter:

            if self.verbose:
                print("\nAdding the Twitter Module...")

            # Imports the IotTwitter
            try:
                from twitter import IotTwitter

            except ImportError:
                exit("This script requires to import the Twitter functions\nThe file twitter.py was not found")

            configTwitter = {
                'verbose': self.verbose,
                'configFileAddress': self.addressConfig + self.filesAddresses['twitter'],
                'functionsDict': self.functionsDict,
                "twitter_user": self.args.twitter_user,
                "tweets_count": self.args.tweets_count,
            }

            # Return the Temperature Sensor object initialized
            return IotTwitter(configTwitter)

        else:
            if self.verbose:
                print("\nTwitter not selected, not adding module...")

            return None

    def netScan(self):
        '''
        Initializes the netScan object with it's parsed values
        Updates the functionsDict with the Temperature Sensor module

        Notes:
        --------
            If no parameters is parsed, it will use the ones defined at the configuration file
        '''

        if self.args.network_scan:

            if self.verbose:
                print("\nAdding the Network Scanner Module...")

            # Imports the IotInfraRed
            try:
                from network_scanner import IotNetworkScanner

            except ImportError:
                exit("This script requires to import the Network Scanner functions\nThe file network_scanner.py was not found")

            configNetScan = {
                'verbose': self.verbose,
                'configFileAddress': self.addressConfig + self.filesAddresses['network_scan'],
                'functionsDict': self.functionsDict,

                # "twitter_user": self.args.twitter_user,
                # "tweets_count": self.args.tweets_count,
            }

            # Return the Temperature Sensor object initialized
            return IotNetworkScanner(configNetScan)

        else:
            if self.verbose:
                print("\Infra-Red not selected, not adding module...")

            return None

    def infraRed(self):
        '''
        Initializes the infraRed object with it's parsed values
        Updates the functionsDict with the Temperature Sensor module

        Notes:
        --------
            If no parameters is parsed, it will use the ones defined at the configuration file
        '''

        if self.args.infra_red:

            if self.verbose:
                print("\nAdding the InfraRed Module...")

            # Imports the IotInfraRed
            try:
                from infra_red import IotInfraRed

            except ImportError:
                exit("This script requires to import the InfraRed functions\nThe file infra_red.py was not found")

            configInfraRed = {
                'verbose': self.verbose,
                'configFileAddress': self.addressConfig + self.filesAddresses['twitter'],
                'functionsDict': self.functionsDict,

                # "twitter_user": self.args.twitter_user,
                # "tweets_count": self.args.tweets_count,
            }

            # Return the Temperature Sensor object initialized
            return IotInfraRed(configInfraRed)

        else:
            if self.verbose:
                print("\Infra-Red not selected, not adding module...")

            return None

    def relays(self):
        '''AA'''

        if self.args.relay:

            if self.verbose:
                print("\nAdding the Relays Module...")

            # Imports the IotRelays
            try:
                from relays import IotRelays

            except ImportError:
                exit("This script requires to import the Relays functions\nThe file relays.py was not found")

            configRelays = {
                'verbose': self.verbose,
                'configFileAddress': self.addressConfig + self.filesAddresses['relays'],
                'functionsDict': self.functionsDict,
            }

            # Return the Relays object initialized
            return IotRelays(configRelays)

        else:
            if self.verbose:
                print("\nRelays not selected, not adding module...")

            return None

    def buttons(self):
        '''A'''

        if self.args.buttons:

            if self.verbose:
                print("\nAdding the Buttons Module...")

            try:
                from buttons import IotButtons

            except ImportError:
                exit("This script requires to import the Buttons functions\nThe file buttons.py was not found")

            configButtons = {
                'verbose': self.verbose,
                'configFileAddress': self.addressConfig + self.filesAddresses['buttons'],
                'configFunctionsFileAddress': self.addressConfig + self.filesAddresses['buttons_functions'],
            }

            # Return the Relays object initialized
            return IotButtons(configButtons)

        else:
            if self.verbose:
                print("\nButtons not selected, not adding module...")

            return None
