from peewee import *
import requests
import unittest
import imp
import json

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testGetConnections(unittest.TestCase):
    """Testing get connections API"""

    def setUp(self):
        """Create needed tables and example record"""
        testDatabase.createAll()
	    #Create a Client entry, a Patient entry, a connection  and a password.
        testClient = testDatabase.Client.insert(
            username = "test",
            email = "justhealth@richlogan.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        testClient.execute()

        testPatient = testDatabase.Patient.insert(
            username = "test1",
            firstname = "test",
            surname = "test",
            ismale = True)
        testPatient.execute()

        testPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "test")
        testPassword.execute()

        testPatientCarer = testDatabase.PatientCarer.insert(
            carer = "test",
            patient = "test1")
        testPatientCarer.execute()


        def testLegitimate (self):
            """Getting Legitimate date"""

            payload = {
                "username : test"
            }

            getConnections = request.post("http://127.0.0.1:9999/api/getConnections", data=payload)
            getAccountInfo = json.loads(getConnections.text)

            self.assertEqual(getConnections['carer'], "test")
            self.assertEqual(getConnections['patient'], "test1")


        def testInvalid(self):
            """Testing invalid username"""
        payload = {
            "username" : "test"
        }

        getAccountInfo = requests.post("http://127.0.0.1:9999/api/getConnections", data=payload)
        self.assertEqual(getConnections.text, "User does not exist")



        def testNullValues(self):
            payload = {
                "username" : None
                }

        prescription = requests.post("http://127.0.0.1:9999/api/getConnections", data=payload)
        self.assertEqual(getConnections.text, "User does not exist")


        def tearDown(self):
            """Delete all tables"""
            testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
