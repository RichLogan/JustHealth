# ORM Testing Script
# Test Case 1_15

from peewee import *
import unittest
import imp

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testCase_1_15(unittest.TestCase):

  def setUp(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

  def test_1_15_1(self):
    with testDatabase.database.transaction():
      with self.assertRaises(DataError):
        newUser = testDatabase.Client.insert(
          username='testtesttesttesttesttestte',
          firstname='test',
          surname='test',
          dob='01/01/2001',
          ismale='TRUE',
          iscarer='TRUE',
          email='test@test.com')
        newUser.execute()

  def test_1_15_2(self):
    with testDatabase.database.transaction():
      with self.assertRaises(DataError):
        newUser = testDatabase.Client.insert(
          username='test',
          firstname='testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttestt',
          surname='test',
          dob='01/01/2001',
          ismale='TRUE',
          iscarer='TRUE',
          email='test@test.com')
        newUser.execute()

  def test_1_15_3(self):
    with testDatabase.database.transaction():
      with self.assertRaises(DataError):
        newUser = testDatabase.Client.insert(
          username= 'test',
          firstname='test',
          surname='testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttestt',
          dob='01/01/2001',
          ismale='TRUE',
          iscarer='TRUE',
          email='test@test.com')
        newUser.execute()

  def test_1_15_4(self):
    with testDatabase.database.transaction():
      with self.assertRaises(DataError):
        newUser = testDatabase.Client.insert(
          username= 'test',
          firstname='test',
          surname='test',
          dob='01111/01/2001',
          ismale='test',
          iscarer='TRUE',
          email='test@test.com')
        newUser.execute()
    with testDatabase.database.transaction():
      with self.assertRaises(DataError):
        newUser = testDatabase.Client.insert(
          username= 'test',
          firstname='test',
          surname='test',
          dob='01/0111111/2001',
          ismale='test',
          iscarer='TRUE',
          email='test@test.com')
        newUser.execute()

  def test_1_15_5(self):
    with testDatabase.database.transaction():
      with self.assertRaises(DataError):
        newUser = testDatabase.Client.insert(
          username= 'test',
          firstname='test',
          surname='test',
          dob='01/01/2001',
          ismale='TRUE',
          iscarer='TRUE',
          email='testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest@test.com')
        newUser.execute()

  def tearDown(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

if __name__ == '__main__':
    unittest.main()
