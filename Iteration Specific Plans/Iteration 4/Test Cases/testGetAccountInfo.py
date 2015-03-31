from peewee import *
from passlib.hash import sha256_crypt
import requests
from requests.auth import HTTPBasicAuth
import unittest
import imp
import json

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testGetAccountInfo(unittest.TestCase):
    """Testing Get Account Info API"""

    def setUp(self):
        """Create needed tables and example record"""
        testDatabase.createAll()

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
            patient = "patient"
        )
        testRelationship.execute()

    def testGetPatientSelf(self):
        """Patient accessing themselves"""

        payload = {
            "username" : "patient"
        }

        getAccountInfo = requests.post("http://127.0.0.1:9999/api/getAccountInfo", data=payload, auth=('patient', '73630002494546d52bdc16cf5874a41e720896b566cd8cb72afcf4f866d70570aa078832f3e953daaa2dca60aac7521a7b4633d12652519a2e2baee39e2b539c85ac5bdb82a9f237'))
        getAccountInfo = json.loads(getAccountInfo.text)

        self.assertEqual(getAccountInfo['username'], "patient")
        self.assertEqual(getAccountInfo['accounttype'], "Patient")
        self.assertEqual(getAccountInfo['firstname'], "patient")
        self.assertEqual(getAccountInfo['surname'], "patient")
        self.assertEqual(getAccountInfo['email'], "justhealth123@richlogan.co.uk")
        self.assertEqual(getAccountInfo['dob'], "1993-03-03")
        self.assertEqual(getAccountInfo['gender'], "Male")

    def testGetCarerSelf(self):
        """Carer accessing themselves"""

        payload = {
            "username" : "carer"
        }

        getAccountInfo = requests.post("http://127.0.0.1:9999/api/getAccountInfo", data=payload, auth=('carer', '73630002494546d52bdc16cf5874a41e720896b566cd8cb72afcf4f866d70570aa078832f3e953daaa2dca60aac7521a7b4633d12652519a2e2baee39e2b539c85ac5bdb82a9f237'))
        getAccountInfo = json.loads(getAccountInfo.text)

        self.assertEqual(getAccountInfo['username'], "carer")
        self.assertEqual(getAccountInfo['accounttype'], "Carer")
        self.assertEqual(getAccountInfo['firstname'], "carer")
        self.assertEqual(getAccountInfo['surname'], "carer")
        self.assertEqual(getAccountInfo['email'], "justhealth@richlogan.co.uk")
        self.assertEqual(getAccountInfo['dob'], "1993-03-03")
        self.assertEqual(getAccountInfo['gender'], "Male")

    def testGetPatientCarer(self):
        """Carer accessing their Patient"""

        payload = {
            "username" : "patient"
        }

        getAccountInfo = requests.post("http://127.0.0.1:9999/api/getAccountInfo", data=payload, auth=('carer', '73630002494546d52bdc16cf5874a41e720896b566cd8cb72afcf4f866d70570aa078832f3e953daaa2dca60aac7521a7b4633d12652519a2e2baee39e2b539c85ac5bdb82a9f237'))
        self.assertEqual(getAccountInfo.text, "Unauthorised")

    def testGetCarerPatient(self):
        """Patient accessing their Carer"""

        payload = {
            "username" : "carer"
        }

        getAccountInfo = requests.post("http://127.0.0.1:9999/api/getAccountInfo", data=payload, auth=('patient', '73630002494546d52bdc16cf5874a41e720896b566cd8cb72afcf4f866d70570aa078832f3e953daaa2dca60aac7521a7b4633d12652519a2e2baee39e2b539c85ac5bdb82a9f237'))
        self.assertEqual(getAccountInfo.text, "Unauthorised")

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
