from peewee import *
from passlib.hash import sha256_crypt
import requests
import unittest
import imp
import json

testDatabase = imp.load_source('testDatabase', '../../Website/justHealthServer/testDatabase.py')

class testGetAppointments(unittest.TestCase):

    def setUp(self):
        testDatabase.createAll()
        #Create a Client entry, a Patient entry, an appointment  and a password.
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

        testAppointment = testDatabase.Appointments.insert(
            creator = "test",
            invitee = "test",
            name = "test",
            apptype = "test",
            addressnamenumber = "Test",
            postcode = "Test",
            startdate = 01/01/2020,
            starttime = 00:00,
            enddate = 01/01/2020,
            endtime = 00:00,
            description = "Test",
            private = True)       
        testAppointment.execute()

    def testLegitimate(self):
        payload = {
            "creator" : "test",
            "invitee" : "test",
            "name" : "test",
            "apptype" : "test",
            "addressnamenumber" : "Test",
            "postcode" : "Test",
            "startdate" : "01/01/2020",
            "starttime" : "00:00",
            "enddate" : "01/01/2020",
            "endtime" : "00:00",
            "description" : "Test",
            "private" : True           
        }

        appointment = requests.post("http://127.0.0.1:9999/api/addPatientAppointment", data=payload)
        self.assertEqual(appointment.text, "Appointment Added")

    def testNullValues(self):
        payload = {
            "creator" : "test",
            "invitee" : "test",
            "name" : "test",
            "apptype" : "test",
            "addressnamenumber" : "Test",
            "postcode" : "Test",
            "startdate" : "01/01/2020",
            "starttime" : "00:00",
            "enddate" : "01/01/2020",
            "endtime" : "00:00",
            "description" : "Test",
            "private" : True
        }

        for key in payload:
            payload = {
                "creator" : "test",
                "invitee" : "test",
                "name" : "test",
                "apptype" : "test",
                "addressnamenumber" : "Test",
                "postcode" : "Test",
                "startdate" : "01/01/2020",
                "starttime" : "00:00",
                "enddate" : "01/01/2020",
                "endtime" : "00:00",
                "description" : "Test",
                "private" : True
            }
            payload[key] = None
            appointment = requests.post("http://127.0.0.1:9999/api/addPatientAppointment", data=payload)
            self.assertEqual(testDatabase.Appointments.select().count(), 1)

    def tearDown(self):
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()