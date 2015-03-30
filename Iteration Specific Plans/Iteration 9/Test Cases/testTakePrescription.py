import unittest
from peewee import *
import datetime
import imp
import sys
from passlib.hash import sha256_crypt
import requests

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

#import the api so we are able to run locally
sys.path.insert(0, 'Website')
import justHealthServer
from justHealthServer import api

class testTakePrescription(unittest.TestCase):

    def setUp(self):
        """Create all the tables that are needed"""
        testDatabase.createAll()

        # Create a test Patient
        patientClient = testDatabase.Client.insert(
            username = "patient",
            email = "justhealth123@richlogan.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        testPatient = testDatabase.Patient.insert(
            username = "patient",
            firstname = "patient",
            surname = "patient",
            ismale = True)
        patientPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "patient")
        patientClient.execute()
        testPatient.execute()
        patientPassword.execute()

        # Test Carer
        carerClient = testDatabase.Client.insert(
            username = "carer",
            email = "carer1@sjtate.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        carerCarer = testDatabase.Carer.insert(
            username = "carer",
            firstname = "carer",
            ismale = True,
            nhscarer = True,
            surname = "carer")
        carerPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "carer")
        carerClient.execute()
        carerCarer.execute()
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

    def testTakePrescriptionLegitimate(self):
        """Attempt to take a prescription"""
        payload = {
            "prescriptionid" : "1",
            "currentcount" : "3"
        }
        takePrescription = api.takePrescription(payload)
        self.assertEqual(takePrescription, "True")

    def testTakePrescriptionDoesNotExist(self):
        """Attept to take a prescription that does not exist"""
        payload = {
            "prescriptionid" : "10",
            "currentcount" : "3"
        }
        takePrescription = api.takePrescription(payload)
        self.assertEqual(takePrescription, "Specified prescription does not exist")

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
