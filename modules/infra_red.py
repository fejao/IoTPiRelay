#!/usr/bin/env python

try:

    # Imports the IotFetcher
    from iot_fetcher import IotFetcher

except ImportError:
    exit("This script requires to import the IoT shared functions\nThe file iot_fetcher.py was not found")

__author__ = 'https://github.com/fejao'


class InfraRed(object):
    '''A'''

    def __init__(self, args, verbose=False):

        self.verbose = verbose

        # if self.verbose:
        #     print("InfraRed.__init__")

    def testFunction(self):
        '''A'''

        if self.verbose:
            print("InfraRed.testFunction")

class IotInfraRed(InfraRed):
    '''A'''

    def __init__(self, args):

        self.verbose = args.get('verbose')
        self.configFileAddress = args.get('configFileAddress')

        # Sets the fetcher
        fetcher = IotFetcher('Infra-Red',self.configFileAddress, self.verbose)

        # Load Philips-Hue configuration from file
        self.configJson = fetcher.loadConfig()

        # Sets super
        super(IotInfraRed, self).__init__(self.configJson, self.verbose)

    def wtf(self):
        '''A'''

        if self.verbose:
            print("IotInfraRed.wtf")

        return 'aaa'
