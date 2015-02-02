from peewee import *
from passlib.hash import sha256_crypt
import requests
import unittest
import imp
import json

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testCreateConnection(unittest.TestCase):
    """Testing that a patient/carer can request to connect"""

    def setUp(self):
        """Create needed tables and example record"""
        testDatabase.createAll()
	    #Create a Client entry and a Patient entry
        carerClient = testDatabase.Client.insert(
            username = "carer",
            email = "justhealth@richlogan.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        carerClient.execute()

        carerCarer = testDatabase.Carer.insert(
            username = "carer",
            firstname = "carer",
            ismale = True,
            nhscarer = True,
            surname = "carer")
        carerCarer.execute()

        carerPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "carer")
        carerPassword.execute()

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

    def testPatientToCarer(self):
        """Attempt to create a connection from Patient to Carer"""

        payload = {
            "username" : "patient",
            "target" : "carer"
        }

        result = requests.post("http://127.0.0.1:9999/api/createConnection", data=payload, auth=('patient','test'))
        result = int(result.text)
        self.assertEqual(len(str(result)), 4)

    def testCarerToPatient(self):
    	"""Attempt to create a connection from Carer to Patient"""

        payload = {
            "username" : "carer",
            "target" : "patient"
        }

        result = requests.post("http://127.0.0.1:9999/api/createConnection", data=payload, auth=('carer','test'))
        result = int(result.text)
        self.assertEqual(len(str(result)), 4)

    def testUserDoesNotExist(self):
    	"""Attempt to create a connection from Carer to invalid user"""

        payload = {
            "username" : "carer",
            "target" : "nonexistant"
        }

        result = requests.post("http://127.0.0.1:9999/api/createConnection", data=payload, auth=('carer','test'))
        self.assertEqual(result.text, "User does not exist")

    def testRequestInPlace(self):
        """Attempt to connect where a request is already in place"""
        payload = {
            "username" : "carer",
            "target" : "patient"
        }
        result = requests.post("http://127.0.0.1:9999/api/createConnection", data=payload, auth=('carer','test'))
        
        payload = {
            "username" : "patient",
            "target" : "carer"
        }
        result = requests.post("http://127.0.0.1:9999/api/createConnection", data=payload, auth=('patient','test'))
        self.assertEqual(result.text, "Request Waiting")

    def testConnectionAlreadyEstablished(self):
        """Attempt to connect to a user already connected to"""
        connection = testDatabase.Patientcarer.insert(
            patient = "patient",
            carer = "carer")
        connection.execute()

        payload = {
            "username" : "carer",
            "target" : "patient"
        }
        result = requests.post("http://127.0.0.1:9999/api/createConnection", data=payload, auth=('carer','test'))
        self.assertEqual(result.text, "Already Connected")

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
