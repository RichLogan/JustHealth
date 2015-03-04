import unittest

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

        #create notification type
        connectionRequestNotification = testDatabase.Notificationtype.insert(
        	typename = "Connection Request",
        	typeclass = "info"
        	)
       	connectionRequestNotification.execute()

       	notification = testDatabase.Notifications.insert(
       		username = "patient"
       		notificationtype = "Connection Request"
       		relatedobject = 1	
       		)
       	notification.execute()
	
	def testGetAll(self):
		"""Attempt to get all of the notifications for a user"""
		payload = { 
			"username" : "patient"
		}

		expectedResult = {
			'[{"username": "patient", "notificationtype": "Connection Request", "relatedObjectTable": "Relationship", "relatedObject": 1, "content": "You have a new connection request from femaleAttempt", "link": "/profile?go=connections", "dismissed": false, "notificationid": 1, "type": "info"}]'
		}

		getNotification = request.post("http://127.0.0.1:9999/api/getNotifications", data=payload)
		getNotification = json.loads(getNotification.text)
		self.assertEqual(getNotification, expectedResult)


	def testGetDismissed(self):
		"""Attempt to get all of the Dismissed notifications for a user || where dismissed==True"""
		return False


	def testGetNotDismissed(self):
		"""Attempt to get all of the undismissed notifications for a user || where dismissed==False"""
		return False


	def testGetAllInvalidUser(self): 
		"""Attempt to get notifications for an invalid user"""
		payload = { 
			"username" : "DoesNotExist"
		}

		getNotification = request.post("http://127.0.0.1:9999/api/getNotifications", data=payload)
		self.assertEqual(getNotification.text, "Invalid Username")


	def testGetDismissedInvalidUser(self): 
		"""Attempt to get notifications for an invalid user where dismissed==True"""
		return False


	def testGetNotDismissedInvalidUser(self): 
		"""Attempt to get notifications for an invalid user where dismissed==False"""
		return False