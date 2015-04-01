from peewee import *
from passlib.hash import sha256_crypt
import requests
from requests.auth import HTTPBasicAuth
import unittest
import imp
import sys
import json

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

#import the api so we are able to run locally
sys.path.insert(0, 'Website')
import justHealthServer
from justHealthServer import api

class testAddMedication(unittest.TestCase):

    def setUp(self):
        testDatabase.createAll()
        #Create a Client entry, a Patient entry, a prescription  and a password.
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

        medication = testDatabase.Medication.insert(
            name = "test")
        medication.execute()

    def testLegitimate(self):
        request = api.deleteMedication("test")

        self.assertEqual(request, "Deleted test")
        self.assertEqual(testDatabase.Medication.select().count(), 0)

    def testNullValue(self):
        request = api.deleteMedication(None)

        self.assertEqual(testDatabase.Medication.select().count(), 1)
        self.assertEqual(request, "Unable to accept none type")

    def testNonExistent(self):
        request = api.deleteMedication("doesNotExist")

        self.assertEqual(testDatabase.Medication.select().count(), 1)
        self.assertEqual(request, "doesNotExist not found")

    def tearDown(self):
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()