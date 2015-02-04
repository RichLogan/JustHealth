import unittest

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testDismissNotification(unittest.TestCase):
	def testDismissLegitimate(self):
		"""Attempt to dismiss a notification || check that API returns expected response and DB field is set correctly"""
		return False


	def testDismissInvalidId(self):
		"""Attempt to dismiss a notification with an invalid notification ID || check that API returns expected response and DB not updated"""
		return False

