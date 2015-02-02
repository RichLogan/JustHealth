from peewee import *
from passlib.hash import sha256_crypt
import requests
import unittest
import imp
import json

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testCompleteConnection(unittest.TestCase):
    """Testing that a patient/carer can successfully connect"""

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

    def testCorrectCode(self):
        """Atempt to connect giving the correct code"""
        payload = {
            "username" : "patient",
            "requestor" : "carer",
            "codeattempt" : "1234"
        }
        result = requests.post("http://127.0.0.1:9999/api/completeConnection", data=payload, auth=('patient', 'test'))
        self.assertEqual(result.text, "Connection to " + payload['requestor'] + " completed")
    
    def testIncorrectCode(self):
        """Atempt to connect giving the incorrect code"""
        payload = {
            "username" : "patient",
            "requestor" : "carer",
            "codeattempt" : "4321"
        }
        result = requests.post("http://127.0.0.1:9999/api/completeConnection", data=payload, auth=('patient', 'test'))
        self.assertEqual(result.text, "Incorrect code")
    
    def testRelationshipDoesntExist(self):
        """Atempt to a user who has not requested a connection"""
        payload = {
            "username" : "patient",
            "requestor" : "abcd",
            "codeattempt" : "4321"
        }
        result = requests.post("http://127.0.0.1:9999/api/completeConnection", data=payload, auth=('patient', 'test'))
        self.assertEqual(result.text, "Connection not requested")

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
