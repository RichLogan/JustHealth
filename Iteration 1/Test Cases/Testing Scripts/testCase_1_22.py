# ORM Testing Script
# Test Case 1_22

from peewee import *
import unittest
import imp

testDatabase = imp.load_source('testDatabase', '../../../Website/justHealthServer/testdatabase.py')

class testCase_1_22(unittest.TestCase):

  def setUp(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

  def test_1_22_1(self):
    with testDatabase.database.transaction():
      newUser = testDatabase.Client.insert(
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
      #We need to check that the records are inserted correctly
      self.assertEqual(testDatabase.Client.select().count(),1)
      self.assertEqual(testDatabase.uq8LnAWi7D.select().count(),1)
      clientDelete = testDatabase.Client.delete().where(testDatabase.Client.username =='test')
      clientDelete.execute()
      self.assertEqual(testDatabase.Client.select().count(),0)
      self.assertEqual(testDatabase.uq8LnAWi7D.select().count(),0)

  def tearDown(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

if __name__ == '__main__':
    unittest.main()
