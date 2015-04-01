# ORM Testing Script
# Test Case 1_16

from peewee import *
import unittest
import imp

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testCase_1_16(unittest.TestCase):

  def setUp(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

  def test_1_16_1(self):
    with testDatabase.database.transaction():
      with self.assertRaises(IntegrityError):
        newUser = testDatabase.Client.insert(
          username = None,
          firstname= 'test',
          surname = 'test',
          dob = '01/01/2001',
          ismale = 'TRUE',
          iscarer = 'TRUE',
          email = 'test@test.com')
        newUser.execute()

  def test_1_16_2(self):
    with testDatabase.database.transaction():
      with self.assertRaises(IntegrityError):
        newUser = testDatabase.Client.insert(
          username = 'test',
          firstname = None,
          surname ='test',
          dob = '01/01/2001',
          ismale = 'TRUE',
          iscarer = 'TRUE',
          email = 'test@test.com')
        newUser.execute()

  def test_1_16_3(self):
    with testDatabase.database.transaction():
      with self.assertRaises(IntegrityError):
        newUser = testDatabase.Client.insert(
          username = 'test',
          firstname = 'test',
          surname = None,
          dob = '01/01/2001',
          ismale = 'TRUE',
          iscarer = 'TRUE',
          email = 'test@test.com')
        newUser.execute()

  def test_1_16_4(self):
    with testDatabase.database.transaction():
      with self.assertRaises(IntegrityError):
        newUser = testDatabase.Client.insert(
          username = 'test',
          firstname = 'test',
          surname = 'test',
          dob = None,
          ismale = 'TRUE',
          iscarer = 'TRUE',
          email = 'test@test.com')
        newUser.execute()

  def test_1_16_5(self):
    with testDatabase.database.transaction():
      with self.assertRaises(IntegrityError):
        newUser = testDatabase.Client.insert(
          username = 'test',
          firstname = 'test',
          surname = 'test',
          dob = '01/01/2001',
          ismale = None,
          iscarer = 'TRUE',
          email = 'test@test.com')
        newUser.execute()

  def test_1_16_6(self):
    with testDatabase.database.transaction():
      with self.assertRaises(IntegrityError):
        newUser = testDatabase.Client.insert(
          username= 'test',
          firstname = 'test',
          surname = 'test',
          dob = '01/01/2001',
          ismale = 'TRUE',
          iscarer = None,
          email = 'test@test.com')
        newUser.execute()

  def test_1_16_7(self):
    with testDatabase.database.transaction():
      with self.assertRaises(IntegrityError):
        newUser = testDatabase.Client.insert(
          username = 'test',
          firstname = 'test',
          surname = 'test',
          dob = '01/01/2001',
          ismale = 'TRUE',
          iscarer = None,
          email = '')
        newUser.execute()

  def tearDown(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

if __name__ == '__main__':
    unittest.main()
