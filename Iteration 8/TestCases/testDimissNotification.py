import unittest

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testDismissNotification(unittest.TestCase):

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

	def testDismissLegitimate(self):
		"""Attempt to dismiss a notification || check that API returns expected response and DB field is set correctly"""
		payload = { 
			"notificationid" : "1"
			}

		dismiss = requests.post("http://127.0.0.1:9999/api/dismissNotification", data=payload)
		self.assertEqual(dismiss.text, "True")
		self.assertEqual(testDatabase.Notifications.select(testDatabase.Notifications.dismissed).where(testDatabase.Notifications.notificationid == 1), False)

	def testDismissInvalidId(self):
		"""Attempt to dismiss a notification with an invalid notification ID || check that API returns expected response and DB not updated"""
		payload = {
			"notificationid" : "2"
		}

		dismiss = requests.post("http://127.0.0.1:9999/api/dismissNotification", data=payload)
		self.assertEqual(dismiss.text, "Invalid Notification Id")


  def tearDown(self):
    """Delete all tables"""
    testDatabase.dropAll()

if __name__ == '__main__':
  unittest.main()

