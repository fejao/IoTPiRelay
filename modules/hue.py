#!/usr/bin/env python

try:

    # Imports the IotFetcher
    from iot_fetcher import IotFetcher

except ImportError:
    exit("This script requires to import the IoT shared functions\nThe file iot_fetcher.py was not found")

__author__ = 'https://github.com/fejao'

class PhilipsHue(object):
    """docstring for PhilipsHue"""

    def __init__(self, args, verbose=False):

        self.verbose = verbose

        self.bridgeIP = args.get('bridgeIP')
        self.username = args.get('username')

        try:
            from qhue import Bridge

        except ImportError:
            exit("For using PhilipsHue is necessary to import it's bibliotec\n\
            Please install it with: sudo pip install qhue")


        self.bridge = Bridge(self.bridgeIP, self.username)
        self.lights = self.bridge.lights

    def getNameLights(self):
        '''A'''

        # names = []
        # for key, values in self.bridge.lights().iteritems():
        #     names.append(values.get('name'))

        names = {}
        for key, values in self.bridge.lights().iteritems():
            names[key] = {
                'display_name': values.get('name'),
                'function': values.get('name')
            }
            # names.append(values.get('name'))

            # {
            #   "4": {
            #     "display_name": "Test",
            #     "display_description": "Testing function",
            #     "function": "test_function"
            #   }
            # }

        return names

    def toggle(self, lightNum):
        '''A'''

        if self.verbose:
            print("\nPhilipsHue.toggle(%s)" % lightNum)

        if str(lightNum) in self.lights():

            if self.verbose:
                print("PhilipsHue light %s found..." % lightNum)

            if self.lights[lightNum]().get('state').get('reachable'):
                if self.verbose:
                    print('light %s reachable...' % lightNum)

                if self.lights[lightNum]().get('state').get('on'):
                    print('light %s OFF' % lightNum)

                    self.lights[lightNum].state(on=False)

                else:
                    print('light %s ON' % lightNum)
                    self.lights[lightNum].state(on=True)

            else:
                if self.verbose:
                    print('light %s NOT reachable...' % lightNum)

                else:
                    if self.verbose:
                        print("ERROR: PhilipsHue with number %s dosen't exist..." % lightNum)

    def getLightFunctions(self, lightNum):
        '''A'''

        if self.verbose:
            print("PhilipsHue.getLightFunctions(%s)" % lightNum)


        light = self.lights().get(lightNum)
        light_functions = [
            'Toggle',
            'On',
            'Off'
        ]
        if light.get('type') == 'Dimmable light':
            light_functions.append('Dimm Down')
            light_functions.append('Dimm Up')

        # I don't have a RGB light, but it should be done here
        elif light.get('type') == 'Hue':
            import pdb; pdb.set_trace()
            light_functions.append('Hue Change')

        else:
            # TODO
            import pdb; pdb.set_trace()

        return light_functions


class IotPhilipsHue(PhilipsHue):
    '''A'''

    def __init__(self, args):

        self.verbose = args.get('verbose')
        self.configFileAddress = args.get('configFileAddress')

        # Sets the fetcher
        fetcher = IotFetcher('Philips-Hue', self.configFileAddress, self.verbose)

        # Load Philips-Hue configuration from file
        self.configJson = fetcher.loadConfig().get('philips_hue')

        # Sets the values from parsed
        parsed = {
            'bridgeIP': args.get('bridgeIP'),
            'username': args.get('username'),
        }

        # Sets the parameters from parsed or fetched from file
        fetched = fetcher.setsFetcher(parsed, self.configJson)

        # Updates the Dictionary
        self.configJson['bridgeIP'] = fetched.get('bridgeIP')
        self.configJson['username'] = fetched.get('username')

        # Updates the functionsDict with the Twitter module
        dictValues = {
        'display_name': 'Hue',
        'display_description': 'Uses the Philips-Hue',
        'function': 'hue'
        }

        fetcher.updatesFunctionsDict(args.get('functionsDict'), dictValues)

        # Sets super
        super(IotPhilipsHue, self).__init__(self.configJson, self.verbose)

    def getLightNumFromName(self, lightName):
        '''A'''

        if self.verbose:
            print("IotPhilipsHue.getLightNumFromName('%s')" % lightName)

        for key, values in self.lights().iteritems():
            if values.get('name') == lightName:
                return key

    def toggleName(self, lightName):
        '''A'''

        if self.verbose:
            print("IotPhilipsHue.toggle")

        lightNum = self.getLightNumFromName(lightName)

        return super(IotPhilipsHue, self).toggle(lightNum)

    # def runForNavigation(self, args):
    def runForFunction(self, lightNum, function):
        '''A'''

        if self.verbose:
            print("IotPhilipsHue.runForFunction(%s, %s)" %(lightNum, function))

        # Gets the light from it's number
        light = self.lights().get(lightNum)

        # Test if the light is reachable
        if not light.get('state').get('reachable'):
            # Returns string with description
            return "Light not reachable"

        # When the light is reachable
        else:
            if function == 'Toggle':
                self.toggle(lightNum)

            elif function == 'On':
                import pdb; pdb.set_trace()

            elif function == 'Off':
                import pdb; pdb.set_trace()

            elif function == 'Dimm Down':
                # Gets the brightness
                bri = light.get('state').get('bri')
                # Dimm down
                bri -= 32
                # Set's the max brightness
                if bri < 0:
                    bri = 0
                # Updates the light state
                self.lights[lightNum].state(bri=bri)

            elif function == 'Dimm Up':
                # Gets the brightness
                bri = light.get('state').get('bri')
                # Dimm up
                bri += 32
                # Set's the max brightness
                if bri > 254:
                    bri = 254
                # Updates the light state
                self.lights[lightNum].state(bri=bri)

            # Add here the Color functionality
            elif function == 'Hue Change':
                import pdb; pdb.set_trace()

            else:
                # TODO
                import pdb; pdb.set_trace()

            return None


    def toggle_OLD(self, lightNum):
        '''A'''

        if self.verbose:
            print("IotPhilipsHue.toggle")

        return super(IotPhilipsHue, self).toggle(lightNum)
