from peewee import *
from datetime import timedelta
import requests
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
            startdate = datetime.datetime.now().date() + timedelta(days = 3),
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

    def testLegitimate(self):
        """Attempt to check an prescription that is due to be taken today"""
        response = api.getPrescriptionsDueToday('patient', datetime.datetime.now())

        result = {}
        result['username'] = "patient",  
        result['medication'] = "test",
        result['dosage'] = 1,
        result['dosageunit'] = "test",
        result['quantity'] = 1,
        result['startdate'] = datetime.datetime.now().date(),
        result['enddate'] = '01/01/2020',
        result['stockleft'] = 1,
        result['prerequisite'] = "test",
        result['dosageform'] = "test",
        result['frequency'] = 1,
        result['Monday'] = True,
        result['Tuesday'] = True,
        result['Wednesday'] = True,
        result['Thursday'] = True, 
        result['Friday'] = True, 
        result['Saturday'] = True,
        result['Sunday'] = True

        prescription = response[0]

        self.assertEqual(prescription['username'], result['username'])
        self.assertEqual(prescription['medication'], result['medication'])
        self.assertEqual(prescription['dosage'], result['dosage'])
        self.assertEqual(prescription['dosageunit'], result['dosageunit'])
        self.assertEqual(prescription['quantity'], result['quantity'])
        self.assertEqual(prescription['startdate'], result['startdate'])
        self.assertEqual(prescription['enddate'], result['enddate'])
        self.assertEqual(prescription['stockleft'], result['stockleft'])
        self.assertEqual(prescription['prerequisite'], result['prerequisite'])
        self.assertEqual(prescription['dosageform'], result['dosageform'])
        self.assertEqual(prescription['frequency'], result['frequency'])
        self.assertEqual(prescription['Monday'], result['Monday'])
        self.assertEqual(prescription['Tuesday'], result['Tuesday'])
        self.assertEqual(prescription['Wednesday'], result['Wednesday'])
        self.assertEqual(prescription['Thursday'], result['Thursday'])
        self.assertEqual(prescription['Friday'], result['Friday'])
        self.assertEqual(prescription['Saturday'], result['Saturday'])
        self.assertEqual(prescription['Sunday'], result['Sunday'])

    def testNotToday(self):
        """Attempt to check a prescription that is not due to be taken today"""
        response = api.getPrescriptionsDueToday('patient2', datetime.datetime.now())

        self.assertEqual(len(response), 0)

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
