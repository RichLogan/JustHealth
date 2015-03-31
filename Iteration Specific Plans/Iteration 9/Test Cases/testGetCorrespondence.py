import unittest
from peewee import *
import datetime
import imp
from passlib.hash import sha256_crypt
import sys
import requests
from requests.auth import HTTPBasicAuth

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

sys.path.insert(0, 'Website')
from justHealthServer import api

class testGetCorrespondence(unittest.TestCase):

    def setUp(self):
        """Create all the tables that are needed"""
        testDatabase.createAll()

        # Create a test user
        patientClient = testDatabase.Client.insert(
            username = "patient",
            email = "justhealth123@richlogan.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False,
            profilepicture = "default.png")
        testPatient = testDatabase.Patient.insert(
            username = "patient",
            firstname = "patient",
            surname = "patient",
            ismale = True)
        patientPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "patient")
        patientClient.execute()
        testPatient.execute()
        patientPassword.execute()

        # Carer1
        carerClient = testDatabase.Client.insert(
            username = "carer",
            email = "carer1@sjtate.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False,
            profilepicture = "default.png")
        carerCarer = testDatabase.Carer.insert(
            username = "carer",
            firstname = "carer",
            ismale = True,
            nhscarer = True,
            surname = "carer")
        carerPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "carer")
        carerClient.execute()
        carerCarer.execute()
        carerPassword.execute()

        # Carer Invalid
        carerDoesNotExistClient = testDatabase.Client.insert(
            username = "DoesNotExist",
            email = "carer@example.org",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False,
            profilepicture = "default.png")
        carerDoesNotExistCarer = testDatabase.Carer.insert(
            username = "DoesNotExist",
            firstname = "carer",
            ismale = True,
            nhscarer = True,
            surname = "carer")
        carerDoesNotExistPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "DoesNotExist")
        carerDoesNotExistClient.execute()
        carerDoesNotExistCarer.execute()
        carerDoesNotExistPassword.execute()

        r = testDatabase.Patientcarer.insert(
            patient = 'patient',
            carer = 'carer'
        )
        r.execute()

        rDoesNotExist = testDatabase.Patientcarer.insert(
            patient = 'patient',
            carer = 'DoesNotExist'
        )
        rDoesNotExist.execute()

        newNote = testDatabase.Notes.insert(
            carer = "carer",
            patient = "patient",
            notes = "content",
            title = "title",
            datetime = datetime.datetime.now()
        )
        newNote.execute()

    def testGetCorrespondence(self):
        """Test legitimate retrieval"""
        payload = {
            "carer" : "carer",
            "patient" : "patient"
        }
        expectedResult = '[{"patient": "patient", "carer": "carer", "title": "title", "notes": "content", "datetime": "2015-03-31", "noteid": 1}]'
        
        response = requests.post("http://127.0.0.1:9999/api/getCorrespondence", data=payload, auth=HTTPBasicAuth('carer', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(response.text, expectedResult)

    def testGetCorrespondenceInvalidUser(self):
        """User does not exist"""
        payload = {
            "carer" : "DoesNotExist",
            "patient" : "patient"
        }
        expectedResult = '[]'
        
        response = requests.post("http://127.0.0.1:9999/api/getCorrespondence", data=payload, auth=HTTPBasicAuth('DoesNotExist', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(response.text, expectedResult)

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
