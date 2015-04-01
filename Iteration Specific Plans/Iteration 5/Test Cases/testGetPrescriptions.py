from peewee import *
from passlib.hash import sha256_crypt
import requests
from requests.auth import HTTPBasicAuth
import unittest
import imp
import json

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testGetPrescriptions(unittest.TestCase):

    def setUp(self):
        testDatabase.createAll()
		#Create a Client entry, a Patient entry, a prescription  and a password.
        testClient = testDatabase.Client.insert(
            username = "test",
            email = "justhealth@richlogan.co.uk",
            dob = "1993-03-03",
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
            expirydate = '2020-01-01',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "test")
        testPassword.execute()

        testMedication = testDatabase.Medication.insert(
            name = "test")
        testMedication.execute()

        testPrescription = testDatabase.Prescription.insert(
            username = "test",
            medication = "test",
            dosage = 1,
            dosageunit = "test",
            stockleft = 100,
            prerequisite = "None",
            dosageform = "Tablet",
            quantity = 50,
            frequency = 1,
            Monday = True,
            Tuesday = True,
            Wednesday = True,
            Thursday = True,
            Friday = True,
            Saturday = True,
            Sunday = True,
            startdate = "2020-01-01",
            enddate = "2020-01-01"
        )
        testPrescription.execute()

    def testLegitimate(self):
        payload = {
            "username" : "test"
        }

        prescription = requests.post("http://127.0.0.1:9999/api/getPrescriptions", data=payload, auth=('test', '73630002494546d52bdc16cf5874a41e720896b566cd8cb72afcf4f866d70570aa078832f3e953daaa2dca60aac7521a7b4633d12652519a2e2baee39e2b539c85ac5bdb82a9f237'))
        prescription = json.loads(prescription.text)
        prescription = prescription[0]
        
        self.assertEqual(prescription['username'], "test")
        self.assertEqual(prescription['medication'], "test")
        self.assertEqual(prescription['dosage'], 1)
        self.assertEqual(prescription['dosageunit'], "test")
        self.assertEqual(prescription['stockleft'], 100)
        self.assertEqual(prescription['prerequisite'], "None")
        self.assertEqual(prescription['dosageform'], "Tablet")
        self.assertEqual(prescription['quantity'], 50)
        self.assertEqual(prescription['frequency'], 1)
        self.assertEqual(prescription['Monday'], True)
        self.assertEqual(prescription['Tuesday'], True)
        self.assertEqual(prescription['Wednesday'], True)
        self.assertEqual(prescription['Thursday'], True)
        self.assertEqual(prescription['Friday'], True)
        self.assertEqual(prescription['Saturday'], True)
        self.assertEqual(prescription['Sunday'] , True)
        self.assertEqual(prescription['startdate'], "2020-01-01")
        self.assertEqual(prescription['enddate'], "2020-01-01")

    def tearDown(self):
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()