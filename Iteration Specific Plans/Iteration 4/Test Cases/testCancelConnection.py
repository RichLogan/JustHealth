from peewee import *
from passlib.hash import sha256_crypt
import requests
import unittest
import imp
import json
from requests.auth import HTTPBasicAuth
import json
from passlib.hash import sha256_crypt

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testCancelConnection(unittest.TestCase):
    """Testing that a patient/carer can successfully reject an incoming connection request or cancel an outgoing"""

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

        testRelationship = testDatabase.Relationship.insert(
            code = 1234,
            requestor = "carer",
            requestortype = "Carer",
            target = "patient",
            targettype = "Patient")
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

    def testValidReject(self):
        """Atempt to reject an incoming connection"""
        payload = {
            "user" : "patient",
            "connection" : "carer",
        }
        result = requests.post("http://127.0.0.1:9999/api/cancelConnection", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(result.text, "True")

    def testValidRejectSecurity(self):
        """Atempt to reject an incoming connection Security"""
        payload = {
            "user" : "patient",
            "connection" : "carer",
        }
        result = requests.post("http://127.0.0.1:9999/api/cancelConnection", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assert_response(401)

    def testValidCancel(self):
        """Atempt to cancel an outgoing connection"""
        payload = {
            "user" : "carer",
            "connection" : "patient",
        }
        result = requests.post("http://127.0.0.1:9999/api/cancelConnection", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(result.text, "True")

    def testValidCancelSecurity(self):
        """Atempt to cancel an outgoing connection"""
        payload = {
            "user" : "carer",
            "connection" : "patient",
        }
        result = requests.post("http://127.0.0.1:9999/api/cancelConnection", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assert_response(401)

    def testInvalidReject(self):
        """Atempt to reject an nonexistant incoming connection"""
        payload = {
            "user" : "patient",
            "connection" : "1234",
        }
        result = requests.post("http://127.0.0.1:9999/api/cancelConnection", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(result.text, "False")


    def testInvalidRejectSecurity(self):
        """Atempt to reject an nonexistant incoming connection"""
        payload = {
            "user" : "patient",
            "connection" : "1234",
        }
        result = requests.post("http://127.0.0.1:9999/api/cancelConnection", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assert_response(401)

    def testInvalidCancel(self):
        """Atempt to cancel an nonexistant outgoing connection"""
        payload = {
            "user" : "carer",
            "connection" : "1234",
        }
        result = requests.post("http://127.0.0.1:9999/api/cancelConnection", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(result.text, "False")

    def testInvalidCancelSecurity(self):
        """Atempt to cancel an nonexistant outgoing connection"""
        payload = {
            "user" : "carer",
            "connection" : "1234",
        }
        result = requests.post("http://127.0.0.1:9999/api/cancelConnection", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assert_response(401)

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
