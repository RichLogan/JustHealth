# ORM Testing Script
# Test Case 1_16

from peewee import *
import unittest
import imp

testDatabase = imp.load_source('testDatabase', '../../../Website/testDatabase.py')

class testCase_1_16(unittest.TestCase):

  def setUp(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

  def test_1_16_1(self):
    with testDatabase.database.transaction():
      newUser = testDatabase.Client.insert(
        username= '',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUser.execute()

  def test_1_16_2(self):
    with testDatabase.database.transaction():
      newUser = testDatabase.Client.insert(
        username= 'test',
        firstname='',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUser.execute()

  def test_1_16_3(self):
    with testDatabase.database.transaction():
      newUser = testDatabase.Client.insert(
        username= 'test',
        firstname='test',
        surname='',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUser.execute()

  def test_1_16_4(self):
    with testDatabase.database.transaction():
      newUser = testDatabase.Client.insert(
        username= 'test',
        firstname='test',
        surname='test',
        dob='',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUser.execute()

  def test_1_16_5(self):
    with testDatabase.database.transaction():
      newUser = testDatabase.Client.insert(
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='',
        iscarer='TRUE',
        email='test@test.com')
      newUser.execute()

  def test_1_16_6(self):
    with testDatabase.database.transaction():
      newUser = testDatabase.Client.insert(
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='',
        email='test@test.com')
      newUser.execute()

  def test_1_16_7(self):
    with testDatabase.database.transaction():
      newUser = testDatabase.Client.insert(
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='')
      newUser.execute()

  def tearDown(self):
    deleteUsers = testDatabase.Client.delete()
    deletePasswords = testDatabase.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

if __name__ == '__main__':
    unittest.main()
