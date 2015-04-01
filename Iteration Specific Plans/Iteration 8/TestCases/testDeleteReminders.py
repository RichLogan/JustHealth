from peewee import *
from passlib.hash import sha256_crypt
from datetime import timedelta
import unittest
import imp
import datetime
import sys

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

#import the api so we are able to run locally
sys.path.insert(0, 'Website')
import justHealthServer
from justHealthServer import api

class testCreateReminder(unittest.TestCase):
    """Testing the deleteReminder API method"""

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
            starttime = (datetime.datetime.now() - datetime.timedelta(minutes = 20)).time(),
            enddate = datetime.datetime.now().date(),
            endtime = (datetime.datetime.now() - datetime.timedelta(minutes = 10)).time(),
            description = "",
            private = True)
        appointmentid = int(appointmentInsert.execute())

        reminderInsert = testDatabase.Reminder.insert(
            username = 'patient',
            content = 'test',
            reminderClass = 'info',
            relatedObject = appointmentid,
            relatedObjectTable = 'Appointments',
            extraDate = datetime.datetime.now() - datetime.timedelta(minutes=10)
        )
        reminderInsert.execute()

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
            startdate = datetime.datetime.now().date(),
            starttime = (datetime.datetime.now() + datetime.timedelta(minutes = 20)).time(),
            enddate = datetime.datetime.now().date() + timedelta(days=3),
            endtime = datetime.datetime.now().time(),
            description = "",
            private = True)
        appointmentid2 = int(appointmentInsert2.execute())

        reminderInsert2 = testDatabase.Reminder.insert(
            username = 'patient2',
            content = 'test',
            reminderClass = 'info',
            relatedObject = appointmentid2,
            relatedObjectTable = 'Appointments',
            extraDate = datetime.datetime.now().date() + timedelta(days=3)
        )
        reminderInsert2.execute()

    def testLegitimate(self):
        """Attempt to delete a reminder"""
        api.deleteReminders('patient', datetime.datetime.now())

        self.assertEqual(testDatabase.Reminder.select().where(testDatabase.Reminder.username == 'patient').count(),0)

    def testNotDelete(self):
        """Attempt to delete a reminder when it should not be deleted"""
        api.deleteReminders('patient2', datetime.datetime.now())

        self.assertEqual(testDatabase.Reminder.select().where(testDatabase.Reminder.username == 'patient2').count(),1)

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
