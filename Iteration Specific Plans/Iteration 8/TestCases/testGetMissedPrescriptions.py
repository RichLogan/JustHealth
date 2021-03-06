from peewee import *
from datetime import timedelta
from passlib.hash import sha256_crypt
import unittest
import imp
import datetime
import sys

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

#import the api so we are able to run locally
sys.path.insert(0, 'Website')
import justHealthServer
from justHealthServer import api

class testGetAppointmentsDueNow(unittest.TestCase):
    """Testing the getAppointmentsDueNow API method"""

    def setUp(self):
        """Create all the tables that are needed"""
        testDatabase.createAll()

        #create test user 1
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

        testMedication = testDatabase.Medication.insert(
            name = "test")
        testMedication.execute()

        testPrescription = testDatabase.Prescription.insert(
            username = "patient",  
            medication = "test",
            dosage = 1,
            dosageunit = "test",
            quantity = 1,
            startdate = datetime.datetime.now().date() - datetime.timedelta(days=1),
            enddate = '01/01/2020',
            stockleft = 100,
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
        prescriptionid = int(testPrescription.execute())

        takePrescription = testDatabase.TakePrescription.insert(
            prescriptionid = prescriptionid,
            currentcount = 0,
            startingcount = 100,
            currentdate = datetime.datetime.now().date() - datetime.timedelta(days=1))
        takePrescription.execute()

        #create test user 2
        patientClient2 = testDatabase.Client.insert(
            username = "patient2",
            email = "justhealth123@sjtate.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        patientClient2.execute()

        testPatient2 = testDatabase.Patient.insert(
            username = "patient2",
            firstname = "patient",
            surname = "patient",
            ismale = True)
        testPatient2.execute()

        patientPassword2 = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "patient2")
        patientPassword2.execute()

        testPrescription2 = testDatabase.Prescription.insert(
            username = "patient2",  
            medication = "test",
            dosage = 1,
            dosageunit = "test",
            quantity = 1,
            startdate = datetime.datetime.now().date() + datetime.timedelta(days = 3),
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
        testPrescription2.execute()

        notification = testDatabase.Notificationtype.insert(
            typename = "Missed Prescription",
            typeclass = "danger").execute()

    def testLegitimate(self):
        """Attempt to check an prescription that is due to be taken today"""
        api.checkMissedPrescriptions('patient', datetime.datetime.now().date())

        self.assertEqual(testDatabase.Notification.select().where(testDatabase.Notification.username == 'patient').count(),1)

    def testNotToday(self):
        """Attempt to check a prescription that is not due to be taken today"""
        api.checkMissedPrescriptions('patient2', datetime.datetime.now().date())

        self.assertEqual(testDatabase.Notification.select().where(testDatabase.Notification.username == 'patient2').count(),0)

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()