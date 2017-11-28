#!/usr/bin/env python

try:

    # Imports the IotFetcher
    from iot_fetcher import IotFetcher

except ImportError:
    exit("This script requires to import the IoT shared functions\nThe file iot_fetcher.py was not found")

try:

    # Imports the RPi.GPIO
    import RPi.GPIO as GPIO

except ImportError:
    exit("This script requires to import the RPi.GPIO functions\nYou should enable I2C at your Pi")



__author__ = 'https://github.com/fejao'

# Here I am using a 4x4 to have up to 16 inputs only using 4 GPIOs
# You can expand this, just don't forget to also update the file: config_buttons.json
MATRIX_KEYS = [
    ['11', '12', '13', '14'],
    ['21', '22', '23', '24'],
    ['31', '32', '33', '34'],
    ['41', '42', '43', '44']
]

class MatrixButtons(object):
    '''Class for using buttons at the IoTPiRelay'''

    def __init__(self, args, verbose=False):

        # Sets the GPIO mode
        GPIO.setmode(GPIO.BCM)

        self.verbose = verbose
        self.rows = args.get('rows')
        self.cols = args.get('cols')

        # Sets the matrix keys
        self.keys = MATRIX_KEYS

        # Sets
        self.setMatrixButtons()

    def setMatrixButtons(self):
        '''Sets the matrix Buttons'''

        for row_pin in self.rows:
            GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        for col_pin in self.cols:
            GPIO.setup(col_pin, GPIO.OUT)

    def getPressed(self):
        '''A'''

        key = 0
        for col_num, col_pin in enumerate(self.cols):
            GPIO.output(col_pin, 1)

            for row_num, row_pin in enumerate(self.rows):
                if GPIO.input(row_pin):
                    key = self.keys[row_num][col_num]

            GPIO.output(col_pin, 0)
        return key

class IotButtons(MatrixButtons):
    '''A'''

    def __init__(self, args):

        self.verbose = args.get('verbose')
        self.configFileAddress = args.get('configFileAddress')
        self.configFunctionsFileAddress = args.get('configFunctionsFileAddress')

        # Sets the fetcher
        fetcher = IotFetcher('Buttons',self.configFileAddress, self.verbose)

        # Load Buttons configuration from file
        self.configJson = fetcher.loadConfig()

        # Sets the buttons functions
        self.functions = self.getButtonsFunctions()

        # Sets super
        super(IotButtons, self).__init__(self.configJson, self.verbose)

    def getButtonsFunctions(self):
        '''A'''

        # Sets the fetcher
        functionsFetcher = IotFetcher('Buttons Functions',self.configFunctionsFileAddress, self.verbose)

        # Load Buttons Functions configuration from file
        return functionsFetcher.loadConfig()
