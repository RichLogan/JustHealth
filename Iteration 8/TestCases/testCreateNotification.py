import unittest

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testCreateNotification(unittest.TestCase):
	def testLegitimate(self):
		"""Attempt to create a legitimate notification || check that API returns expected response and DB is correct too"""
		return False

	
	def testInvalidType(self):
		"""Attempt to create a notification with a non Foreign Key type || check that API returns expected response and DB contains no notifications"""
		return False


	def testInvalidUser(self):
		"""Attempt to create a notification for a user that doesn't exist || check that API returns expected response and DB contains no notifications"""
		return False

	def testDismissedDefault
		"""Create a legitimate notification and test that dismissed is set to false || check that API returns expected response and DB is correct too"""
