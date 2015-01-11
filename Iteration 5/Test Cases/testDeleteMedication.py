from peewee import *
from passlib.hash import sha256_crypt
import requests
import unittest
import imp
import json

testDatabase = imp.load_source('testDatabase', '../../Website/justHealthServer/testDatabase.py')

class testDeleteMedication(unittest.TestCase):

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

        testMedication = testDatabase.Medication.insert(
            name = "test")
        testMedication.execute()

    def deleteWorks(self):
        payload = {
            "name" : "test"
        }

        prescription = requests.post("http://127.0.0.1:9999/api/testDeleteMedication", data=payload)
        self.assertEqual(prescription.text, "Deleted")

    def deleteFailed(self):
        payload = {
            "name" : None
        }

        prescription = requests.post("http://127.0.0.1:9999/api/testDeleteMedication", data=payload)
        self.assertEqual(prescription.text, "Failed")

    def tearDown(self):
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()