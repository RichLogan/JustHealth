from peewee import *
from passlib.hash import sha256_crypt
import requests
import unittest
import imp
from requests.auth import HTTPBasicAuth
import unittest
import imp
import json

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testDeactivateAccount(unittest.TestCase):
    """Testing Deactivate Account API"""

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

        testPatient = testDatabase.Patient.insert(
            username = "test",
            firstname = "test",
            surname = "test",
            ismale = True)

        testPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "test")

        testReason = testDatabase.Deactivatereason.insert(
            reason = "A reason to deactivate"
        )

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

        testClient.execute()
        testPatient.execute()
        testPassword.execute()
        testReason.execute()

    def testLegitimateDeactivate(self):
        """Legitimate Deactivate Attempt"""

        payload = {
            "username" : "test",
            "comments" : "testComment",
            "reason" : "A reason to deactivate"
        }

        deactivate = requests.post("http://127.0.0.1:9999/api/deactivateaccount", data=payload,  auth=HTTPBasicAuth('test', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(deactivate.text, "Kept")
        self.assertEqual(testDatabase.Client.select().where(testDatabase.Client.username == "test").count(), 1)
        self.assertEqual(testDatabase.Userdeactivatereason.select().count(), 1)

    def testLegitimateDeactivate_noComments(self):
        """Legitimate Deactivate Attempt with no comments"""

        payload = {
            "username" : "test",
            "comments" : None,
            "reason" : "A reason to deactivate"
        }

        deactivate = requests.post("http://127.0.0.1:9999/api/deactivateaccount", data=payload,  auth=HTTPBasicAuth('test', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(deactivate.text, "Kept")
        self.assertEqual(testDatabase.Client.select().where(testDatabase.Client.username == "test").count(), 1)
        self.assertEqual(testDatabase.Userdeactivatereason.select().count(), 1)

    def testLegitimateDelete(self):
        """Legitimate Delete Attempt"""

        payload = {
            "username" : "test",
            "comments" : "testComment",
            "deletecheckbox" : "on",
            "reason" : "A reason to deactivate"
        }

        deactivate = requests.post("http://127.0.0.1:9999/api/deactivateaccount", data=payload,  auth=HTTPBasicAuth('test', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(deactivate.text, "Deleted")
        self.assertEqual(testDatabase.Client.select().where(testDatabase.Client.username == "test").count(), 0)
        self.assertEqual(testDatabase.Userdeactivatereason.select().count(), 1)

    def testLegitimateDelete_noComments(self):
        """Legitimate Delete Attempt with no comments"""

        payload = {
            "username" : "test",
            "comments" : None,
            "deletecheckbox" : "on",
            "reason" : "A reason to deactivate"
        }

        deactivate = requests.post("http://127.0.0.1:9999/api/deactivateaccount", data=payload,  auth=HTTPBasicAuth('test', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(deactivate.text, "Deleted")
        self.assertEqual(testDatabase.Client.select().where(testDatabase.Client.username == "test").count(), 0)
        self.assertEqual(testDatabase.Userdeactivatereason.select().count(), 1)

    def testNulls(self):
        """Testing Nulls for Deactivate"""

        # Username
        payload = {
            "username" : None,
            "comments" : "testComment",
            "reason" : "A reason to deactivate"
        }
        deactivate = requests.post("http://127.0.0.1:9999/api/deactivateaccount", data=payload, auth=HTTPBasicAuth('test', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(deactivate.text, "Your request appears to be malformed")

        # Comments
        payload = {
            "username" : "test",
            "comments" : None,
            "reason" : "Your request appears to be malformed"
        }
        deactivate = requests.post("http://127.0.0.1:9999/api/deactivateaccount", data=payload, auth=HTTPBasicAuth('test', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))

        # Comments
        payload = {
            "username" : "test",
            "comments" : "test",
            "reason" : None
        }
        deactivate = requests.post("http://127.0.0.1:9999/api/deactivateaccount", data=payload, auth=HTTPBasicAuth('test', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(deactivate.text, "Please select a reason")

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
