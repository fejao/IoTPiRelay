#!/usr/bin/env python

try:

    # Imports the IotFetcher
    from iot_fetcher import IotFetcher

except ImportError:
    exit("This script requires to import the IoT shared functions\nThe file iot_fetcher.py was not found")

try:

    # Imports the PiGPIO
    from pi_gpio import PiGPIO

except ImportError:
    exit("This script requires to import the PiGPIO functions\nThe file pi_gpio.py was not found")


__author__ = 'https://github.com/fejao'


class IotRelays(PiGPIO):
    '''A'''

    def __init__(self, args):

        self.verbose = args.get('verbose')
        self.configFileAddress = args.get('configFileAddress')

        # Sets the fetcher
        fetcher = IotFetcher('Relays',self.configFileAddress, self.verbose)

        # Load Philips-Hue configuration from file
        self.configJson = fetcher.loadConfig()

        # Sets super
        super(IotRelays, self).__init__(self.verbose)

    def getPinFromName(self, relayName):
        '''A'''

        if self.verbose:
            print("IotRelays.getPinFromName('%s')" % relayName)

        relay = self.configJson.get(relayName)

        if relay:
            return relay.get('pin')

        else:
            exit("\nError at IotRelays.getPinFromName!!!\nThe relay name '%s' don't exists in it's configuration" % relayName)

    def toggleName(self, relayName):
        '''A'''

        if self.verbose:
            print("IotRelays.toggle('%s')" % relayName)

        pin = self.getPinFromName(relayName)
        self.toggle(pin)

    def runForFunction(self, relayName):
        '''A'''

        # Toggle
        self.toggleName(relayName)

        # Return message
        return "Relay toggle:\n%s" % self.configJson.get(relayName).get('name')
