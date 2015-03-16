from peewee import *
from passlib.hash import sha256_crypt
import requests
import unittest
import imp
import json

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
        result = requests.post("http://127.0.0.1:9999/api/deleteConnection", data=payload, auth=('patient', '73630002494546d52bdc16cf5874a41e720896b566cd8cb72afcf4f866d70570aa078832f3e953daaa2dca60aac7521a7b4633d12652519a2e2baee39e2b539c85ac5bdb82a9f237'))
        self.assertEqual(result.text, "True")

    def testValidDeleteSecurity(self):
        """Atempt to delete a connection Security"""
        payload = {
            "user" : "patient",
            "connection" : "carer",
        }
        result = requests.post("http://127.0.0.1:9999/api/deleteConnection", data=payload, auth=('Security', '73630002494546d52bdc16cf5874a41e720896b566cd8cb72afcf4f866d70570aa078832f3e953daaa2dca60aac7521a7b4633d12652519a2e2baee39e2b539c85ac5bdb82a9f237'))
        self.assertEqual(result.status_code, 401)

    def testInvalidDelete(self):
        """Attempt to delete a connection that does not exists"""
        payload = {
            "user" : "patient",
            "connection" : "1234",
        }
        result = requests.post("http://127.0.0.1:9999/api/deleteConnection", data=payload, auth=('patient', '73630002494546d52bdc16cf5874a41e720896b566cd8cb72afcf4f866d70570aa078832f3e953daaa2dca60aac7521a7b4633d12652519a2e2baee39e2b539c85ac5bdb82a9f237'))
        self.assertEqual(result.text, "Connection does not exist")

        payload = {
            "user" : "carer",
            "connection" : "1234",
        }
        result = requests.post("http://127.0.0.1:9999/api/deleteConnection", data=payload, auth=('patient', '73630002494546d52bdc16cf5874a41e720896b566cd8cb72afcf4f866d70570aa078832f3e953daaa2dca60aac7521a7b4633d12652519a2e2baee39e2b539c85ac5bdb82a9f237'))
        self.assertEqual(result.text, "Connections does not exist")

    def testInvalidDeleteSecurity(self):
        """Attempt to delete a connection that does not exists"""
        payload = {
            "user" : "patient",
            "connection" : "1234",
        }
        result = requests.post("http://127.0.0.1:9999/api/deleteConnection", data=payload, auth=('Security', '73630002494546d52bdc16cf5874a41e720896b566cd8cb72afcf4f866d70570aa078832f3e953daaa2dca60aac7521a7b4633d12652519a2e2baee39e2b539c85ac5bdb82a9f237'))
        self.assertEqual(result.text, "Connection does not exist")

        payload = {
            "user" : "carer",
            "connection" : "1234",
        }
        result = requests.post("http://127.0.0.1:9999/api/deleteConnection", data=payload, auth=('Security', '73630002494546d52bdc16cf5874a41e720896b566cd8cb72afcf4f866d70570aa078832f3e953daaa2dca60aac7521a7b4633d12652519a2e2baee39e2b539c85ac5bdb82a9f237'))
        self.assertEqual(result.status_code, 401)

    
    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
