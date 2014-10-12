# ORM Testing Script
# Test Case 1_16

from peewee import *
import unittest
import imp

database = imp.load_source('database', '../../../Website/database.py')

class testCase_1_16(unittest.TestCase):

  def setUp(self):
    deleteUsers = database.Client.delete()
    deletePasswords = database.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

  def test_1_16_1(self):
    with database.db.transaction():
      newUser = database.Client.insert(
        username= '',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUser.execute()

  def test_1_16_2(self):
    with database.db.transaction():
      newUser = database.Client.insert(
        username= 'test',
        firstname='',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUser.execute()

  def test_1_16_3(self):
    with database.db.transaction():
      newUser = database.Client.insert(
        username= 'test',
        firstname='test',
        surname='',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUser.execute()

  def test_1_16_4(self):
    with database.db.transaction():
      newUser = database.Client.insert(
        username= 'test',
        firstname='test',
        surname='test',
        dob='',
        ismale='TRUE',
        iscarer='TRUE',
        email='test@test.com')
      newUser.execute()

  def test_1_16_5(self):
    with database.db.transaction():
      newUser = database.Client.insert(
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='',
        iscarer='TRUE',
        email='test@test.com')
      newUser.execute()

  def test_1_16_6(self):
    with database.db.transaction():
      newUser = database.Client.insert(
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='',
        email='test@test.com')
      newUser.execute()

  def test_1_16_7(self):
    with database.db.transaction():
      newUser = database.Client.insert(
        username= 'test',
        firstname='test',
        surname='test',
        dob='01/01/2001',
        ismale='TRUE',
        iscarer='TRUE',
        email='')
      newUser.execute()

  def tearDown(self):
    deleteUsers = database.Client.delete()
    deletePasswords = database.uq8LnAWi7D.delete()
    deleteUsers.execute()
    deletePasswords.execute()

if __name__ == '__main__':
    unittest.main()
