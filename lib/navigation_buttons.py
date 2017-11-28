#!/usr/bin/env python

__author__ = 'https://github.com/fejao'

DEFAUL_SELECTED_NAVIGATION = 1
DEFAUL_SELECTED_HUE = 0
DEFAUL_SELECTED_HUE_FUNCTION = 0

class IotNavigationButtons(object):
    '''A'''

    # def __init__(self, functionsDict, verbose=False):
    def __init__(self, functionsDict, lightsDict, verbose=False):

        self.verbose = verbose
        # Functions
        self.functionsDict = functionsDict
        self.selectedNavigation = DEFAUL_SELECTED_NAVIGATION
        # Hue Lights
        self.lightsDict = lightsDict
        self.selectedHue = DEFAUL_SELECTED_HUE
        # Hue Functions
        self.selectedHueFunction = DEFAUL_SELECTED_HUE_FUNCTION

    def runForFunction(self, buttonName):
        '''A'''

        if self.verbose:
            print("IotNavigationButtons.runForFunction(%s)" % buttonName)

        toRun = False
        if buttonName == 'up':
            # Updates the selectedNavigation
            self.selectedNavigation -= 1
            if self.selectedNavigation == 0:
                self.selectedNavigation = len(self.functionsDict)

        elif buttonName == 'down':
            # Updates the selectedNavigation
            self.selectedNavigation += 1
            if self.selectedNavigation > len(self.functionsDict):
                self.selectedNavigation = DEFAUL_SELECTED_NAVIGATION

        elif buttonName == 'select':
            toRun = True

        elif buttonName == 'reset':
            self.selectedNavigation = DEFAUL_SELECTED_NAVIGATION

        else:
            exit("Error !!!\nUsing the navigation buttons, the one selected is unknown: %s" % buttonName)

        # Get selected function
        function_from_menu = self.functionsDict[self.selectedNavigation]
        function = function_from_menu.get('function')

        if toRun:
            toRun = function

        return buttonName, function, toRun

    def runForHueLights(self, buttonName):
        '''A'''

        if self.verbose:
            print("IotNavigationButtons.runForHueLights(%s)" % buttonName)

        to_run = None

        # elif buttonName == 'up':
        if buttonName == 'up':
            self.selectedHue -= 1
            if self.selectedHue < 0:
                self.selectedHue = len(self.lightsDict.keys()) - 1

        elif buttonName == 'down':
            self.selectedHue += 1
            if self.selectedHue > len(self.lightsDict.keys()) - 1:
                self.selectedHue = DEFAUL_SELECTED_HUE

        elif buttonName == 'select':
            # If the select button was pressed
            to_run = True

        elif buttonName == 'reset':
            # For reseting the menu
            to_run = buttonName

        else:
            # If none button is pressed before setting the menu
            None

        # Get seleted light number
        light_num = self.lightsDict.keys()[self.selectedHue]

        return light_num, to_run

    def runForHueFunctions(self, buttonName, functionsList):
        '''A'''

        if self.verbose:
            print("IotNavigationButtons.runForHueFunctions(%s)" % buttonName)

        # Fetches the selected light number
        light_num = self.lightsDict.keys()[self.selectedHue]

        to_run = None

        if buttonName == 'up':
            # Updates the selectedHueFunction
            self.selectedHueFunction -= 1
            if self.selectedHueFunction < 0:
                self.selectedHueFunction = len(functionsList) - 1

        elif buttonName == 'down':
            # Updates the selectedHueFunction
            self.selectedHueFunction += 1
            if self.selectedHueFunction > len(functionsList) - 1:
                self.selectedHueFunction = DEFAUL_SELECTED_HUE_FUNCTION

        elif buttonName == 'select':
            # If the select button was pressed
            to_run = True

        elif buttonName == 'reset':
            # For reseting the menu
            to_run = buttonName

        else:
            # If none button is pressed before setting the menu
            None

        if to_run:
            to_run = functionsList[self.selectedHueFunction]

        return light_num, self.selectedHueFunction, to_run
