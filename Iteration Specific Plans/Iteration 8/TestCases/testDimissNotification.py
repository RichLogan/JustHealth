from peewee import *
from passlib.hash import sha256_crypt
import unittest
import imp
import requests
from requests.auth import HTTPBasicAuth

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
      typeclass = "info")
    connectionRequestNotification.execute()

    notification = testDatabase.Notification.insert(
      username = "patient",
      notificationtype = "Connection Request",
      relatedObject = 1,
      relatedObjectTable = "A Table")
    notification.execute()

  def testDismissLegitimate(self):
    """Attempt to dismiss a notification || check that API returns expected response and DB field is set correctly"""
    payload = { 
      "notificationid" : 1
    }
    passwordEncrypted = '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'

    dismiss = requests.post("http://127.0.0.1:9999/api/dismissNotification", data=payload, auth=HTTPBasicAuth('patient', passwordEncrypted))
    self.assertEqual(dismiss.text, "True")
    self.assertEqual(testDatabase.Notification.select(testDatabase.Notification.dismissed).where(testDatabase.Notification.notificationid == 1), False)

  def testDismissInvalidId(self):
    """Attempt to dismiss a notification with an invalid notification ID || check that API returns expected response and DB not updated"""
    payload = {
      "notificationid" : 2
    }

    passwordEncrypted = '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'

    dismiss = requests.post("http://127.0.0.1:9999/api/dismissNotification", data=payload, auth=HTTPBasicAuth('patient', passwordEncrypted))
    self.assertEqual(dismiss.text, "Notification Does Not Exist")

  def tearDown(self):
    """Delete all tables"""
    testDatabase.dropAll()

if __name__ == '__main__':
  unittest.main()

