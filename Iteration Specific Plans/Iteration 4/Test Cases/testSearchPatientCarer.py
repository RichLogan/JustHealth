from peewee import *
from passlib.hash import sha256_crypt
import requests
from requests.auth import HTTPBasicAuth
import unittest
import imp
import json

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testSearchPatientCarer(unittest.TestCase):
    """Testing that a Patient can search for a carer, and vice versa"""

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

    def testCorrectSearch_carer(self):
        """Attempt to search for keyword 'carer' as patient"""

        payload = {
            "username" : "patient",
            "searchterm" : "carer"
        }

        result = requests.post("http://127.0.0.1:9999/api/searchPatientCarer", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        result = json.loads(result.text)
        
        self.assertEqual(result[0]['username'], 'carer')
        self.assertEqual(result[0]['firstname'], 'carer')
        self.assertEqual(result[0]['surname'], 'carer')
        self.assertEqual(result[0]['ismale'], True)
        self.assertEqual(result[0]['nhscarer'], True)

    def testIncompleteSearch_carer(self):
        """Attempt to search for keyword 'c' as a patient"""

        payload = {
        "username" : "patient",
            "searchterm" : "c"
        }

        result = requests.post("http://127.0.0.1:9999/api/searchPatientCarer", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        result = json.loads(result.text)
        
        self.assertEqual(result[0]['username'], 'carer')
        self.assertEqual(result[0]['firstname'], 'carer')
        self.assertEqual(result[0]['surname'], 'carer')
        self.assertEqual(result[0]['ismale'], True)
        self.assertEqual(result[0]['nhscarer'], True)

    def testCaseSearch_carer(self):
        """Attempt to search for keyword: C"""

        payload = {
            "username" : "patient",
            "searchterm" : "C"
        }

        result = requests.post("http://127.0.0.1:9999/api/searchPatientCarer", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        result = json.loads(result.text)
        
        self.assertEqual(result[0]['username'], 'carer')
        self.assertEqual(result[0]['firstname'], 'carer')
        self.assertEqual(result[0]['surname'], 'carer')
        self.assertEqual(result[0]['ismale'], True)
        self.assertEqual(result[0]['nhscarer'], True)

    def testCorrectSearch_patient(self):
        """Attempt to search for keyword 'patient' as carer"""

        payload = {
            "username" : "carer",
            "searchterm" : "patient"
        }

        result = requests.post("http://127.0.0.1:9999/api/searchPatientCarer", data=payload, auth=HTTPBasicAuth('carer', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        result = json.loads(result.text)
        
        self.assertEqual(result[0]['username'], 'patient')
        self.assertEqual(result[0]['firstname'], 'patient')
        self.assertEqual(result[0]['surname'], 'patient')
        self.assertEqual(result[0]['ismale'], True)

    def testIncompleteSearch_patient(self):
        """Attempt to search for keyword 'p' as a carer"""

        payload = {
            "username" : "carer",
            "searchterm" : "p"
        }

        result = requests.post("http://127.0.0.1:9999/api/searchPatientCarer", data=payload, auth=HTTPBasicAuth('carer', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        result = json.loads(result.text)
        
        self.assertEqual(result[0]['username'], 'patient')
        self.assertEqual(result[0]['firstname'], 'patient')
        self.assertEqual(result[0]['surname'], 'patient')
        self.assertEqual(result[0]['ismale'], True)

    def testCaseSearch_patient(self):
        """Attempt to search for keyword: P"""

        payload = {
            "username" : "carer",
            "searchterm" : "P"
        }

        result = requests.post("http://127.0.0.1:9999/api/searchPatientCarer", data=payload, auth=HTTPBasicAuth('carer', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        result = json.loads(result.text)
        
        self.assertEqual(result[0]['username'], 'patient')
        self.assertEqual(result[0]['firstname'], 'patient')
        self.assertEqual(result[0]['surname'], 'patient')
        self.assertEqual(result[0]['ismale'], True)

    def testNoMatch(self):
        """Search for non-existant user"""

        payload = {
            "username" : "carer",
            "searchterm" : "rich"
        }

        result = requests.post("http://127.0.0.1:9999/api/searchPatientCarer", data=payload, auth=HTTPBasicAuth('carer', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        
        self.assertEqual(result.text, "No users found")

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
