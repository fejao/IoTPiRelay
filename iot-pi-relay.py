#!/usr/bin/env python

import argparse
import sys
import time
import subprocess

# DEBUG
import pdb
from pprint import pprint

__author__ = 'https://github.com/fejao'

# Sets the used subrirectories
DEFAULT_FOLDER_ADDRESS_CONFIG = './config/'
DEFAULT_FOLDER_ADDRESS_LIB = './lib/'
DEFAULT_FOLDER_ADDRESS_MODULES = './modules/'

# Adds the subdirectories to the known path
sys.path.append(DEFAULT_FOLDER_ADDRESS_CONFIG)
sys.path.append(DEFAULT_FOLDER_ADDRESS_LIB)
sys.path.append(DEFAULT_FOLDER_ADDRESS_MODULES)

# Imports necessary functions/classes from files
from iot_pi import IotPi
from script_parser import setParser
from navigation_buttons import IotNavigationButtons

# Pause used for waiting for the next button press
DEFAULT_BUTTON_REFRESH = 0.3

class IotPiFunctions(IotPi):
    '''A'''

    def __init__(self, args):

        # Parsing globals to init object
        values = {
            'defaultAddressConfig': DEFAULT_FOLDER_ADDRESS_CONFIG,
            'defaultAddressModules': DEFAULT_FOLDER_ADDRESS_MODULES
        }

        # Sets super
        super(IotPiFunctions, self).__init__(args, values)

        # Sets navigation
        self.navigation = IotNavigationButtons(self.functionsDict, self.hue.lights(), self.verbose)
        self.navigation_type = 'functions'

    def showOutput(self, msg, size):
        '''
		Displays the output from functions, if the OLED module is enable it will
        show over the display

		Attributes:
		-----------
		msg (string):
			The message to be displayed
		size (int):
			The text size to be displayed
        '''

        if self.verbose:
            print("IotPiFunctions.showOutput(%s, %s)" % (msg, size))

        if self.oled:
            if msg:
                self.oled.showText(msg, size)

        else:
            if msg:
                print(msg)

    def runForFunction(self, function):
        '''
		Will set for the function name to be runned

		Attributes:
		-----------
		function (string):
			The name of the function to be runned
        '''

        if self.verbose:
            print("\nIotPiFunctions.runForFunction(%s)" % function)

        if function == 'clear':
            if self.oled:
                # If the OLED module is enable, clear it
                self.oled.clear()
            else:
                # If the OLED module is not enable, clear the terminal
                subprocess.call(['clear'])

        elif function == 'clock':
                        # Gets the system time
            msg = time.strftime('%d %b, %Y \nWeek: %W\n\n%X:%m')
            size = 14
            # Displays the sytem time
            self.showOutput(msg, size)

        elif function == 'stats':
            # Displays the system status
            self.oled.displayStats()

        # TODO
        elif function == 'oled':
            msg = "Test-OLED"
            size = 15
            self.showOutput(msg, size)

        elif function =='hue':
            # Set's the navigation for hue
            self.navigation_type = 'hue_lights'

            # Show Menu
            self.runForNavigation('none')

        elif function =='hue_test':
            self.hue.toggle(4)
            msg = "Test-Hue"
            size = 15
            self.showOutput(msg, size)

        elif function == 'temperature':
            # Gets the sensor output
            msg = self.sensor.getReading()
            size = 13
            # Shows the sensor output
            self.showOutput(msg, size)

        elif function == 'twitter':
            # Get the tweets
            tweets = self.twitter.getTweets()
            # Display the tweets scrolling
            self.oled.scrollText(tweets[0])

        elif function == 'network_scanner':
            # Display warning long waiting scan
            msg = "Scanning Network..."
            size = 12
            self.showOutput(msg, size)

            # Get the Network-scann results
            scan_result = self.netScan.checkConnections()
            if scan_result:
                # Displays the detectededs new connections
                self.showOutput(scan_result, 11)
            else:
                # Displays tha t no unknown connection was detected
                self.showOutput("No Network errors\n\nNo unknown\ndetected...", 12)

        else:
            # For extras buttons, please add in here your own functions
            msg = "Extra %s toggle" % function
            size = 12
            self.showOutput(msg, size)

    def runForNavigation(self, function):
        '''
		Will set for the function name to be runned

		Attributes:
		-----------
		function (string):
			The name of the function to be runned
        '''

        if self.verbose:
            print("IotPiFunctions.runForNavigation(%s)" % function)

        if self.navigation_type == 'functions':
            # Gets the default functions with it's added modules
            buttonName, function, to_run = self.navigation.runForFunction(function)
            if to_run:
                # Runs the selected function
                self.runForFunction(to_run)

            else:
                # Display the functions options
                self.oled.displayFunctions(self.functionsDict, function)

        elif self.navigation_type == 'hue_lights':

            # Gets the Philips-Hue light
            light_num, to_run = self.navigation.runForHueLights(function)

            if to_run:
                if to_run == 'reset':
                    # Resets the navigation_type
                    self.navigation_type = 'functions'
                    # Clear the display
                    self.runForFunction('clear')
                else:
                    # Set's the navigation for hue ligth functions
                    self.navigation_type = 'hue_functions'

                    # Show the menu for Philips-Hue lights
                    self.runForNavigation('none')

            else:
                # Display the menu for Hue lights
                self.oled.displayHueLights(self.hue.lights(), light_num)

        elif self.navigation_type == 'hue_functions':

            # Get selected light from navigation
            selected_nacigation_num = self.navigation.selectedHue

            # Get Hue light number
            keyList=sorted(self.hue.lights().keys())
            light_num = keyList[selected_nacigation_num]

            # Get Hue light functions
            functions_list = self.hue.getLightFunctions(light_num)

            # Gets the Philips-Hue light functions
            light_num, selected_function, to_run = self.navigation.runForHueFunctions(function, functions_list)

            if to_run:
                if to_run == 'reset':
                    # Resets the navigation_type
                    self.navigation_type = 'functions'
                    # Clear the display
                    self.runForFunction('clear')

                else:
                    # Run the selected function at the selcted light
                    hue_output = self.hue.runForFunction(light_num, to_run)
                    if hue_output:
                        # Output message
                        self.showOutput(hue_output, 13)
                        # Reset to functions
                        self.navigation_type = 'functions'

            else:
                # Gets the selected light name
                light_name = self.hue.lights()[light_num].get('name')
                # Displays the selected light funtions
                self.oled.displayHueFunctions(light_name, functions_list, selected_function)

        else:
            # TODO
            import pdb; pdb.set_trace()

    def runForPressed(self, button):
        '''
		Gets the button pressed and runs the functions from it's type

		Attributes:
		-----------
		button (int):
			The button number that was pressed
        '''

        if self.verbose:
            print("\nIotPiFunctions.runForPressed(button) | button: %s" % button)

        button_type = self.buttons.functions.get(button).get('type')
        function = self.buttons.functions.get(button).get('function')

        if button_type == 'relay':
            msg = self.relays.runForFunction(function)
            size = 12
            self.showOutput(msg, size)

        elif button_type == 'navigation':
            self.runForNavigation(function)

        elif button_type == 'extras':
            self.runForFunction(function)

        else:
            exit("Error !!!\nButton type is unknown: %s" % button_type)

    def runForButtons(self):
        '''
		Function that detects if a button was pressed
        '''

        if self.verbose:
            print("\n-->PiOledRelay.runForButtons\n")

        if self.buttons:

            try:
                while True:
                    button = self.buttons.getPressed()
                    if button:

                        self.runForPressed(button)

                    time.sleep(self.button_refresh)

            except KeyboardInterrupt:
                if self.verbose:
                    print("\nCleaning Oled")

                # Clean the OLED Display before exiting
                if self.oled:
                    self.oled.clear()

                print("\nKEYBOARD INTERRUPT !!!\n")

        else:
            print("\nNot using buttons...")

# ####
# #### MAIN
# ####
def main():
    '''A'''

    print("Running Raspberry Pi as a IoT...\n")

    # Fetch parsed parameters from the terminal
    parserArgs = {
        'default_button_refresh': DEFAULT_BUTTON_REFRESH,
        'default_folder_config' : DEFAULT_FOLDER_ADDRESS_CONFIG
    }
    args = setParser(parserArgs)

    # Creates the object
    piot = IotPiFunctions(args)

    # Runs the script
    if piot.buttons:
        piot.runForButtons()
    else:
        # TODO
        exit("No buttons !!!")

    print("\n...Finished Raspberry Pi as a IoT")

if __name__ == '__main__':
    main()
