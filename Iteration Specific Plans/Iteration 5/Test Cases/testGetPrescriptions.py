from peewee import *
from passlib.hash import sha256_crypt
import requests
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

        testPrescription = testDatabase.Prescription.insert(
            username = "test",  
            medication = "test",
            dosage = 1,
            dosageunit = "test",
            frequency = 1,
            quantity = 1,
            frequencyunit = "test",
            startdate = '01/01/2020',
            enddate = '01/01/2020',
            repeat = "test",
            stockleft = 1,
            prerequisite = "test",
            dosageform = "test")
        testPrescription.execute()

    def testLegitimate(self):
        payload = {
            "username" : "test"
        }

        prescription = requests.post("http://127.0.0.1:9999/api/getPrescriptions", data=payload)
        prescription = json.loads(prescription.text)
        prescription = prescription[0]
        self.assertEqual(prescription['username'], "test")
        self.assertEqual(prescription['medication'], "test")
        self.assertEqual(prescription['dosage'], 1)
        self.assertEqual(prescription['dosageunit'], "test")
        self.assertEqual(prescription['frequency'], 1)
        self.assertEqual(prescription['quantity'], 1)
        self.assertEqual(prescription['frequencyunit'], "test")
        self.assertEqual(prescription['startdate'], '01/01/2020')
        self.assertEqual(prescription['enddate'], '01/01/2020')
        self.assertEqual(prescription['repeat'], "test")
        self.assertEqual(prescription['stockleft'], 1)
        self.assertEqual(prescription['prerequisite'], "test")
        self.assertEqual(prescription['dosageform'], "test")

    def testNullValues(self):
        payload = {
            "username" : None
        }
        
        prescription = requests.post("http://127.0.0.1:9999/api/getPrescriptions", data=payload)
        self.assertEqual(prescription.text, "No username given")

    def testInvalidUsername(self):
        payload = {
            "username" : "1234"
        }

        prescription = requests.post("http://127.0.0.1:9999/api/getPrescriptions", data=payload)
        self.assertEqual(prescription.text, "Invalid username")

    def tearDown(self):
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()