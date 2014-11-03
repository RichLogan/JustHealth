# ORM Testing Script
# Test Case 1_18

from peewee import *
import unittest
import imp

testDatabase = imp.load_source('testDatabase', '../../../Website/justHealthServer/testdatabase.py')

class testCase_1_18(unittest.TestCase):

  def setUp(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

  def test_1_18_1(self):
    with testDatabase.database.transaction():
      newUserInsert = testDatabase.Client.insert (
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUserInsert.execute()
      newUserUpdate = testDatabase.Client.update(username='testingUpdate').where(testDatabase.Client.username == 'test')
      newUserUpdate.execute()
      self.assertEqual(testDatabase.Client.select().count(),1)

  def test_1_18_2(self):
    with testDatabase.database.transaction():
      newUserInsert = testDatabase.Client.insert (
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUserInsert.execute()
      newUserUpdate = testDatabase.Client.update(firstname='testingFirstname').where(testDatabase.Client.username == 'test')
      newUserUpdate.execute()
      self.assertEqual(testDatabase.Client.select().count(),1)

  def test_1_18_3(self):
    with testDatabase.database.transaction():
      newUserInsert = testDatabase.Client.insert (
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUserInsert.execute()
      newUserUpdate = testDatabase.Client.update(surname='testingSurname').where(testDatabase.Client.username == 'test')
      newUserUpdate.execute()
      self.assertEqual(testDatabase.Client.select().count(),1)

  def test_1_18_4(self):
    with testDatabase.database.transaction():
      newUserInsert = testDatabase.Client.insert (
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUserInsert.execute()
      newUserUpdate = testDatabase.Client.update(dob='03/03/1993').where(testDatabase.Client.username == 'test')
      newUserUpdate.execute()
      self.assertEqual(testDatabase.Client.select().count(),1)

  def test_1_18_5(self):
    with testDatabase.database.transaction():
      newUserInsert = testDatabase.Client.insert (
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUserInsert.execute()
      newUserUpdate = testDatabase.Client.update(ismale='False').where(testDatabase.Client.username == 'test')
      newUserUpdate.execute()
      self.assertEqual(testDatabase.Client.select().count(),1)

  def test_1_18_6(self):
    with testDatabase.database.transaction():
      newUserInsert = testDatabase.Client.insert (
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUserInsert.execute()
      newUserUpdate = testDatabase.Client.update(iscarer='False').where(testDatabase.Client.username == 'test')
      newUserUpdate.execute()
      self.assertEqual(testDatabase.Client.select().count(),1)

  def test_1_18_7(self):
    with testDatabase.database.transaction():
      newUserInsert = testDatabase.Client.insert (
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUserInsert.execute()
      newUserUpdate = testDatabase.Client.update(email='testingUpdate@testingUpdate.com').where(testDatabase.Client.username == 'test')
      newUserUpdate.execute()
      self.assertEqual(testDatabase.Client.select().count(),1)

  def test_1_18_8(self):
    with testDatabase.database.transaction():
      newUserInsert = testDatabase.Client.insert (
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUserInsert.execute()
      newUserUpdate = testDatabase.Client.update(verified='TRUE').where(testDatabase.Client.username == 'test')
      newUserUpdate.execute()
      self.assertEqual(testDatabase.Client.select().count(),1)

  def test_1_18_9(self):
    with testDatabase.database.transaction():
      newUserInsert = testDatabase.Client.insert (
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUserInsert.execute()
      newUserUpdate = testDatabase.Client.update(accountlocked='TRUE').where(testDatabase.Client.username == 'test')
      newUserUpdate.execute()
      self.assertEqual(testDatabase.Client.select().count(),1)

  def tearDown(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

if __name__ == '__main__':
  unittest.main()
