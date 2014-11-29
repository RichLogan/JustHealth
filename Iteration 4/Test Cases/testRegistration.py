from peewee import *
import requests
import unittest
import imp

testDatabase = imp.load_source('testDatabase', '../../Website/justHealthServer/testDatabase.py')

class testRegistration(unittest.TestCase):
    """Testing Registration API"""

    def setUp(self):
        """Create needed tables"""
        testDatabase.createAll()

    def testLegitimate(self):
        """Inserting legitimate data"""

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
            "terms":"on"
        }

        registration = requests.post("http://127.0.0.1:9999/api/registerUser", data=payload)
        self.assertEqual(registration.text, "True")
        self.assertEqual(testDatabase.Client.select().where(testDatabase.Client.username == "testUsername").count(), 1)

    def testNulls(self):
        """Inserting NULL values"""
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
            "terms":"on"
        }

        for key in payload:
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
                "terms":"on"
            }
            payload[key] = None
            registration = requests.post("http://127.0.0.1:9999/api/registerUser", data=payload)
            if key != "terms":
                self.assertEqual(registration.text, "All fields must be filled out")
            else:
                self.assertEqual(registration.text, "Terms and Conditions must be accepted")
        self.assertEqual(testDatabase.Client.select().count(), 0)

    def testLongData(self):
        """Inserting data too long"""

        # Legitimate
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
            "terms":"on"
        }

        # Username
        payload['username'] = "aaaaaaaaaaaaaaaaaaaaaaaaaa"
        registration = requests.post("http://127.0.0.1:9999/api/registerUser", data=payload)
        self.assertEqual(registration.text, "Username can not be longer than 25 characters")
        self.assertEqual(testDatabase.Client.select().count(), 0)
        payload['username'] = "testUsername"

        # First Name
        payload['firstname'] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", #101 characters, 100 limit.
        registration = requests.post("http://127.0.0.1:9999/api/registerUser", data=payload)
        self.assertEqual(registration.text, "Firstname, surname and email can not be longer than 100 characters")
        self.assertEqual(testDatabase.Client.select().count(), 0)
        payload['firstname'] = "testFirstname"

        # Surname
        payload['surname'] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", #101 characters, 100 limit.
        registration = requests.post("http://127.0.0.1:9999/api/registerUser", data=payload)
        self.assertEqual(registration.text, "Firstname, surname and email can not be longer than 100 characters")
        self.assertEqual(testDatabase.Client.select().count(), 0)
        payload['surname'] = "testSurname"

        # # Email (Commented out so we don't keep blocking Zoho!)
        # payload['email'] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@richlogan.co.uk", #101 characters, 100 limit.
        # registration = requests.post("http://127.0.0.1:9999/api/registerUser", data=payload)
        # self.assertEqual(registration.text, "Firstname, surname and email can not be longer than 100 characters")
        # self.assertEqual(testDatabase.Client.select().count(), 0)
        # payload['email'] = "justhealth@richlogan.co.uk"


    def testDataTypes(self):
        """Inserting incorrect data types"""

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
            "terms":"on"
        }

        # Date of birth
        payload['dob'] = "aaa" #Should be date format
        registration = requests.post("http://127.0.0.1:9999/api/registerUser", data=payload)
        self.assertEqual(registration.text, "Incorrect data type")
        self.assertEqual(testDatabase.Client.select().count(), 0)
        payload['dob'] = "01/01/1991"

        # isMale
        payload['isMale'] = "aaa" #Should be boolean
        registration = requests.post("http://127.0.0.1:9999/api/registerUser", data=payload)
        self.assertEqual(registration.text, "Incorrect data type")
        self.assertEqual(testDatabase.Client.select().count(), 0)
        payload['isMale'] = "true"

        # terms
        payload['terms'] = "aaa" #Should be 'on'
        registration = requests.post("http://127.0.0.1:9999/api/registerUser", data=payload)
        self.assertEqual(registration.text, "Incorrect data type")
        self.assertEqual(testDatabase.Client.select().count(), 0)
        payload['terms'] = "on"

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
