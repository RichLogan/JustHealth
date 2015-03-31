from peewee import *
from passlib.hash import sha256_crypt
import requests
from requests.auth import HTTPBasicAuth
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

        securityClient = testDatabase.Client.insert(
            username = "Security",
            email = "Security@richlogan.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        securityClient.execute()

        testSecurity = testDatabase.Patient.insert(
            username = "Security",
            firstname = "Security",
            surname = "Security",
            ismale = True)
        testSecurity.execute()

        securityPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "Security")
        securityPassword.execute()

    def testPatientToCarer(self):
        """Attempt to create a connection from Patient to Carer"""

        passwordPayload = {"password" : "test"}
        password = requests.post("http://127.0.0.1:9999/api/encryptPassword", data=passwordPayload)

        payload = {"username" : "patient", "target" : "carer"}

        result = requests.post("http://127.0.0.1:9999/api/createConnection", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(len(str(result)), 4)



    def testCarerToPatient(self):
    	"""Attempt to create a connection from Carer to Patient"""

        payload = {
            "username" : "carer",
            "target" : "patient"
        }

        result = requests.post("http://127.0.0.1:9999/api/createConnection", data=payload, auth=HTTPBasicAuth('carer', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(len(str(result)), 4)


    def testUserDoesNotExist(self):
    	"""Attempt to create a connection from Carer to invalid user"""

        payload = {
            "username" : "carer",
            "target" : "nonexistant"
        }

        result = requests.post("http://127.0.0.1:9999/api/createConnection", data=payload, auth=HTTPBasicAuth('carer', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(result.text, "User does not exist")



    def testRequestInPlace(self):
        """Attempt to connect where a request is already in place"""
        payload = {
            "username" : "carer",
            "target" : "patient"
        }
        result = requests.post("http://127.0.0.1:9999/api/createConnection", data=payload, auth=HTTPBasicAuth('carer', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        
        payload = {
            "username" : "patient",
            "target" : "carer"
        }
        result = requests.post("http://127.0.0.1:9999/api/createConnection", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
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
        result = requests.post("http://127.0.0.1:9999/api/createConnection", data=payload, auth=('carer','73630002494546d52bdc16cf5874a41e720896b566cd8cb72afcf4f866d70570aa078832f3e953daaa2dca60aac7521a7b4633d12652519a2e2baee39e2b539c85ac5bdb82a9f237'))
        self.assertEqual(result.text, "Already Connected")



    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
