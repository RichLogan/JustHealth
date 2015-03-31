from peewee import *
from passlib.hash import sha256_crypt
import requests
import unittest
import imp
from requests.auth import HTTPBasicAuth
import json
from passlib.hash import sha256_crypt

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testAuthentication(unittest.TestCase):
    """Testing Authentication API"""

    def setUp(self):
        """Create needed tables"""
        testDatabase.createAll()
        #Create a Client entry, a Patient entry, and a password.
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
            username = "test",
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

    def testLegitimate(self):
        """Legitimate Authentication Attempt"""

        payload = {
            "username" : "test",
            "password" : "test"
        }

        login = requests.post("http://127.0.0.1:9999/api/authenticate", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(login.text, "Authenticated")

    def testIncorrectPassword(self):
        """Incorrect Password Attempt"""

        payload = {
            "username" : "test",
            "password" : "1234"
        }

        login = requests.post("http://127.0.0.1:9999/api/authenticate", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(login.text, "Incorrect username/password")

    def testIncorrectUsername(self):
        """Incorrect Username Attempt"""

        payload = {
            "username" : "1234",
            "password" : "test"
        }

        login = requests.post("http://127.0.0.1:9999/api/authenticate", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(login.text, "Incorrect username/password")

    def testNullUsername(self):
        """Null username attempt"""

        payload = {
            "username" : None,
            "password" : "test"
        }

        login = requests.post("http://127.0.0.1:9999/api/authenticate", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(login.text, "Your request appears to be malformed")

    def testNullPassword(self):
        """Null password attempt"""

        payload = {
            "username" : "test",
            "password" : None
        }

        login = requests.post("http://127.0.0.1:9999/api/authenticate", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(login.text, "Your request appears to be malformed")

    def testDeactivated(self):
        """Account Deactivated"""

        setAccountDeactivated = testDatabase.Client.update(accountdeactivated=True).where(testDatabase.Client.username == "test")
        setAccountDeactivated.execute()

        payload = {
            "username" : "test",
            "password" : "test"
        }

        login = requests.post("http://127.0.0.1:9999/api/authenticate", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(login.text, "Account deactivated")

    def testLocked(self):
        """Account Locked"""

        setAccountLocked = testDatabase.Client.update(accountlocked=True).where(testDatabase.Client.username == "test")
        setAccountLocked.execute()

        payload = {
            "username" : "test",
            "password" : "test"
        }

        login = requests.post("http://127.0.0.1:9999/api/authenticate", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(login.text, "Account is locked. Please check your email for instructions")

    def testVerified(self):
        """Account not verified"""

        setAccountUnverified = testDatabase.Client.update(verified=False).where(testDatabase.Client.username == "test")
        setAccountUnverified.execute()

        payload = {
            "username" : "test",
            "password" : "test"
        }

        login = requests.post("http://127.0.0.1:9999/api/authenticate", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(login.text, "Account not verified. Please check your email for instructions")

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
