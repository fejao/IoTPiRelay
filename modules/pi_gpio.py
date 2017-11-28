#!/usr/bin/env python

__author__ = 'https://github.com/fejao'

try:
    import RPi.GPIO as GPIO

except ImportError:
    exit("Error importing RPi.GPIO!\n \
        This might be because you need to run it as a superuser")

class PiGPIO(object):
    '''Class used to sends commands to the Raspberry-Pi GPIO'''

    def __init__(self, verbose=False):

        self.verbose = verbose

        # Int the Pi's GPIO'S
        GPIO.setmode(GPIO.BCM)
        # Disable Warnings from the Pi
        GPIO.setwarnings(False)

    def setPin(self, gpioNum):
        '''A'''

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(gpioNum,GPIO.OUT)

    def setHigh_NEW(self, gpioNum):
        '''Sets the Raspberry-Pi GPIO to High'''

        if self.verbose:
            print('PiGPIO.setHigh: %d' % gpioNum)

        self.setPin(gpioNum)

        # self.setPin(gpioNum)
        # GPIO.setup(gpioNum,GPIO.OUT)
        GPIO.output(gpioNum, GPIO.HIGH)

    def setLow_NEW(self, gpioNum):
        '''Sets the Raspberry-Pi GPIO to low'''

        if self.verbose:
            print('PiGPIO.setLow: %d' % gpioNum)

        self.setPin(gpioNum)

        # self.setPin(gpioNum)
        # GPIO.setup(gpioNum,GPIO.OUT)
        GPIO.output(gpioNum, GPIO.LOW)

    def setHigh(self, gpioNum):
        '''Sets the Raspberry-Pi GPIO to High'''

        if self.verbose:
            print('PiGPIO.setHigh: %d' % gpioNum)

        # self.setPin(gpioNum)
        GPIO.setup(gpioNum,GPIO.OUT)
        GPIO.output(gpioNum, GPIO.HIGH)

    def setLow(self, gpioNum):
        '''Sets the Raspberry-Pi GPIO to low'''

        if self.verbose:
            print('PiGPIO.setLow: %d' % gpioNum)

        # self.setPin(gpioNum)
        GPIO.setup(gpioNum,GPIO.OUT)
        GPIO.output(gpioNum, GPIO.LOW)

    def getState(self, gpioNum):
        '''Returns the Raspberry-Pi GPIO state'''

        if self.verbose:
            print('PiGPIO.getState: %d' % gpioNum)

        # self.setPin(gpioNum)
        GPIO.setup(gpioNum,GPIO.OUT)
        return GPIO.input(gpioNum)

    def toggle(self, gpioNum):
        '''A'''

        if self.verbose:
            print('PiGPIO.toggle: %d' % gpioNum)

        if self.getState(gpioNum) == False:
            self.setHigh(gpioNum)

        else:
            self.setLow(gpioNum)

# DEBUG: inits the class and test it here
# test = PiGPIO(True)
# import pdb; pdb.set_trace()
