from peewee import *
from passlib.hash import sha256_crypt
import requests
import unittest
import imp
import json

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testGetConnections(unittest.TestCase):
    """Testing get connections"""

    def setUp(self):
        """Create needed tables and example record"""
        testDatabase.createAll()
	    #Create a Client entry and a Patient entry

        # Carer1
        carerClient = testDatabase.Client.insert(
            username = "carer1",
            email = "carer1@richlogan.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        carerClient.execute()
        carerCarer = testDatabase.Carer.insert(
            username = "carer1",
            firstname = "carer",
            ismale = True,
            nhscarer = True,
            surname = "carer")
        carerCarer.execute()
        carerPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "carer1")
        carerPassword.execute()

        # Carer 2
        carerClient = testDatabase.Client.insert(
            username = "carer2",
            email = "carer2@richlogan.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        carerClient.execute()
        carerCarer = testDatabase.Carer.insert(
            username = "carer2",
            firstname = "carer",
            ismale = True,
            nhscarer = True,
            surname = "carer")
        carerCarer.execute()
        carerPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "carer2")
        carerPassword.execute()

        # Carer 3
        carerClient = testDatabase.Client.insert(
            username = "carer3",
            email = "carer3@richlogan.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        carerClient.execute()
        carerCarer = testDatabase.Carer.insert(
            username = "carer3",
            firstname = "carer",
            ismale = True,
            nhscarer = True,
            surname = "carer")
        carerCarer.execute()
        carerPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "carer3")
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

        # Incoming for Patient
        testIncoming = testDatabase.Relationship.insert(
            code = 1234,
            requestor = "carer1",
            requestortype = "Carer",
            target = "patient",
            targettype = "Patient")
        testIncoming.execute()

        # Outgoing for Patient
        testOutgoing = testDatabase.Relationship.insert(
            code = 1234,
            requestor = "patient",
            requestortype = "Patient",
            target = "carer2",
            targettype = "Carer")
        testOutgoing.execute()

        # Completed for Patient
        testCompleted = testDatabase.Patientcarer.insert(
            patient = "patient",
            carer = "carer3")
        testCompleted.execute()

    def testGetAllPatient(self):
        """Attempt to get all connections for patient"""
        payload = {
            "username" : "patient",
        }
        result = requests.post("http://127.0.0.1:9999/api/getConnections", data=payload, auth=('patient', 'test'))
        result = json.loads(result.text)

        expectedJSON = {
            'outgoing' : '[{"username": "carer2", "code": "1234", "surname": "carer", "accounttype": "Carer", "firstname": "carer"}]',
            'incoming' : '[{"username": "carer1", "connectionid": "1", "surname": "carer", "accounttype": "Carer", "firstname": "carer"}]',
            'completed' : '[{"username": "carer3", "surname": "carer", "accounttype": "Carer", "firstname": "carer"}]'
        }

        self.assertEqual(result, expectedJSON)

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
