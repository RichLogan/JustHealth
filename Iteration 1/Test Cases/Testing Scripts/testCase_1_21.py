# ORM Testing Script
# Test Case 1_21

from peewee import *
import unittest
import imp

testDatabase = imp.load_source('testDatabase', '../../../Website/testDatabase.py')

class testCase_1_21(unittest.TestCase):

  def setUp(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()


  def test_1_21_1(self):
    newPassword = testDatabase.uq8LnAWi7D.insert(
      username ='test',
      password =crypt.crypt('password',bcrypt.gensalt(12))
      isCurrent = TRUE,
      expiryDate = '10/10/2014')
    newPassword.execute()
    newPasswordDelete = testDatabase.uq8LnAWi7D.delete().where(testDatabase.uq8LnAWi7D.username == 'test')
    newPasswordDelete.execute()
    self.assertEqual(testDatabase.Client.select().count(),0)


  def tearDown(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

if __name__ == '__main__':
    unittest.main()
