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

    def testLegitimate(self):
        payload = {
            "name" : "test"
        }

        medication = requests.post("http://127.0.0.1:9999/api/deleteMedication", data=payload)
        #'name' should be 'medicationName' but it errors
        self.assertEqual(medication.text, "Added " + payload["name"])

    def testNullValue(self):
        payload = {
            "name" : None
        }

        prescription = requests.post("http://127.0.0.1:9999/api/deleteMedication", data=payload)
        self.assertEqual(testDatabase.Medication.select().count(), 0)

    def tearDown(self):
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()