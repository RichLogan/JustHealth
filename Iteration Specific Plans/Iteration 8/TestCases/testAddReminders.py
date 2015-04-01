from peewee import *
from passlib.hash import sha256_crypt
import datetime
from datetime import timedelta
import unittest
import imp
import sys

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

#import the api so we are able to run locally
sys.path.insert(0, 'Website')
import justHealthServer
from justHealthServer import api

class testAddReminder(unittest.TestCase):
    """Testing the createReminder API"""

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

        appointmentType = testDatabase.Appointmenttype.insert(
        	type = "Doctors")
        appointmentType.execute()

        appointmentInsert = testDatabase.Appointments.insert(
		    creator = "patient",
		    name = "test",
		    apptype = "Doctors",
		    addressnamenumber = "11",
		    postcode = "SS17 9AY",
		    startdate = datetime.datetime.now().date(),
		    starttime = (datetime.datetime.now() + datetime.timedelta(minutes = 20)).time(),
		    enddate = datetime.datetime.now().date() + timedelta(days=3),
		    endtime = datetime.datetime.now().time(),
		    description = "",
		    private = True)
        appointmentInsert.execute()

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
        testPrescription.execute()

        #create test user 2
        patientClient2 = testDatabase.Client.insert(
            username = "patient2",
            email = "justhealth123@richlogan.co.uk",
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

        appointmentInsert2 = testDatabase.Appointments.insert(
            creator = "patient2",
            name = "test",
            apptype = "Doctors",
            addressnamenumber = "11",
            postcode = "SS17 9AY",
            startdate = datetime.datetime.now().date() + datetime.timedelta(days=3),
            starttime = (datetime.datetime.now() + datetime.timedelta(minutes = 20)).time(),
            enddate = datetime.datetime.now().date() + timedelta(days=3),
            endtime = datetime.datetime.now().time(),
            description = "",
            private = True
        )
        appointmentInsert2.execute()

        testPrescription2 = testDatabase.Prescription.insert(
            username = "patient2",  
            medication = "test",
            dosage = 1,
            dosageunit = "test",
            quantity = 1,
            startdate = datetime.datetime.now().date() + datetime.timedelta(days=3),
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
        testPrescription2.execute()

    def testLegitimate(self):
        """Attempt to create a reminder"""
        api.addReminders('patient', datetime.datetime.now())
        
        self.assertEqual(testDatabase.Reminder.select().where(testDatabase.Reminder.username == 'patient').count(),2)

    def testNotToday(self):
        """Attempt to create a reminder when one should not be created"""
        api.addReminders('patient2', datetime.datetime.now())

        self.assertEqual(testDatabase.Reminder.select().where(testDatabase.Reminder.username == 'patient2').count(),0)

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
