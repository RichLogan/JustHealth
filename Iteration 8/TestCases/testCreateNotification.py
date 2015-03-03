from peewee import *
import requests
import unittest
import imp

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testCreateNotificationRecord(unittest.TestCase):
	"""Testing the CreateNotificationRecord API"""

	def setUp(self):
		"""Create all the tables that are needed"""
		testDatabase.createAll()

		#create a test user
		patientClient = testDatabase.Client.insert(
            username = "patient",
            email = "justhealth123@richlogan.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        patientClient.execute()

        testPatient = testDatabase.Patient.insert(
            username = "patient",
            firstname = "patient",
            surname = "patient",
            ismale = True)
        testPatient.execute()

        patientPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "patient")
        patientPassword.execute()

        #create notification type
        connectionRequestNotification = testDatabase.Notificationtype.insert(
        	typename = "Connection Request",
        	typeclass = "info"
        	)
       	connectionRequestNotification.execute()

	def testLegitimate(self):
		"""Attempt to create a legitimate notification || check that API returns expected response and DB is correct too"""

		payload = {
			"user" : "patient",
			"notificationType" : "Connection Request",
			"relatedObject" : "1"
		}

		#Method is not externally addressable how does this work? 
		createNotification = requests.post("http://127.0.0.1:9999/api/createNotificationRecord", data=payload)
		self.assertEqual(createNotification.text, "True")
		self.assertEqual(testDatabase.Notifications.select().where(testDatabase.Notifications.usename == "testUsername".count(), 1)

	def testInvalidType(self):
		"""Attempt to create a notification with a non Foreign Key type || check that API returns expected response and DB contains no notifications"""
		
		payload = {
			"user" : "patient"
			"notificationType" : "Incorrect Notification Type"
		}

		#Method is not externally addressable, how do we send? 
		self.assertEqual(createNotification.text, "Invalid Notification Type")


	def testInvalidUser(self):
		"""Attempt to create a notification for a user that doesn't exist || check that API returns expected response and DB contains no notifications"""
		return False

	def testDismissedDefault
		"""Create a legitimate notification and test that dismissed is set to false || check that API returns expected response and DB is correct too"""
