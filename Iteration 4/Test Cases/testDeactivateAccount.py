from peewee import *
from passlib.hash import sha256_crypt
import requests
import unittest
import imp

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

        deactivate = requests.post("http://127.0.0.1:9999/api/deactivateaccount", data=payload)
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

        deactivate = requests.post("http://127.0.0.1:9999/api/deactivateaccount", data=payload)
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

        deactivate = requests.post("http://127.0.0.1:9999/api/deactivateaccount", data=payload)
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

        deactivate = requests.post("http://127.0.0.1:9999/api/deactivateaccount", data=payload)
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
        deactivate = requests.post("http://127.0.0.1:9999/api/deactivateaccount", data=payload)
        self.assertEqual(deactivate.text, "No username supplied")

        # Comments
        payload = {
            "username" : "test",
            "comments" : None,
            "reason" : "A reason to deactivate"
        }
        deactivate = requests.post("http://127.0.0.1:9999/api/deactivateaccount", data=payload)

        # Comments
        payload = {
            "username" : "test",
            "comments" : "test",
            "reason" : None
        }
        deactivate = requests.post("http://127.0.0.1:9999/api/deactivateaccount", data=payload)
        self.assertEqual(deactivate.text, "Please select a reason")

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
