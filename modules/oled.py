#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
import math
import time

try:
	import Adafruit_GPIO.SPI as SPI

except ImportError:
	exit("This script requires the Adafruit_GPIO module\nInstall with: sudo pip install Adafruit_GPIO")

try:
	import Adafruit_SSD1306

except ImportError:
	exit("This script requires the Adafruit_SSD1306 module\nInstall with: sudo pip install Adafruit_SSD1306")


# Raspberry Pi pin
RST = 7
# RST = 19

PICTURES_FOLDER = './pics/'
# FONTS_FOLDER = './fonts/'
FONTS_FOLDER = '/usr/share/fonts/truetype/freefont/'

class OledDisplay(object):
	"""A"""

	def __init__(self, args, verbose=False):

		self.verbose = verbose

		self.rst_pin = args.get('rst_pin')
		self.size = args.get('size')

		# The display from it's size
		if self.size == '128x32':
			self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=self.rst_pin)

		elif self.size == '128x64':
			self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=self.rst_pin)

		else:
			exit("OLED Display size unknown: %s\nPlese set is as 128x32 or 128x64" % self.size)

		# Sets display
		self.disp.begin()
		self.width = self.disp.width
		self.height = self.disp.height

	def clear(self):
		'''A'''

		if self.verbose:
				print("OledDisplay.clear()")

		self.disp.clear()
		self.disp.display()

	def show(self, image):
		'''A'''

		if self.verbose:
			print("OledDisplay.show(image)")

		self.disp.image(image)
		self.disp.display()

	def showImage(self, imageName):
		'''A'''

		if self.verbose:
				print("OledDisplay.showImage('%s')" % imageName)

		image = Image.open(PICTURES_FOLDER + imageName).convert('1')

		self.show(image)

	def showText(self, text, size):
		'''A'''

		if self.verbose:
			print("OledDisplay.showText('%s', %s)" % (text, size))

		padding = 2
		shapeWidht = 20
		top = padding
		bottom = self.height - padding

		textFill = 255
		backgroundFill = 127


		# font = ImageFont.load_default()

		font = ImageFont.truetype(FONTS_FOLDER + "FreeMono.ttf", size, encoding="unic")


		img = Image.new('1', (self.width, self.height))
		imgd = ImageDraw.Draw(img)

		imgd.text((padding, top), text, font=font, fill=backgroundFill)
		imgd.text((padding, top), text, font=font, fill=textFill)

		self.show(img)

	def showText_WTF(self, text, size):
		'''A'''

		if self.verbose:
			print("OledDisplay.showText('%s', %s)" % (text, size))

		padding = 2
		shapeWidht = 20
		top = padding
		bottom = self.height - padding

		textFill = 255
		backgroundFill = 127


		# font = ImageFont.load_default()

		font = ImageFont.truetype(FONTS_FOLDER + "FreeMono.ttf", size, encoding="unic")


		img = Image.new('1', (self.width, self.height))
		imgd = ImageDraw.Draw(img)

		imgd.text((padding, top), text, font=font, fill=backgroundFill)
		imgd.text((padding, top), text, font=font, fill=textFill)

		return img

		# self.show(img)

	def drawLine(self, imgd, starPixel, width=None):
		'''A'''

		if width:
			imgd.line(((0, starPixel), (self.width, starPixel)), fill=255, width=width)
		else:
			imgd.line(((0, starPixel), (self.width, starPixel)), fill=255, width=2)

		# return imgd


class IotOledDisplay(OledDisplay):
	'''A'''

	def __init__(self, args):

		try:

		    # Imports the IotFetcher
		    from iot_fetcher import IotFetcher

		except ImportError:
		    exit("This script requires to import the IoT shared functions\nThe file iot_fetcher.py was not found")

		self.verbose = args.get('verbose')
		self.configFileAddress = args.get('configFileAddress')

		# Sets the fetcher
		fetcher = IotFetcher('OLED Display',self.configFileAddress, self.verbose)

		# Load OLED Display configuration from file
		self.configJson = fetcher.loadConfig().get('oled_display')

		# Sets the values from parsed
		parsed = {
			'rst_pin': args.get('rst_pin'),
			'size': args.get('size'),
		}

		# Sets the parameters from parsed or fetched from file
		fetched = fetcher.setsFetcher(parsed, self.configJson)

		# Updates the Dictionary
		self.configJson['rst_pin'] = fetched.get('rst_pin')
		self.configJson['size'] = fetched.get('size')

		# Updates the functionsDict with the Twitter module
		dictValues = {
            'display_name': 'OLED Display',
			'display_description': 'Uses the OLED Display module',
			'function': 'oled'
		}
		fetcher.updatesFunctionsDict(args.get('functionsDict'), dictValues)

		# Sets super
		super(IotOledDisplay, self).__init__(self.configJson, self.verbose)

	def displayStats(self):
		'''A'''

		# image = Image.new('1', (width, height))
		image = Image.new('1', (self.width, self.height))

		# Get drawing object to draw on image.
		draw = ImageDraw.Draw(image)

		# Draw a black filled box to clear the image.
		draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)

		# Draw some shapes.
		# First define some constants to allow easy resizing of shapes.
		padding = -2
		top = padding
		bottom = self.height-padding

		# Load default font.
		font = ImageFont.load_default()
		# font = ImageFont.truetype(FONTS_FOLDER + "FreeMono.ttf", 12, encoding="unic")

	    # Draw a black filled box to clear the image.
		draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)

		# Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
		cmd = "hostname -I | cut -d\' \' -f1"
		IP = subprocess.check_output(cmd, shell = True )
		cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
		CPU = subprocess.check_output(cmd, shell = True )
		# cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB %.2f%%\", $3,$2,$3*100/$2 }'"
		cmd = "free -m | awk 'NR==2{printf \"%s/%s MB %.2f%%\", $3,$2,$3*100/$2 }'"
		MemUsage = subprocess.check_output(cmd, shell = True )
		cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%dGB %s\", $3,$2,$5}'"
		Disk = subprocess.check_output(cmd, shell = True )

		# Write two lines of text.
		draw.text((0, top), "IP:     " + str(IP),  font=font, fill=255)
		top += 12
		draw.text((0, top), "CPU Load: " + str(CPU), font=font, fill=255)
		top += 12
		draw.text((0, top), "Memory: \n  " + str(MemUsage),  font=font, fill=255)
		top += 25
		draw.text((0, top), "Disk:     " + str(Disk),  font=font, fill=255)

		# Display image.
		self.disp.image(image)
		self.disp.display()

	def scrollText(self, text):
		'''A'''

		# Create image buffer.
		# Make sure to create image with mode '1' for 1-bit color.
		image = Image.new('1', (self.width, self.height))

		# Load default font.
		font_size = 13
		font = ImageFont.truetype(FONTS_FOLDER + "FreeMono.ttf", font_size, encoding="unic")

		# Create drawing object.
		draw = ImageDraw.Draw(image)

		# Define text and get total width.
		# text = 'SSD1306 ORGANIC LED DISPLAY. THIS IS AN OLD SCHOOL DEMO SCROLLER!! GREETZ TO: LADYADA & THE ADAFRUIT CREW, TRIXTER, FUTURE CREW, AND FARBRAUSCH'
		maxwidth, unused = draw.textsize(text, font=font)

		# Set animation and sine wave parameters.
		amplitude = self.height/4
		offset = self.height/2 - 4
		velocity = -2
		startpos = self.width

		# Animate text moving in sine wave.
		pos = startpos

		# while True:
		done = True
		while done:
		    # Clear image buffer by drawing a black filled box.
		    draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
		    # Enumerate characters and draw them offset vertically based on a sine wave.
		    x = pos
		    for i, char in enumerate(text):
		        # Stop drawing if off the right side of screen.
		        if x > self.width:
		            break
		        # Calculate width but skip drawing if off the left side of screen.
		        if x < -10:
		            char_width, char_height = draw.textsize(char, font=font)
		            x += char_width
		            continue
		        # Calculate offset from sine wave.
		        y = offset + math.floor(amplitude * math.sin(x/float(self.width)*2.0*math.pi))
		        # Draw text.
		        draw.text((x, y), char, font=font, fill=255)
		        # Increment x position based on chacacter width.
		        char_width, char_height = draw.textsize(char, font=font)
		        x += char_width
		    # Draw the image buffer.
		    self.disp.image(image)
		    self.disp.display()
		    # Move position for next frame.
		    pos += velocity

		    # Start over if text has scrolled completely off left side of screen.
		    if pos < -maxwidth:
				done = False
		        # pos = startpos

		    # Pause briefly before drawing next frame.
		    # time.sleep(0.1)
		    time.sleep(0.05)

	def drawTitle(self, imgd, title):
		'''
		Draws the title for menus

		Attributes:
		-----------
		imgd (ImageDraw.Draw):
			The ImageDraw object to be updated with the added lines
		title (string):
			The title name to be added

		Returns:
		---------
		imgd (ImageDraw.Draw):
			The updated ImageDraw object with the added title
		int:
			with the number of the added pixels
		'''

		top = 0
		padding = 0
		textFill = 255
		size = 15
		font = ImageFont.truetype(FONTS_FOLDER + "FreeMono.ttf", size, encoding="unic")
		# Draw the Title
		imgd.text((padding, top), title, font=font, fill=textFill)
		# Draw a line under the title
		self.drawLine(imgd, size + 2)

		# Returns the updated ImageDraw object
		return imgd, size + 3

	def addOptions(self, imgd, top, entries):
		'''A'''

		# Sets font
		font_size = 13
		font = ImageFont.truetype(FONTS_FOLDER + "FreeMono.ttf", font_size, encoding="unic")
		textFill = 255
		for entry in entries:
			imgd.text((0, top), entry, font=font, fill=textFill)
			top += 15

		return imgd

	def displayFunctions(self, functionsDict, selected):
		'''
		Displays the functions over the OLED display

		Attributes:
		-----------
		title (string):
			The title name of the function to be displayed
		functionsDict (dict):
			Dictionary with all the possible choices
			usually the self.functionsDict
		selected (int)
			Number of the selected function

		Returns:
		---------
			It dosen't returns nothing, only display the selected over the display
		'''
		self.clear()

		# Creates the object to be handeled to draw over the display
		img = Image.new('1', (self.width, self.height))
		imgd = ImageDraw.Draw(img)

		# Adds the Menu Title
		imgd, added_pixels = self.drawTitle(imgd, 'Functions')
		top = added_pixels

		menuEntries = []
		found = False
		for key, values in functionsDict.iteritems():

			# Displays only 3 entries at time
			# For at least 9 function entries
			if key == 4 or key == 7:

				# If founded, stops
				if found:
					break
				else:
					# Fill again the list
					menuEntries = []

			if values.get('function') == selected:
				text = '> ' + values.get('display_name')
				found = True

			else:
				text = '  ' + values.get('display_name')

			menuEntries.append(text)

		# Adds the founded options to be displayed
		imdg = self.addOptions(imgd, top, menuEntries)

		self.disp.image(img)
		self.disp.display()

	def displayHueLights(self, lightsDict, selected):
		'''
		A
		'''

		# Creates the object to be handeled to draw over the display
		img = Image.new('1', (self.width, self.height))
		imgd = ImageDraw.Draw(img)

		# Adds the Menu Title
		imgd, added_pixels = self.drawTitle(imgd, 'Hue Lights')
		top = added_pixels

		menuEntries = []
		found = False
		keyList=sorted(lightsDict.keys())
		for i,v in enumerate(keyList):
			light_name = lightsDict.get(v).get('name')

			if i == 4 or i == 7:

				# If founded, stops
				if found:
					break
				else:
					# Fill again the list
					menuEntries = []

			if v == selected:
				text = '> ' + light_name
				found = True

			else:
				text = '  ' + light_name

			menuEntries.append(text)

		# Adds the founded options to be displayed
		imdg = self.addOptions(imgd, top, menuEntries)

		self.disp.image(img)
		self.disp.display()

	def displayHueFunctions(self, lightName, functionsList, selected):
		'''
		A
		'''

		# padding = 2
		padding = 0
		shapeWidht = 20
		top = padding
		bottom = self.height - padding

		textFill = 255
		# backgroundFill = 127

		img = Image.new('1', (self.width, self.height))
		imgd = ImageDraw.Draw(img)

		# Adds the Menu Title
		imgd, added_pixels = self.drawTitle(imgd, lightName)
		top += added_pixels



		menuEntries = []
		found = False
		# keyList=sorted(lightsDict.keys())
		for i, function_name in enumerate(functionsList):
			# Displays in max 3 options
			if i == 3 or i == 6:

				# If founded, stops
				if found:
					break
				else:
					# Fill again the list
					menuEntries = []

			if i == selected:
				text = '> ' + function_name
				found = True

			else:
				text = '  ' + function_name

			menuEntries.append(text)

		# # Sets font
		# font_size = 13
		# font = ImageFont.truetype(FONTS_FOLDER + "FreeMono.ttf", font_size, encoding="unic")
        #
		# for entry in menuEntries:
		# 	imgd.text((padding, top), entry, font=font, fill=textFill)
		# 	top += 15

		# Adds the founded options to be displayed
		imdg = self.addOptions(imgd, top, menuEntries)

		self.disp.image(img)
		self.disp.display()
