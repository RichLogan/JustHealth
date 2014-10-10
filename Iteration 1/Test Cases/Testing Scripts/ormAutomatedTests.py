# ORM Testing

def test_1_14_1():
  newUser = Client.insert (username= 'test',
                          firstName='test',
                          surname='test',
                          dob='01/01/2001',
                          isMale='TRUE',
                          isCarer='TRUE',
                          email='test@test.com')
  newUser.execute()
  Client.select()

def test_1_15_1():
  newUser = Client.insert (username='testtesttesttesttesttestte',
                          firstName='test',
                          surname='test',
                          dob='01/01/2001',
                          isMale='TRUE',
                          isCarer='TRUE',
                          email='test@test.com')
  newUser.execute()
  Client.select()

def test_1_15_2():
    newUser = Client.insert (username='test'
                            firstName='testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttestt',
                            surname='test',
                            dob='01/01/2001',
                            isMale='TRUE',
                            isCarer='TRUE',
                            email='test@test.com')
    newUser.execute()
    Client.select()

def test_1_15_3():
  newUser = Client.insert (username= 'test',
                          firstName='test',
                          surname='testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttestt'',
                          dob='01/01/2001',
                          isMale='TRUE',
                          isCarer='TRUE',
                          email='test@test.com')
  newUser.execute()
  Client.select()

def test_1_15_3():
  newUser = Client.insert (username= 'test',
                          firstName='test',
                          surname='test',
                          dob='test',
                          isMale='TRUE',
                          isCarer='TRUE',
                          email='test@test.com')
  newUser.execute()
  Client.select()

def test_1_15_4():
  newUser = Client.insert (username= 'test',
                          firstName='test',
                          surname='test',
                          dob='01/01/2001',
                          isMale='test',
                          isCarer='TRUE',
                          email='test@test.com')
  newUser.execute()
  Client.select()

def test_1_15_5():
  newUser = Client.insert (username= 'test',
                          firstName='test',
                          surname='test',
                          dob='01/01/2001',
                          isMale='TRUE',
                          isCarer='test',
                          email='test@test.com')
  newUser.execute()
  Client.select()

def test_1_15_5():
  newUser = Client.insert (username= 'test',
                          firstName='test',
                          surname='test',
                          dob='01/01/2001',
                          isMale='TRUE',
                          isCarer='TRUE',
                          email='testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest@test.com')
  newUser.execute()
  Client.select()

def test_1_16_1():
  newUser = Client.insert (username= '',
                          firstName='test',
                          surname='test',
                          dob='01/01/2001',
                          isMale='TRUE',
                          isCarer='TRUE',
                          email='test@test.com')
  newUser.execute()
  Client.select()

def test_1_16_2():
  newUser = Client.insert (username= 'test',
                          firstName='',
                          surname='test',
                          dob='01/01/2001',
                          isMale='TRUE',
                          isCarer='TRUE',
                          email='test@test.com')
  newUser.execute()
  Client.select()

def test_1_16_3():
  newUser = Client.insert (username= 'test',
                          firstName='test',
                          surname='',
                          dob='01/01/2001',
                          isMale='TRUE',
                          isCarer='TRUE',
                          email='test@test.com')
  newUser.execute()
  Client.select()

def test_1_16_4():
  newUser = Client.insert (username= 'test',
                          firstName='test',
                          surname='test',
                          dob='',
                          isMale='TRUE',
                          isCarer='TRUE',
                          email='test@test.com')
  newUser.execute()
  Client.select()

def test_1_16_5():
  newUser = Client.insert (username= 'test',
                          firstName='test',
                          surname='test',
                          dob='01/01/2001',
                          isMale='',
                          isCarer='TRUE',
                          email='test@test.com')
  newUser.execute()
  Client.select()

def test_1_16_6():
  newUser = Client.insert (username= 'test',
                          firstName='test',
                          surname='test',
                          dob='01/01/2001',
                          isMale='TRUE',
                          isCarer='',
                          email='test@test.com')
  newUser.execute()
  Client.select()

def test_1_16_7():
  newUser = Client.insert (username= 'test',
                          firstName='test',
                          surname='',
                          dob='01/01/2001',
                          isMale='TRUE',
                          isCarer='TRUE',
                          email='')
  newUser.execute()
  Client.select()

def test_1_17_1():
  newUser = Client.delete ()
  newUser.execute()
  newUserInsert = Client.insert (username= 'test',
                                firstName='test',
                                surname='test',
                                dob='01/01/2001',
                                isMale='TRUE',
                                isCarer='TRUE',
                                email='test@test.com')
  newUserInsert.execute()
  newUserDelete = Client.delete().where(Client.username == 'test')
  newUserDelete.execute()

def test_1_17_2():
  newUser = Client.delete ()
  newUser.execute()
  newUserInsert = Client.insert (username= 'test',
                                firstName='test',
                                surname='test',
                                dob='01/01/2001',
                                isMale='TRUE',
                                isCarer='TRUE',
                                email='test@test.com')
  newUserInsert.execute()
  newUserDelete = Client.delete().where(Client.email == 'test@test.com')
  newUserDelete.execute()

def test_1_18_1():
  newUser = Client.delete ()
  newUser.execute()
  newUserInsert = Client.insert (username= 'test',
                              firstName='test',
                              surname='test',
                              dob='01/01/2001',
                              isMale='TRUE',
                              isCarer='TRUE',
                              email='test@test.com')
  newUserInsert.execute()
  newUserUpdate = Client.update(username='testingUpdate').where(Client.username == 'test')
  newUserUpdate.execute()

def test_1_18_2():
  newUser = Client.delete ()
  newUser.execute()
  newUserInsert = Client.insert (username= 'test',
                              firstName='test',
                              surname='test',
                              dob='01/01/2001',
                              isMale='TRUE',
                              isCarer='TRUE',
                              email='test@test.com')
  newUserInsert.execute()
  newUserUpdate = Client.update(firstname='testingFirstname').where(Client.username == 'test')
  newUserUpdate.execute()

def test_1_18_3():
  newUser = Client.delete ()
  newUser.execute()
  newUserInsert = Client.insert (username= 'test',
                              firstName='test',
                              surname='test',
                              dob='01/01/2001',
                              isMale='TRUE',
                              isCarer='TRUE',
                              email='test@test.com')
  newUserInsert.execute()
  newUserUpdate = Client.update(surename='testingSurename').where(Client.username == 'test')
  newUserUpdate.execute()

def test_1_18_4():
  newUser = Client.delete ()
  newUser.execute()
  newUserInsert = Client.insert (username= 'test',
                              firstName='test',
                              surname='test',
                              dob='01/01/2001',
                              isMale='TRUE',
                              isCarer='TRUE',
                              email='test@test.com')
  newUserInsert.execute()
  newUserUpdate = Client.update(dob='03/03/1993').where(Client.username == 'test')
  newUserUpdate.execute()

def test_1_18_5():
  newUser = Client.delete ()
  newUser.execute()
  newUserInsert = Client.insert (username= 'test',
                              firstName='test',
                              surname='test',
                              dob='01/01/2001',
                              isMale='TRUE',
                              isCarer='TRUE',
                              email='test@test.com')
  newUserInsert.execute()
  newUserUpdate = Client.update(isMale='False').where(Client.username == 'test')
  newUserUpdate.execute()

def test_1_18_6():
  newUser = Client.delete ()
  newUser.execute()
  newUserInsert = Client.insert (username= 'test',
                              firstName='test',
                              surname='test',
                              dob='01/01/2001',
                              isMale='TRUE',
                              isCarer='TRUE',
                              email='test@test.com')
  newUserInsert.execute()
  newUserUpdate = Client.update(isCarer='False').where(Client.username == 'test')
  newUserUpdate.execute()

def test_1_18_7():
  newUser = Client.delete ()
  newUser.execute()
  newUserInsert = Client.insert (username= 'test',
                              firstName='test',
                              surname='test',
                              dob='01/01/2001',
                              isMale='TRUE',
                              isCarer='TRUE',
                              email='test@test.com')
  newUserInsert.execute()
  newUserUpdate = Client.update(email='testingUpdate@testingUpdate.com').where(Client.username == 'test')
  newUserUpdate.execute()

def test_1_18_8():
  newUser = Client.delete ()
  newUser.execute()
  newUserInsert = Client.insert (username= 'test',
                              firstName='test',
                              surname='test',
                              dob='01/01/2001',
                              isMale='TRUE',
                              isCarer='TRUE',
                              email='test@test.com')
  newUserInsert.execute()
  newUserUpdate = Client.update(verified='TRUE').where(Client.username == 'test')
  newUserUpdate.execute()

def test_1_18_9():
  newUser = Client.delete()
  newUser.execute()
  newUserInsert = Client.insert (username= 'test',
                              firstName='test',
                              surname='test',
                              dob='01/01/2001',
                              isMale='TRUE',
                              isCarer='TRUE',
                              email='test@test.com')
  newUserInsert.execute()
  newUserUpdate = Client.update(accountLocked='TRUE').where(Client.username == 'test')
  newUserUpdate.execute()

#Rich 100% to check 1_19_1

def test_1_19_1():
  newUser = Client.insert (username= 'test',
                          firstName='test',
                          surname='test',
                          dob='01/01/2001',
                          isMale='TRUE',
                          isCarer='TRUE',
                          email='test@test.com')
  newUser.execute()
  newPassword = uq8LnAWi7D.insert(username ='test',
                                  password =crypt.crypt('password',bcrypt.gensalt(12))
                                  isCurrent = TRUE,
                                  expiryDate = '10/10/2014')
  newPassword.execute()

def test_1_20_1():
  newPassword = uq8LnAWi7D.delete()
  newPassword.execute()
  newPassword2 = uq8LnAWi7D.insert(
                                  username ='notintable',
                                  password =crypt.crypt('password',bcrypt.gensalt(12))
                                  isCurrent = TRUE,
                                  expiryDate = '10/10/2014')
  newPassword2.execute()

def test_1_20_2():
  newPassword = uq8LnAWi7D.insert(username ='test',
                                password =crypt.crypt('passwordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpasswordpassword',bcrypt.gensalt(12))
                                isCurrent = TRUE,
                                expiryDate = '10/10/2014')
  newPassword.execute()

def test_1_20_3():
  newPassword = uq8LnAWi7D.insert(username ='test',
                                  password =crypt.crypt('password',bcrypt.gensalt(12))
                                  isCurrent = 'test',
                                  expiryDate = '10/10/2014')
  newPassword.execute()

def test_1_20_4():
  newPassword = uq8LnAWi7D.insert(username ='test',
                                  password =crypt.crypt('password',bcrypt.gensalt(12))
                                  isCurrent = TRUE,
                                  expiryDate = '19/17/1993')
  newPassword.execute()

def test_1_21_1():
  newPassword = uq8LnAWi7D.insert(username ='test',
                                  password =crypt.crypt('password',bcrypt.gensalt(12))
                                  isCurrent = TRUE,
                                  expiryDate = '10/10/2014')
  newPassword.execute()
  newPasswordDelete.delete().where(username='test')
  newPasswordDelete.execute()

def test_1_22_1():
  newPasswordDelete = uq8LnAWi7D.delete()
  newUserDelete = Client.delete()
  newPasswordDelete.execute()
  newUserDelete.execute()
  newUser = Client.insert(username= 'test',
                          firstName='test',
                          surname='test',
                          dob='01/01/2001',
                          isMale='TRUE',
                          isCarer='TRUE',
                          email='test@test.com')
  newUser.execute()
  newPassword = uq8LnAWi7D.insert(username ='test',
                                  password =crypt.crypt('password',bcrypt.gensalt(12))
                                  isCurrent = TRUE,
                                  expiryDate = '10/10/2014')
  newPassword.execute()
  #We need to check that the records are inserted correctly
  Client.select()
  uq8LnAWi7D.select()
  clientDelete = Client.delete().where(username ='test')
  #We need to check that the records are deleted from password and client table
  Client.select()
  uq8LnAWi7D.select()
