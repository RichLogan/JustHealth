# ORM Testing Script
# Test Case 1_20

from peewee import *
import unittest
import imp

testDatabase = imp.load_source('testDatabase', '../../../Website/testDatabase.py')

class testCase_1_20(unittest.TestCase):

  def setUp(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

  def test_1_20_1(self):
    with testDatabase.database.transaction():
      newPassword2 = testDatabase.uq8LnAWi7D.insert(
        username ='notintable',
        password =crypt.crypt('password',bcrypt.gensalt(12))
        isCurrent = TRUE,
        expiryDate = '10/10/2014')
        newPassword2.execute()

  def test_1_20_2(self):
    with testDatabase.database.transaction():
      newPassword = testDatabase.uq8LnAWi7D.insert(
      username ='test',
      password =crypt.crypt('passwordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpassword',bcrypt.gensalt(12))
      isCurrent = TRUE,
      expiryDate = '10/10/2014')
    newPassword.execute()

  def test_1_20_3(self):
    with testDatabase.database.transaction()
      newPassword = testDatabase.uq8LnAWi7D.insert(
        username ='test',
        password =crypt.crypt('password',bcrypt.gensalt(12))
        isCurrent = 'test',
        expiryDate = '10/10/2014')
      newPassword.execute()

  def test_1_20_4(self):
    with testDatabase.database.transaction()
      newPassword = testDatabase.uq8LnAWi7D.insert(
        username ='test',
        password =crypt.crypt('password',bcrypt.gensalt(12))
        isCurrent = TRUE,
        expiryDate = '19/17/1993')
      newPassword.execute()

  def tearDown(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

if __name__ == '__main__':
    unittest.main()
