# ORM Testing Script
# Test Case 1_14

from peewee import *
import unittest
import imp

testDatabase = imp.load_source('testDatabase', 'Website/justHealthServer/testDatabase.py')

class testCase_1_14(unittest.TestCase):

  def setUp(self):
    testDatabase.createAll()

  def test_1_14_1(self):
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

  def tearDown(self):
    testDatabase.dropAll()

if __name__ == '__main__':
    unittest.main()
