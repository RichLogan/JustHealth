from peewee import *
from passlib.hash import sha256_crypt
import requests
import unittest
import imp
from requests.auth import HTTPBasicAuth
import json
from passlib.hash import sha256_crypt

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testDeleteConnection(unittest.TestCase):
    """Testing that a patient/carer can successfully delete an existing completed connection"""

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

        testRelationship = testDatabase.Patientcarer.insert(
            carer = "carer",
            patient = "patient")
        testRelationship.execute()

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

    def testValidDelete(self):
        """Atempt to delete a connection"""
        payload = {
            "user" : "patient",
            "connection" : "carer",
        }
        result = requests.post("http://127.0.0.1:9999/api/deleteConnection", data=payload,  auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(result.text, "True")

    def testInvalidDelete(self):
        """Attempt to delete a connection that does not exists"""
        payload = {
            "user" : "patient",
            "connection" : "1234",
        }
        result = requests.post("http://127.0.0.1:9999/api/deleteConnection", data=payload,  auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(result.text, "Connection does not exist")

        payload = {
            "user" : "carer",
            "connection" : "1234",
        }
        result = requests.post("http://127.0.0.1:9999/api/deleteConnection", data=payload,  auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(result.text, "Connections does not exist")

 
    
    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
