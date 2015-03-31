from peewee import *
from passlib.hash import sha256_crypt
import requests
import unittest
import imp
import json
from requests.auth import HTTPBasicAuth
import json
from passlib.hash import sha256_crypt

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testCompleteConnection(unittest.TestCase):
    """Testing that a patient/carer can successfully connect"""

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

        securityClient = testDatabase.Client.insert(
            username = "Security",
            email = "Security@richlogan.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        securityClient.execute()

        testRelationship = testDatabase.Relationship.insert(
            code = 1234,
            requestor = "carer",
            requestortype = "Carer",
            target = "patient",
            targettype = "Patient")
        testRelationship.execute()


        #create notification type
        connectionRequestNotification = testDatabase.Notificationtype.insert(
            typename = "Connection Request",
            typeclass = "info"
            )
        connectionRequestNotification.execute()

        notificationNormal = testDatabase.Notification.insert(
            username = "patient",
            notificationtype = "Connection Request",
            dismissed = False,
            relatedObject = 1
            )
        notificationNormal.execute()

        notificationDismissed = testDatabase.Notification.insert(
            username = "patient",
            notificationtype = "Connection Request",
            dismissed = True,
            relatedObject = 2
            )
        notificationDismissed.execute()


    def testCorrectCode(self):
        """Atempt to connect giving the correct code"""
        payload = {
            "username" : "patient",
            "requestor" : "carer",
            "codeattempt" : "4321"
        }
        result = requests.post("http://127.0.0.1:9999/api/completeConnection", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(result.text, "Incorrect code")
 
    def testIncorrectCode(self):
        """Atempt to connect giving the incorrect code"""
        payload = {
            "username" : "patient",
            "requestor" : "carer",
            "codeattempt" : "4321"
        }
        result = requests.post("http://127.0.0.1:9999/api/completeConnection", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(result.text, "Incorrect code")

    
    def testRelationshipDoesntExist(self):
        """Atempt to connect giving the incorrect code"""
        payload = {
            "username" : "patient",
            "requestor" : "carer",
            "codeattempt" : "4321"
        }
        result = requests.post("http://127.0.0.1:9999/api/completeConnection", data=payload, auth=HTTPBasicAuth('patient', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
        self.assertEqual(result.text, "Incorrect code")

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
