#!/usr/bin/env python

try:

    # Imports the IotFetcher
    from iot_fetcher import IotFetcher

except ImportError:
    exit("This script requires to import the IoT shared functions\nThe file iot_fetcher.py was not found")

__author__ = 'https://github.com/fejao'


class Twitter(object):
	'''A'''

	def __init__(self, args, verbose=False):

		self.verbose = verbose

		self.consumer_key = args.get('consumer_key')
		self.consumer_secret = args.get('consumer_secret')
		self.access_token = args.get('access_token')
		self.access_token_secret = args.get('access_token_secret')

		if self.verbose:
			print("Importing the tweepy library...")

		try:
			self.tweepyModule = __import__('tweepy')

			if self.verbose:
				print("...tweepy library imported")

		except ImportError:
			exit("For using twitter is necessary to import it's bibliotec\n\
			Please install it with: sudo pip install tweepy")

		self.setsAPI()

	def setsAPI(self):
		'''A'''

		if self.verbose:
			print("Setting the Twitter API...")

		self.auth = self.tweepyModule.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_token, self.access_token_secret)

		self.api = self.tweepyModule.API(self.auth)

		if self.verbose:
			print("...Twitter API set")

	def getTweets(self, user, tweetsCount):
		'''A'''

		tweets = self.api.user_timeline(screen_name = str(user), count = int(tweetsCount), include_rts = True)

		tweetsList = []
		for tweet in tweets:
			tweetsList.append(tweet.text.encode('utf-8'))

		return tweetsList

class IotTwitter(Twitter):
	'''A'''

	def __init__(self, args):

		self.verbose = args.get('verbose')
		self.configFileAddress = args.get('configFileAddress')

		# Sets the fetcher
		fetcher = IotFetcher('Twitter',self.configFileAddress, self.verbose)

		# Load Twitter configuration from file
		self.configJson = fetcher.loadConfig()

		# Sets the values from parsed
		parsed = {
			'twitter_user': args.get('twitter_user'),
			'tweets_count': args.get('tweets_count'),
		}

		# Sets the parameters from parsed or fetched from file
		fetched = fetcher.setsFetcher(parsed, self.configJson.get('fetcher'))

		# Updates the Dictionary
		self.configJson['twitter_user'] = fetched.get('twitter_user')
		self.configJson['tweets_count'] = fetched.get('tweets_count')

		# Updates the functionsDict with the Twitter module
		dictValues = {
            'display_name': 'Twitter',
			'display_description': 'Uses the Twitter module',
			'function': 'twitter'
		}
		fetcher.updatesFunctionsDict(args.get('functionsDict'), dictValues)

        # Sets the variables
		self.twitter_user = fetched.get('twitter_user')
		self.tweets_count = fetched.get('tweets_count')

		# Sets super
		super(IotTwitter, self).__init__(self.configJson.get('config'), self.verbose)

	def getTweets(self):
		'''A'''
		if self.verbose:
			print("IotTwitter.getTweets")

		return super(IotTwitter, self).getTweets(self.twitter_user, self.tweets_count)
