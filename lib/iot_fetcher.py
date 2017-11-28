#!/usr/bin/env python

import json

__author__ = 'https://github.com/fejao'

class IotFetcher(object):
	'''A'''

	def __init__(self, name, configFileAddress, verbose):

		self.name = name
		self.configFileAddress = configFileAddress
		self.verbose = verbose

	def loadConfig(self):
		'''A'''

		try:
			if self.verbose:
				print('Importing the %s configuration file: %s' % (self.name, self.configFileAddress))

			# Gets the configurations from the json configuration file
			with open(self.configFileAddress) as data_file:
				return json.load(data_file)

		except Exception as err:
			exit("\nImport Error!!!\nThis script requires to import the %s configuration file\nThe configuration file '%s' not found" % (self.name, self.configFileAddress))

		finally:
			data_file.close()

	def setsFetcher(self, parsed, configJson):
		'''A'''

		fetched = {}
		for key, values in parsed.iteritems():
			if values:
				fetched[key] = values
			else:
				fetched[key] = configJson[key]

		return fetched

	def updatesFunctionsDict(self, functionsDict, values):
		'''A'''

		functionsDict[len(functionsDict) + 1] = values
