from peewee import *
from passlib.hash import sha256_crypt
import requests
from requests.auth import HTTPBasicAuth
import unittest
import imp
import json

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testAddPrescriptions(unittest.TestCase):

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

        testCarer = testDatabase.Carer.insert(
            username = "test",
            firstname = "test",
            surname = "test",
            ismale = True)
        testCarer.execute()

        testPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "test")
        testPassword.execute()

        testClient2= testDatabase.Client.insert(
            username = "patient",
            email = "justhealth@richlogan.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        testClient2.execute()

        testPatient = testDatabase.Carer.insert(
            username = "patient",
            firstname = "test",
            surname = "test",
            ismale = True)
        testPatient.execute()

        testPassword2 = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "patient")
        testPassword2.execute()

        relationship = testDatabase.Patientcarer.insert(
            patient="patient",
            carer="test")
        relationship.execute()

        testMedication = testDatabase.Medication.insert(
            name = "test")
        testMedication.execute()

        notification = testDatabase.Notificationtype.insert(
            typename = "Prescription Added",
            typeclass = "success").execute()

    def testLegitimate(self):
        payload = {
            "username" : "patient",
            "medication" : "test",
            "dosage" : "1",
            "dosageunit" : "test",
            "frequency" : "1",
            "quantity" : "1",
            "frequencyunit" : "test",
            "startdate" : "01/01/2020",
            "enddate" : "01/01/2020",
            "repeat" : "test",
            "stockleft" : "1",
            "prerequisite" : "test",
            "dosageform" : "test"
        }

        prescription = requests.post("http://127.0.0.1:9999/api/addPrescription", data=payload, auth=HTTPBasicAuth('test', '7363000274128bb03e7418d95d4dd26eeb00a86e7b4f06ad70f186f6948945a687c9f855cca6cafd8e72b2602aa48255ed2e2aabb7d6eafd5751761369049a8b3d34ffb4305b3b76'))
        self.assertEqual(prescription.text, "test 1test  added for patient")

    def testNullValues(self):
        payload = {
            "username" : None,
            "medication" : None,
            "dosage" : None,
            "dosageunit" : None,
            "frequency" : None,
            "quantity" : None,
            "frequencyunit" : None,
            "startdate" : None,
            "enddate" : None,
            "repeat" : None,
            "stockleft" : None,
            "prerequisite" : None,
            "dosageform" : None
        }
    
        prescription = requests.post("http://127.0.0.1:9999/api/addPrescription", data=payload, auth=HTTPBasicAuth('test', '7363000274128bb03e7418d95d4dd26eeb00a86e7b4f06ad70f186f6948945a687c9f855cca6cafd8e72b2602aa48255ed2e2aabb7d6eafd5751761369049a8b3d34ffb4305b3b76'))
        self.assertEqual(testDatabase.Prescription.select().count(), 0)

    def tearDown(self):
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()