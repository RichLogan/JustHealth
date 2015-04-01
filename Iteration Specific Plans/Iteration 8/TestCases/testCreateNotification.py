from peewee import *
from passlib.hash import sha256_crypt
import unittest
import imp
import sys

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

#import the api so we are able to run locally
sys.path.insert(0, 'Website')
import justHealthServer
from justHealthServer import api

class testCreateNotificationRecord(unittest.TestCase):
    """Testing the createReminder API"""

    def setUp(self):
        """Create all the tables that are needed"""
        testDatabase.createAll()
        
        #create a test user
        patientClientTable = testDatabase.Client.insert(
            username = "patient",
            email = "justhealth123@richlogan.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False).execute()

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
        user = "patient"
        notificationType = "Connection Request"
        relatedObject = int(1)

        #Method is not externally addressable how does this work? 
        createNotification = api.createNotificationRecord(user, notificationType, relatedObject)
        self.assertEqual(createNotification, "True")

    def testInvalidType(self):
        """Attempt to create a notification with a non Foreign Key type || check that API returns expected response and DB contains no notifications"""
        
        user = "patient"
        notificationType = "Connection Added"
        relatedObject = 1

        createNotification = api.createNotificationRecord(user, notificationType, relatedObject)
        self.assertEqual(createNotification, "Invalid Notification Type")
        self.assertEqual(testDatabase.Notification.select().where(testDatabase.Notification.username == "patient").count(), 0)

    def testInvalidNotificationType(self):
        """Attempt to create a notification with a Notification Type that does not exist || check that the API returns expected response and DB contains no notifications"""
        user = "patient"
        notificationType = "Does Not Exist"
        relatedObject = 1

        createNotification = api.createNotificationRecord(user, notificationType, relatedObject)
        self.assertEqual(createNotification, "Invalid Notification Type")
        self.assertEqual(testDatabase.Notification.select().where((testDatabase.Notification.username == "patient") & (testDatabase.Notification.notificationtype == "Does Not Exist")).count(), 0)

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()
 
if __name__ == '__main__':
    unittest.main()
