from peewee import *
from passlib.hash import sha256_crypt
import requests
from requests.auth import HTTPBasicAuth
import unittest
import imp
import json

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testAddAppointment(unittest.TestCase):

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

        appType = testDatabase.Appointmenttype.insert(
            type = "test").execute()


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

        appointment = requests.post("http://127.0.0.1:9999/api/addPatientAppointment", data=payload, auth=HTTPBasicAuth('test', '7363000274128bb03e7418d95d4dd26eeb00a86e7b4f06ad70f186f6948945a687c9f855cca6cafd8e72b2602aa48255ed2e2aabb7d6eafd5751761369049a8b3d34ffb4305b3b76'))
        self.assertEqual(appointment.text, "1")

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
            appointment = requests.post("http://127.0.0.1:9999/api/addPatientAppointment", data=payload, auth=HTTPBasicAuth('test', '7363000274128bb03e7418d95d4dd26eeb00a86e7b4f06ad70f186f6948945a687c9f855cca6cafd8e72b2602aa48255ed2e2aabb7d6eafd5751761369049a8b3d34ffb4305b3b76'))
            self.assertEqual(testDatabase.Appointments.select().count(), 1)

    def tearDown(self):
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()