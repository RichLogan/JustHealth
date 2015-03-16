from peewee import *
from passlib.hash import sha256_crypt
import requests
import unittest
import imp
import json

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testAddMedication(unittest.TestCase):

    def setUp(self):
        testDatabase.createAll()
        #Create a Client entry, a Patient entry, a prescription  and a password.
        testClient = testDatabase.Client.insert(
            username = "test",
            email = "justhealth@richlogan.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        testClient.execute()

        testPatient = testDatabase.Patient.insert(
            username = "test",
            firstname = "test",
            surname = "test",
            ismale = True)
        testPatient.execute()

        testPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "test")
        testPassword.execute()

        securityClient = testDatabase.Client.insert(
            username = "Security",
            email = "Security@richlogan.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        securityClient.execute()

        testSecurity = testDatabase.Patient.insert(
            username = "Security",
            firstname = "Security",
            surname = "Security",
            ismale = True)
        testSecurity.execute()

        securityPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "Security")
        securityPassword.execute()

    def testLegitimate(self):
        payload = {
            "name" : "test"
        }

        medication = requests.post("http://127.0.0.1:9999/api/deleteMedication", data=payload, auth=('patient','73630002494546d52bdc16cf5874a41e720896b566cd8cb72afcf4f866d70570aa078832f3e953daaa2dca60aac7521a7b4633d12652519a2e2baee39e2b539c85ac5bdb82a9f237'))
        #'name' should be 'medicationName' but it errors
        self.assertEqual(medication.text, "Added " + payload["name"])


    def testLegitimateSecurity(self):
        payload = {
            "name" : "test"
        }

        medication = requests.post("http://127.0.0.1:9999/api/deleteMedication", data=payload, auth=('Security','73630002494546d52bdc16cf5874a41e720896b566cd8cb72afcf4f866d70570aa078832f3e953daaa2dca60aac7521a7b4633d12652519a2e2baee39e2b539c85ac5bdb82a9f237'))
        #'name' should be 'medicationName' but it errors
        self.assert_response(401)


    def testNullValue(self):
        payload = {
            "name" : None
        }

        prescription = requests.post("http://127.0.0.1:9999/api/deleteMedication", data=payload, auth=('patient','73630002494546d52bdc16cf5874a41e720896b566cd8cb72afcf4f866d70570aa078832f3e953daaa2dca60aac7521a7b4633d12652519a2e2baee39e2b539c85ac5bdb82a9f237'))
        self.assertEqual(testDatabase.Medication.select().count(), 0)

    def testNullValueSecurity(self):
        payload = {
            "name" : None
        }

        prescription = requests.post("http://127.0.0.1:9999/api/deleteMedication", data=payload, auth=('Security','73630002494546d52bdc16cf5874a41e720896b566cd8cb72afcf4f866d70570aa078832f3e953daaa2dca60aac7521a7b4633d12652519a2e2baee39e2b539c85ac5bdb82a9f237'))
        self.assert_response(401)


    def tearDown(self):
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()