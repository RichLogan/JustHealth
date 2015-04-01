from peewee import *
from datetime import timedelta
from passlib.hash import sha256_crypt
import unittest
import json
import imp
import datetime
import sys

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

#import the api so we are able to run locally
sys.path.insert(0, 'Website')
import justHealthServer
from justHealthServer import api

class testCreateReminder(unittest.TestCase):
    """Testing the deleteReminder API method"""

    def setUp(self):
        """Create all the tables that are needed"""
        testDatabase.createAll()

        #create test user 1
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

        reminderInsert = testDatabase.Reminder.insert(
            username = 'patient',
            content = 'test',
            reminderClass = 'info',
            relatedObject = 1,
            relatedObjectTable = 'Appointments',
            extraDate = datetime.datetime.now() - datetime.timedelta(minutes = 10))
        reminderInsert.execute()

        #create test user 2
        patientClient2 = testDatabase.Client.insert(
            username = "patient2",
            email = "justhealth123@richlogan.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        patientClient2.execute()

        testPatient2 = testDatabase.Patient.insert(
            username = "patient2",
            firstname = "patient",
            surname = "patient",
            ismale = True)
        testPatient2.execute()

        patientPassword2 = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "patient2")
        patientPassword2.execute()

    def testLegitimate(self):
        """Attempt to get a reminder"""
        expectedResult = {
            "username": "patient", 
            "content": "test", 
            "reminderClass": "info", 
            "relatedObject": 1,
            "relatedObjectTable": "Appointments"
        }
        
        response = api.getReminders('patient')
        jsonResponse = json.loads(response)

        self.assertEqual(jsonResponse[0]['username'], expectedResult['username'])
        self.assertEqual(jsonResponse[0]['content'], expectedResult['content'])
        self.assertEqual(jsonResponse[0]['reminderClass'], expectedResult['reminderClass'])
        self.assertEqual(jsonResponse[0]['relatedObject'], expectedResult['relatedObject'])
        self.assertEqual(jsonResponse[0]['relatedObjectTable'], expectedResult['relatedObjectTable'])

    def testNotDelete(self):
        """Attempt to get reminders that don't exist"""
        expectedResult = '[]'
        
        response = api.getReminders('patient2')

        self.assertEqual(response, expectedResult)

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()