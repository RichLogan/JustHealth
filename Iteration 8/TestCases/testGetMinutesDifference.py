from peewee import *
from datetime import timedelta
import requests
import unittest
import imp
import datetime
import sys

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

#import the api so we are able to run locally
sys.path.insert(0, 'Website')
import justHealthServer
from justHealthServer import api

class testGetMinutesDifference(unittest.TestCase):
	"""Testing the getMinutesDifference API method"""

		def getMinutesDifference(self):
		"""Attempt to check that the correct number of minutes is returned"""
		timeOne = datetime.datetime.now().time()
		timeTwo = (datetime.datetime.now() + datetime.timedelta(minutes = 20)).time()

		response = api.getMinutesDifference(timeOne, timeTwo)
		self.assertEqual(response, 20)


if __name__ == '__main__':
    unittest.main()