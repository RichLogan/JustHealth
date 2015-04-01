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

class testGetAppointmentsDueIn30(unittest.TestCase):
    """Testing the getAppointmentsDueIn30 API method"""

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

        #create test user 2
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

        appointmentInsert2 = testDatabase.Appointments.insert(
            creator = "carer1",
            name = "test",
            apptype = "Doctors",
            addressnamenumber = "11",
            postcode = "SS17 9AY",
            startdate = datetime.datetime.now().date(),
            starttime = (datetime.datetime.now() + datetime.timedelta(minutes = 45)).time(),
            enddate = datetime.datetime.now().date() + timedelta(days=3),
            endtime = datetime.datetime.now().time(),
            description = "",
            private = False
        )
        appointmentInsert2.execute()

    def testLegitimate(self):
        """Attempt to check a appointment that is due in the next 30mins || check that API returns expected response and DB is correct too"""
        response = api.getAppointmentsDueIn30('patient', datetime.datetime.now())

        result = {}
        result['creator'] = "patient"
        result['startdate'] = datetime.datetime.now().date()
        result['enddate'] = datetime.datetime.now().date() + timedelta(days=3)
        result['name'] = "test"
        result['apptype'] = "Doctors"

        reminder = response[0]

        self.assertEqual(reminder['creator'], result['creator'])
        self.assertEqual(reminder['startdate'], result['startdate'])
        self.assertEqual(reminder['enddate'], result['enddate'])
        self.assertEqual(reminder['name'], result['name'])
        self.assertEqual(reminder['apptype'], result['apptype'])
        
    def testNotDueIn30(self):
        """Attempt to check appointment that is not due in the next 30mins || check that the API returns expected response and nothing has been added to the DB"""
        response = api.getAppointmentsDueIn30('carer1', datetime.datetime.now())
        self.assertEqual(len(response), 0)

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()

