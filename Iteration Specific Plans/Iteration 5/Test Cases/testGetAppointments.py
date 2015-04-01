from peewee import *
from passlib.hash import sha256_crypt
import requests
from requests.auth import HTTPBasicAuth
import unittest
import imp
import json

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

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

        appointment = testDatabase.Appointmenttype.insert(
            type = "test")
        appointment.execute()

        testAppointment = testDatabase.Appointments.insert(
            creator = "test",
            invitee = "test",
            name = "test",
            apptype = "test",
            addressnamenumber = "Test",
            postcode = "Test",
            startdate = "01/01/2020",
            starttime = "00:00",
            enddate = "01/01/2020",
            endtime ="00:00",
            description = "Test",
            private = True)
        testAppointment.execute()

    def testLegitimate(self):
        payload = {
            "user" : "test",
            "appid" : 1
        }

        expectedResult = {
            "appid" : 1,
            "name" : "test",
            "apptype" : "test",
            "addressnamenumber" : "Test",
            "postcode" : "Test",
        }

        appointment = requests.post("http://127.0.0.1:9999/api/getAppointment", data=payload, auth=HTTPBasicAuth("test", '7363000274128bb03e7418d95d4dd26eeb00a86e7b4f06ad70f186f6948945a687c9f855cca6cafd8e72b2602aa48255ed2e2aabb7d6eafd5751761369049a8b3d34ffb4305b3b76'))
        response = json.loads(appointment.text)
        self.assertEqual(response['appid'], expectedResult['appid'])
        self.assertEqual(response['name'], expectedResult['name'])
        self.assertEqual(response['apptype'], expectedResult['apptype'])
        self.assertEqual(response['addressnamenumber'], expectedResult['addressnamenumber'])
        self.assertEqual(response['postcode'], expectedResult['postcode'])

    def testNullValues(self):
        payload = {
            "user" : "test",
            "appid" : None
        }

        appointment = requests.post("http://127.0.0.1:9999/api/getAppointment", data=payload, auth=HTTPBasicAuth("test", '7363000274128bb03e7418d95d4dd26eeb00a86e7b4f06ad70f186f6948945a687c9f855cca6cafd8e72b2602aa48255ed2e2aabb7d6eafd5751761369049a8b3d34ffb4305b3b76'))
        self.assertEqual(appointment.text, "Your request appears to be malformed")

    def testDoesNotExist(self):
        payload = {
            "user" : "test",
            "appid" : 2
        }

        appointment = requests.post("http://127.0.0.1:9999/api/getAppointment", data=payload, auth=HTTPBasicAuth("test", '7363000274128bb03e7418d95d4dd26eeb00a86e7b4f06ad70f186f6948945a687c9f855cca6cafd8e72b2602aa48255ed2e2aabb7d6eafd5751761369049a8b3d34ffb4305b3b76'))
        self.assertEqual(appointment.text, "Appointment does not exist")

    def tearDown(self):
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
