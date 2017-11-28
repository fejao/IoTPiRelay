#!/usr/bin/env python

try:

    from iot_fetcher import IotFetcher

except ImportError:
    exit("This script requires to import the IoT shared functions\nThe file iot_fetcher.py was not found")

__author__ = 'https://github.com/fejao'

class TemperatureSensor(object):
    '''A'''

    def __init__(self, verbose=False):
        '''A'''

        self.verbose = verbose

        if self.verbose:
            print("Importing the Adafruit_DHT library...")

        try:
            self.dhtModule = __import__('Adafruit_DHT')

            if self.verbose:
                print("...Adafruit_DHT library imported")

        except ImportError:
            exit("For reading tempetatures you need to install the libraries first\n\
            Please visit the webpage for installing it: \
            \nhttps://github.com/adafruit/Adafruit_Python_DHT")

    def getReading(self, model, gpio_pin):
        '''A'''

        if self.verbose:
            print("Running TemperatureSensor.getReading...")

        humidity, temperature = self.dhtModule.read_retry(model, gpio_pin)

        if humidity is not None and temperature is not None:
            return {
                'result': True,
                'temperature': "{0:.2f}".format(temperature),
                'humidity': "{0:.2f}".format(humidity),
            }

        else:
            return {'result': False}

class IotTemperatureSensor(TemperatureSensor):
    '''A'''

    def __init__(self, args):

        self.verbose = args.get('verbose')
        self.configFileAddress = args.get('configFileAddress')

        # Sets the fetcher
        fetcher = IotFetcher('Temperature Sensor',self.configFileAddress, self.verbose)

        # Load Philips-Hue configuration from file
        self.configJson = fetcher.loadConfig().get('temperature_sensor')

        # Sets the values from parsed
        parsed = {
            'model': args.get('model'),
            'gpio_pin': args.get('gpio_pin'),
        }

        # Sets the parameters from parsed or fetched from file
        fetched = fetcher.setsFetcher(parsed, self.configJson)

        # Updates the Dictionary
        self.configJson['model'] = fetched.get('model')
        self.configJson['gpio_pin'] = fetched.get('gpio_pin')

        # Sets the variables
        self.model = fetched.get('model')
        self.gpio_pin = fetched.get('gpio_pin')

        # Updates the functionsDict with the Twitter module
        dictValues = {
            'display_name': 'Temperature Sensor',
            'display_description': 'Uses the Temperature Sensor',
            'function': 'temperature'
        }

        fetcher.updatesFunctionsDict(args.get('functionsDict'), dictValues)

        # Sets super
        super(IotTemperatureSensor, self).__init__(self.verbose)

    def getReading(self):
        '''A'''

        if self.verbose:
            print("IotTwitter.getReading")

        reading = super(IotTemperatureSensor, self).getReading(self.model, self.gpio_pin)
        return "Humidity:\n %s%%\nTemperature:\n %s C" % (reading.get('humidity'), reading.get('temperature'))
