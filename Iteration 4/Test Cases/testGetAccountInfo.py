from peewee import *
import requests
import unittest
import imp
import json

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testGetAccountInfo(unittest.TestCase):
    """Testing Get Account Info API"""

    def setUp(self):
        """Create needed tables and example record"""
        testDatabase.createAll()

        # Example
        payload = {
            "username" : "testUsername",
            "firstname" : "testFirstname",
            "surname" : "testSurname",
            "dob" : "03/03/1993",
            "ismale" : "true",
            "email" : "justhealth@richlogan.co.uk",
            "password" : "test",
            "confirmpassword" : "test",
            "accounttype" : "patient",
            "terms" : "on"
        }
        registration = requests.post("http://127.0.0.1:9999/api/registerUser", data=payload)

    def testLegitimate(self):
        """Getting legitimate data"""

        payload = {
            "username" : "testUsername"
        }

        getAccountInfo = requests.post("http://127.0.0.1:9999/api/getAccountInfo", data=payload)
        getAccountInfo = json.loads(getAccountInfo.text)

        self.assertEqual(getAccountInfo['accounttype'], "Patient")
        self.assertEqual(getAccountInfo['accounttype'], "Patient")
        self.assertEqual(getAccountInfo['firstname'], "testFirstname")
        self.assertEqual(getAccountInfo['surname'], "testSurname")
        self.assertEqual(getAccountInfo['username'], "testUsername")
        self.assertEqual(getAccountInfo['email'], "justhealth@richlogan.co.uk")
        self.assertEqual(getAccountInfo['dob'], "1993-03-03")
        self.assertEqual(getAccountInfo['gender'], "Male")

    def testInvalid(self):
        """Testing invalid username"""
        payload = {
            "username" : "test"
        }

        getAccountInfo = requests.post("http://127.0.0.1:9999/api/getAccountInfo", data=payload)
        self.assertEqual(getAccountInfo.text, "User does not exist")


    # Not sure if this is actually needed. Obv causes a 400 but don't know if thats actually a fail? We'll just make a pretty bad request page?
    def testNull(self):
        """Testing null username"""
        payload = {
            "username" : None
        }

        getAccountInfo = requests.post("http://127.0.0.1:9999/api/getAccountInfo", data=payload)
        self.assertEqual(getAccountInfo.text, "User does not exist")

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
