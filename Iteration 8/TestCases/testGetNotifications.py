import unittest

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testGetNotifications(unittest.TestCase):
	
	def testGetAll(self):
		"""Attempt to get all of the notifications for a user"""
		return False


	def testGetDismissed(self):
		"""Attempt to get all of the Dismissed notifications for a user || where dismissed==True"""
		return False


	def testGetNotDismissed(self):
		"""Attempt to get all of the undismissed notifications for a user || where dismissed==False"""
		return False


	def testGetAllInvalidUser(self): 
		"""Attempt to get notifications for an invalid user"""
		return False


	def testGetDismissedInvalidUser(self): 
		"""Attempt to get notifications for an invalid user where dismissed==True"""
		return False


	def testGetNotDismissedInvalidUser(self): 
		"""Attempt to get notifications for an invalid user where dismissed==False"""
		return False