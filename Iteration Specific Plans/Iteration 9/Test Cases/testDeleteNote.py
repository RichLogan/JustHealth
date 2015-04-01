import unittest
from peewee import *
import datetime
import imp
from passlib.hash import sha256_crypt
import sys
import requests
from requests.auth import HTTPBasicAuth

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

sys.path.insert(0, 'Website')
from justHealthServer import api

class testDeleteNote(unittest.TestCase):

    def setUp(self):
      """Create all the tables that are needed"""
      testDatabase.createAll()

      # Create a test user
      patientClient = testDatabase.Client.insert(
        username = "patient",
        email = "justhealth123@richlogan.co.uk",
        dob = "03/03/1993",
        verified = True,
        accountlocked = False,
        loginattempts = 0,
        accountdeactivated = False,
        profilepicture = "default.png")
      testPatient = testDatabase.Patient.insert(
        username = "patient",
        firstname = "patient",
        surname = "patient",
        ismale = True)
      patientPassword = testDatabase.uq8LnAWi7D.insert(
          expirydate = '01/01/2020',
          iscurrent = True,
          password = sha256_crypt.encrypt('test'),
          username = "patient")
      patientClient.execute()
      testPatient.execute()
      patientPassword.execute()

      # Carer1
      carerClient = testDatabase.Client.insert(
          username = "carer",
          email = "carer1@sjtate.co.uk",
          dob = "03/03/1993",
          verified = True,
          accountlocked = False,
          loginattempts = 0,
          accountdeactivated = False,
          profilepicture = "default.png")
      carerCarer = testDatabase.Carer.insert(
          username = "carer",
          firstname = "carer",
          ismale = True,
          nhscarer = True,
          surname = "carer")
      carerPassword = testDatabase.uq8LnAWi7D.insert(
          expirydate = '01/01/2020',
          iscurrent = True,
          password = sha256_crypt.encrypt('test'),
          username = "carer")
      carerClient.execute()
      carerCarer.execute()
      carerPassword.execute()

      # Create an invalid patient
      patientDoesNotExistClient = testDatabase.Client.insert(
        username = "DoesNotExist",
        email = "justhealth123@richlogan.co.uk",
        dob = "03/03/1993",
        verified = True,
        accountlocked = False,
        loginattempts = 0,
        accountdeactivated = False,
        profilepicture = "default.png")
      testDoesNotExistPatient = testDatabase.Patient.insert(
        username = "DoesNotExist",
        firstname = "patient",
        surname = "patient",
        ismale = True)
      patientDoesNotExistPassword = testDatabase.uq8LnAWi7D.insert(
        expirydate = '01/01/2020',
        iscurrent = True,
        password = sha256_crypt.encrypt('test'),
        username = "DoesNotExist")
      patientDoesNotExistClient.execute()
      testDoesNotExistPatient.execute()
      patientDoesNotExistPassword.execute()

      r = testDatabase.Patientcarer.insert(
        patient = 'patient',
        carer = 'carer'
      )
      r.execute()

      rDoesNotExist = testDatabase.Patientcarer.insert(
        patient = 'patient',
        carer = 'DoesNotExist'
      )
      rDoesNotExist.execute()

      newNote = testDatabase.Notes.insert(
        noteid = 1,
        carer = "carer",
        patient = "patient",
        notes = "content",
        title = "title",
        datetime = datetime.datetime.now()
      )
      newNote.execute()

    def testDeleteLegitimate(self):
      """Test legitimate note adding"""
      payload = {
        "noteid" : 1
      }
        
      response = requests.post("http://127.0.0.1:9999/api/deleteNote", data=payload, auth=HTTPBasicAuth('carer', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
      self.assertEqual(response.text, 'Deleted')
      self.assertEqual(testDatabase.Notes.select().count(), 0)

    def testDeleteNotExistant(self):
      """Test legitimate note adding"""
      payload = {
        "noteid" : 100
      }
        
      response = requests.post("http://127.0.0.1:9999/api/deleteNote", data=payload, auth=HTTPBasicAuth('carer', '7363000287e45c448721f2b3bd6b0811e82725fc18030fe18fe8d97aa698e9c554e14099ccdc8f972df79c3d2209c2330924d6d677328fb99bf9fc1cb325667d9a5c6a3447201210'))
      self.assertEqual(response.text, 'Failed')
      self.assertEqual(testDatabase.Notes.select().count(), 1)


    def tearDown(self):
      """Delete all tables"""
      testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
