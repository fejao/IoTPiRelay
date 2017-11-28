#!/usr/bin/env python

# import sys
# sys.path.append('./lib/')

__author__ = 'https://github.com/fejao'

class IotPi(object):
    '''A'''

    # def __init__(self, args):
    def __init__(self, args, values):

        # Varibles from parsed values
        self.args = args
        self.verbose = args.verbose
        self.button_refresh = args.button_refresh

        # Variables from initilized Globals
        self.defaultFileNames = values.get('defaultFileNames')
        self.defaultAddressConfig = values.get('defaultAddressConfig')
        self.defaultAddressModules = values.get('defaultAddressModules')

        # ADDS MODULES
        self.modulesAdd = self.addModuleInitHelper()
        self.functionsDict = self.modulesAdd.functionsDict

        self.relays = self.modulesAdd.relays()
        self.buttons = self.modulesAdd.buttons()

        self.oled = self.modulesAdd.oled()
        self.hue = self.modulesAdd.hue()
        self.sensor = self.modulesAdd.temperatureSensor()
        self.twitter = self.modulesAdd.twitter()
        self.netScan = self.modulesAdd.netScan()
        self.infraRed = self.modulesAdd.infraRed()

        # self.relays = self.modulesAdd.relays()
        # self.buttons = self.modulesAdd.buttons()

    def addModuleInitHelper(self):
        '''
        A
        '''

        try:
            if self.verbose:
                print("Importing the init_helper.py file...")

            from init_helper import IoTPiRelayInitHelper

            helperConfig = {
                'addressConfig': self.defaultAddressConfig,
                'addressModules': self.defaultAddressModules,
                'files_addresses': self.defaultFileNames
            }

            return IoTPiRelayInitHelper(helperConfig, self.args)

        except ImportError:
            exit("Import Error!!!\n \
                This script requires to import the initialization helper functions\n \
                The file init_helper.py was not found")
