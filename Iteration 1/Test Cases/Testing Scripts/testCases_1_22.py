# ORM Testing Script
# Test Case 1_22

from peewee import *
import unittest
import imp

testDatabase = imp.load_source('testDatabase', '../../../Website/testDatabase.py')

class testCase_1_22(unittest.TestCase):

  def setUp(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

  def test_1_22_1(self):
    newUser = testDatabase.Client.insert(
      username= 'test',
      firstName='test',
      surname='test'
      dob='01/01/2001',
      isMale='TRUE',
      isCarer='TRUE',
      email='test@test.com')
    newUser.execute()
    newPassword = testDatabase.uq8LnAWi7D.insert(
      username ='test',
      password =crypt.crypt('password',bcrypt.gensalt(12))
      isCurrent = TRUE,
      expiryDate = '10/10/2014')
    newPassword.execute()
    #We need to check that the records are inserted correctly
    testDatabase.Client.select()
    testDatabase.uq8LnAWi7D.select()
    clientDelete = testDatabase.Client.delete().where(username ='test')
    #We need to check that the records are deleted from password and client table
    testDatabase.Client.select()
    testDatabase.uq8LnAWi7D.select()

  def tearDown(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

if __name__ == '__main__':
    unittest.main()
