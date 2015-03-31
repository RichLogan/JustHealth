import unittest
import imp
import requests
from requests.auth import HTTPBasicAuth
import json
from passlib.hash import sha256_crypt

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')


class testGetNotifications(unittest.TestCase):

    def setUp(self):
        """Create all the tables that are needed"""
        testDatabase.createAll()

        #create a test user
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

        #create a test user that has no notifications
        DoesNotExistClient = testDatabase.Client.insert(
            username = "DoesNotExist",
            email = "justhealth123@richlogan.co.uk",
            dob = "03/03/1993",
            verified = True,
            accountlocked = False,
            loginattempts = 0,
            accountdeactivated = False)
        DoesNotExistClient.execute()

        DoesNotExistPatient = testDatabase.Patient.insert(
            username = "DoesNotExist",
            firstname = "patient",
            surname = "patient",
            ismale = True)
        DoesNotExistPatient.execute()

        DoesNotExistPassword = testDatabase.uq8LnAWi7D.insert(
            expirydate = '01/01/2020',
            iscurrent = True,
            password = sha256_crypt.encrypt('test'),
            username = "DoesNotExist")
        DoesNotExistPassword.execute()


                # Carer1
        carerClient = testDatabase.Client.insert(
            username = "carer1",
            email = "carer1@sjtate.co.uk",
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
            email = "carer2@sjtate.co.uk",
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

        # First Incoming for Patient
        testIncoming = testDatabase.Relationship.insert(
            code = 1234,
            requestor = "carer1",
            requestortype = "Carer",
            target = "patient",
            targettype = "Patient")
        testIncoming.execute()

        # Second Incoming for Patient
        testIncomingTwo = testDatabase.Relationship.insert(
            code = 1234,
            requestor = "carer2",
            requestortype = "Carer",
            target = "patient",
            targettype = "Patient")
        testIncomingTwo.execute()

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

    def testGetAll(self):
        """Attempt to get all of the notifications for a user"""
        payload = { 
            "username" : "patient"
        }

        expectedResult = '[{"username": "patient", "notificationtype": "Connection Request", "relatedObjectTable": null, "relatedObject": 2, "content": "You have a new connection request from carer2", "link": "/?go=connections", "dismissed": true, "notificationid": 2, "type": "info"}, {"username": "patient", "notificationtype": "Connection Request", "relatedObjectTable": null, "relatedObject": 1, "content": "You have a new connection request from carer1", "link": "/?go=connections", "dismissed": false, "notificationid": 1, "type": "info"}]'

        getNotification = requests.post("http://127.0.0.1:9999/api/getAllNotifications", data=payload, auth=HTTPBasicAuth('patient', '7363000274128bb03e7418d95d4dd26eeb00a86e7b4f06ad70f186f6948945a687c9f855cca6cafd8e72b2602aa48255ed2e2aabb7d6eafd5751761369049a8b3d34ffb4305b3b76'))
        # getNotification = json.loads(getNotification.text)
        self.assertEqual(getNotification.text, expectedResult)


    def testGetDismissed(self):
        """Attempt to get all of the Dismissed notifications for a user || where dismissed==True"""
        payload = { 
            "username" : "patient"
        }   

        expectedResult = '[{"username": "patient", "notificationtype": "Connection Request", "relatedObjectTable": null, "relatedObject": 2, "content": "You have a new connection request from carer2", "link": "/?go=connections", "dismissed": true, "notificationid": 2, "type": "info"}]'

        getNotification = requests.post("http://127.0.0.1:9999/api/getDismissedNotifications", data=payload, auth=HTTPBasicAuth('patient', '7363000274128bb03e7418d95d4dd26eeb00a86e7b4f06ad70f186f6948945a687c9f855cca6cafd8e72b2602aa48255ed2e2aabb7d6eafd5751761369049a8b3d34ffb4305b3b76'))
        self.assertEqual(getNotification.text, expectedResult)


    def testGetNotDismissed(self):
        """Attempt to get all of the undismissed notifications for a user || where dismissed==False"""
        payload = { 
            "username" : "patient"
        }

        expectedResult = '[{"username": "patient", "notificationtype": "Connection Request", "relatedObjectTable": null, "relatedObject": 1, "content": "You have a new connection request from carer1", "link": "/?go=connections", "dismissed": false, "notificationid": 1, "type": "info"}]'

        getNotification = requests.post("http://127.0.0.1:9999/api/getNotifications", data=payload, auth=HTTPBasicAuth('patient', '7363000274128bb03e7418d95d4dd26eeb00a86e7b4f06ad70f186f6948945a687c9f855cca6cafd8e72b2602aa48255ed2e2aabb7d6eafd5751761369049a8b3d34ffb4305b3b76'))
        self.assertEqual(getNotification.text, expectedResult)


    def testGetAllInvalidUser(self): 
        """Attempt to get notifications for an invalid user"""
        payload = { 
            "username" : "DoesNotExist"
        }

        getNotification = requests.post("http://127.0.0.1:9999/api/getAllNotifications", data=payload, auth=HTTPBasicAuth('DoesNotExist', '7363000274128bb03e7418d95d4dd26eeb00a86e7b4f06ad70f186f6948945a687c9f855cca6cafd8e72b2602aa48255ed2e2aabb7d6eafd5751761369049a8b3d34ffb4305b3b76'))
        self.assertEqual(getNotification.text, '[]')


    def testGetDismissedInvalidUser(self): 
        """Attempt to get notifications for an invalid user where dismissed==True"""
        payload = { 
            "username" : "DoesNotExist"
        }

        getNotification = requests.post("http://127.0.0.1:9999/api/getDismissedNotifications", data=payload, auth=HTTPBasicAuth('DoesNotExist', '7363000274128bb03e7418d95d4dd26eeb00a86e7b4f06ad70f186f6948945a687c9f855cca6cafd8e72b2602aa48255ed2e2aabb7d6eafd5751761369049a8b3d34ffb4305b3b76'))
        self.assertEqual(getNotification.text, '[]')


    def testGetNotDismissedInvalidUser(self): 
        """Attempt to get notifications for an invalid user where dismissed==False"""
        payload = { 
            "username" : "DoesNotExist"
        }

        getNotification = requests.post("http://127.0.0.1:9999/api/getNotifications", data=payload, auth=HTTPBasicAuth('DoesNotExist', '7363000274128bb03e7418d95d4dd26eeb00a86e7b4f06ad70f186f6948945a687c9f855cca6cafd8e72b2602aa48255ed2e2aabb7d6eafd5751761369049a8b3d34ffb4305b3b76'))
        self.assertEqual(getNotification.text, '[]')

    def tearDown(self):
        """Delete all tables"""
        testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
