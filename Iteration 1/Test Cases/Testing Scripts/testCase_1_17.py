# ORM Testing Script
# Test Case 1_17

from peewee import *
import unittest
import imp

testDatabase = imp.load_source('testDatabase', '../../../Website/testDatabase.py')

class testCase_1_17(unittest.TestCase):

  def setUp(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

  def test_1_17_1(self):
    newUserInsert = testDatabase.Client.insert(
      username= 'test',
      firstname='test',
      surname='test',
      dob='01/01/2001',
      ismale='TRUE',
      iscarer='TRUE',
      email='test@test.com')
    newUserInsert.execute()
    newUserDelete = testDatabase.Client.delete().where(testDatabase.Client.username == 'test')
    newUserDelete.execute()
    self.assertEqual(testDatabase.Client.select().count(),0)


  def test_1_17_2(self):
    newUserInsert = testDatabase.Client.insert (
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
    newUserInsert.execute()
    newUserDelete = testDatabase.Client.delete().where(testDatabase.Client.email == 'test@test.com')
    newUserDelete.execute()
    self.assertEqual(testDatabase.Client.select().count(),0)

  def tearDown(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

if __name__ == '__main__':
    unittest.main()
