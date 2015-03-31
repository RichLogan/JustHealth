from peewee import *
from passlib.hash import sha256_crypt
import requests
from requests.auth import HTTPBasicAuth
import datetime
import unittest
import imp
import json

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testDeletePrescriptions(unittest.TestCase):

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

        testClientCarer = testDatabase.Client.insert(
            username = "carer",
            email = "justhealth@richlogan.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        testClientCarer.execute()

        testCarer = testDatabase.Carer.insert(
            username = "carer",
            firstname = "test",
            surname = "test",
            ismale = True)
        testCarer.execute()

        testPasswordCarer = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "carer")
        testPasswordCarer.execute()

        relationship = testDatabase.Patientcarer.insert(
            patient = "test",
            carer = "carer")
        relationship.execute()

        testMedication = testDatabase.Medication.insert(
            name = "test")
        testMedication.execute()

        testPrescription = testDatabase.Prescription.insert(
            username = "test",  
            medication = "test",
            dosage = 1,
            dosageunit = "test",
            quantity = 1,
            startdate = datetime.datetime.now().date(),
            enddate = '01/01/2020',
            stockleft = 1,
            prerequisite = "test",
            dosageform = "test",
            frequency = 1,
            Monday = True,
            Tuesday = True,
            Wednesday = True,
            Thursday = True, 
            Friday = True, 
            Saturday = True,
            Sunday = True
        )
        testPrescription.execute()

    def testLegitimate(self):
        payload = {
            "prescriptionid" : 1
        }

        prescription = requests.post("http://127.0.0.1:9999/api/deletePrescription", data=payload, auth=HTTPBasicAuth('carer', '7363000274128bb03e7418d95d4dd26eeb00a86e7b4f06ad70f186f6948945a687c9f855cca6cafd8e72b2602aa48255ed2e2aabb7d6eafd5751761369049a8b3d34ffb4305b3b76'))
        self.assertEqual(prescription.text, "Deleted")
        self.assertEqual(testDatabase.Prescription.select().count(), 0)

    def testNullValues(self):
        payload = {
            "prescriptionid" : None
        }

        prescription = requests.post("http://127.0.0.1:9999/api/deletePrescription", data=payload, auth=HTTPBasicAuth('carer', '7363000274128bb03e7418d95d4dd26eeb00a86e7b4f06ad70f186f6948945a687c9f855cca6cafd8e72b2602aa48255ed2e2aabb7d6eafd5751761369049a8b3d34ffb4305b3b76'))
        self.assertEqual(prescription.text, "Your request appears to be malformed")
        self.assertEqual(testDatabase.Prescription.select().count(), 1)

    def testNonExistentValues(self):
        payload = {
            "prescriptionid" : 2
        }

        prescription = requests.post("http://127.0.0.1:9999/api/deletePrescription", data=payload, auth=HTTPBasicAuth('carer', '7363000274128bb03e7418d95d4dd26eeb00a86e7b4f06ad70f186f6948945a687c9f855cca6cafd8e72b2602aa48255ed2e2aabb7d6eafd5751761369049a8b3d34ffb4305b3b76'))
        self.assertEqual(prescription.text, "Failed")
        self.assertEqual(testDatabase.Prescription.select().count(), 1)

    def tearDown(self):
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()