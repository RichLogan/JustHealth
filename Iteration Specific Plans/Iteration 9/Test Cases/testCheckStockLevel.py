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

class testCheckStockLevel(unittest.TestCase):

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
            accountdeactivated = False,
            profilepicture = "default.png"
        )
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
            accountdeactivated = False,
            profilepicture = "default.png"
        )
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

        patientC = testDatabase.Patientcarer.insert(
            patient = "patient",
            carer = "carer"
        ).execute()

        ntype1 = testDatabase.Notificationtype.insert(
            typename = "Medication Low",
            typeclass = "danger"
        ).execute()
        ntype2 = testDatabase.Notificationtype.insert(
            typename = "Patient Medication Low",
            typeclass = "danger"
        ).execute()

        # New Prescription
        medication = testDatabase.Medication.insert(name = "Morphine").execute()
        prescription = testDatabase.Prescription.insert(
            prescriptionid = 1,
            username = "patient",
            medication = "Morphine",
            dosage = 25,
            dosageunit = "Mg",
            stockleft = 5,
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
        
    def testCheckNotifications(self):
        """Check the correct notifications are generated"""
        payload = {
            "prescriptionid" : 1,
            "currentcount" : "3"
        }
        takePrescription = api.takePrescription(payload)

        self.assertEqual(testDatabase.Notification.select().where(testDatabase.Notification.notificationtype == "Medication Low").count(), 1)
        self.assertEqual(testDatabase.Notification.select().where(testDatabase.Notification.notificationtype == "Patient Medication Low").count(), 1)

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
