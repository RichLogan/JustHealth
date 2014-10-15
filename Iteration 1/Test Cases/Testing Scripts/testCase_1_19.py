# ORM Testing Script
# Test Case 1_19

from peewee import *
import unittest
import imp

testDatabase = imp.load_source('testDatabase', '../../../Website/testDatabase.py')

class testCase_1_19(unittest.TestCase):

  def setUp(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

  def test_1_19_1(self):
    with testDatabase.database.transaction():
      newUser = testDatabase.Client.insert (
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUser.execute()
      newPassword = testDatabase.uq8LnAWi7D.insert(
        username ='test',
        password ='password',
        iscurrent = 'TRUE',
        expirydate = '10/10/2014')
      newPassword.execute()
      self.assertEqual(testDatabase.Client.select().count(),1)

  def tearDown(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

if __name__ == '__main__':
    unittest.main()
