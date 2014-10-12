# ORM Testing Script
# Test Case 1_14

from peewee import *
import unittest
import imp

database = imp.load_source('database', '../../../Website/database.py')

class testCase_1_14(unittest.TestCase):

  def setUp(self):
    deleteUsers = database.Client.delete()
    deletePasswords = database.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

  def test_1_14_1(self):
    with database.db.transaction():
      newUser = database.Client.insert(
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUser.execute()

  def tearDown(self):
    deleteUsers = database.Client.delete()
    deletePasswords = database.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

if __name__ == '__main__':
    unittest.main()
