import unittest
from peewee import *
import datetime
import imp
from passlib.hash import sha256_crypt
import requests

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testGetPrescriptionCount(unittest.TestCase):

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

        # Carer1
        carerClient = testDatabase.Client.insert(
            username = "carer1",
            email = "carer1@sjtate.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        carerClient.execute()

        carerCarer = testDatabase.Carer.insert(
            username = "carer1",
            firstname = "carer",
            ismale = True,
            nhscarer = True,
            surname = "carer")
        carerCarer.execute()

        carerPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "carer1")
        carerPassword.execute()

        # New Prescription
        medication = testDatabase.Medication.insert(name = "Morphine").execute()
        prescription = testDatabase.Prescription.insert(
            prescriptionid = 1,
            username = "patient",
            medication = "Morphine",
            dosage = 25,
            dosageunit = "Mg",
            stockleft = 100,
            prerequisite = "None",
            dosageform = "Tablet",
            quantity = 1,
            frequency = 5,
            Monday = True,
            Tuesday = True,
            Wednesday = True,
            Thursday = True,
            Friday = True,
            Saturday = True,
            Sunday = True).execute()
        
        payload = {
            "prescriptionid" : "1",
            "currentcount" : "3"
        }
        takePrescription = requests.post("http://127.0.0.1:9999/api/takePrescription", data=payload)

    def testGetPrescriptionCountLegitimate(self):
        """Attempt to get the prescription count"""
        payload = { "prescriptionid" : "1" }
        expectedResult = '3'
    
        getPrescriptionCount = requests.post("http://127.0.0.1:9999/api/getPrescriptionCount", data=payload)
        self.assertEqual(getPrescriptionCount.text, expectedResult)

    def tearDown(self):
        """Delete all tables"""
        #testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
