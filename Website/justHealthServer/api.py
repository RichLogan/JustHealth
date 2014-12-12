from justHealthServer import app
from flask import Flask, render_template, request, session, redirect, url_for, abort
from flask.ext.httpauth import HTTPBasicAuth
# Line 5 !!!MUST!!! be the database import in order for /runTests.sh to work. Please do not change without also altering /runTests.sh
from database import *
from itsdangerous import URLSafeSerializer, BadSignature
from passlib.hash import sha256_crypt
import re
import datetime
import smtplib
import json
import random

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username,password):
    try:
        hashedPassword = uq8LnAWi7D.get((uq8LnAWi7D.username == username) & (uq8LnAWi7D.iscurrent==True)).password
        return sha256_crypt.verify(password, hashedPassword)
    except:
        return False

@app.route("/api/registerUser", methods=["POST"])
def registerUser():
    # Build User Registration
    try:
      profile = {}
      profile['username'] = request.form['username']
      profile['firstname'] = request.form['firstname']
      profile['surname'] = request.form['surname']
      profile['dob'] = request.form['dob']
      profile['ismale'] = request.form['ismale']
      profile['email'] = request.form['email']
      profile['password'] = request.form['password']
      profile['confirmpassword'] = request.form['confirmpassword']
      accountType = request.form['accounttype']
    except KeyError, e:
      return "All fields must be filled out"
    try:
      profile['terms'] = request.form['terms']
    except KeyError, e:
      return "Terms and Conditions must be accepted"

    # Validate all input
    for key, value in profile.iteritems():
      value = value.strip()

    # Validate username >25
    if len(profile['username']) > 25:
      return "Username can not be longer than 25 characters"

    if Client.select().where(Client.username == profile['username']).count() != 0:
       return "Username already taken"

    # Validate firstname, surname and email >25
    if len(profile['firstname']) > 100 or len(profile['surname']) > 100 or len(profile['email']) > 100:
      return 'Firstname, surname and email can not be longer than 100 characters'

    # Validate email correct format
    pattern = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
    if not re.match(pattern, profile['email']):
      return "Fail email verification"

    # Encrypt password with SHA 256
    profile['password'] = sha256_crypt.encrypt(profile['password'])

    #Check for existing username
    if Client.select().where(Client.username == profile['username']).count() != 0:
      return "Username already taken"
    if Client.select().where(Client.email == profile['email']).count() != 0:
      return "Email address already taken"

    # Build insert user query
    userInsert = Client.insert(
      username = profile['username'],
      dob = profile['dob'],
      email = profile['email'],
      accountdeactivated = False,
      accountlocked = False,
      loginattempts = 0,
      verified  = False
    )

    if accountType == "patient":
        accountType = Patient
    elif accountType == "carer":
        accountType = Carer

    typeInsert = accountType.insert(
        username = profile['username'],
        firstname = profile['firstname'],
        surname = profile['surname'],
        ismale = profile['ismale'],
    )

    # Build insert password query
    userPassword = uq8LnAWi7D.insert(
      username = profile['username'],
      password = profile['password'],
      iscurrent = 'TRUE',
      expirydate = str(datetime.date.today() + datetime.timedelta(days=90))
    )

    # Execute Queries
    with database.transaction():
        userInsert.execute()
        typeInsert.execute()
        userPassword.execute()

    sendVerificationEmail(profile['username'])
    return "True"

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    try:
        attempted = Client.get(username=request.form['username'])
    except Client.DoesNotExist:
        return "Incorrect username/password"

    # Check Password
    hashedPassword = uq8LnAWi7D.get((uq8LnAWi7D.username == attempted.username) & (uq8LnAWi7D.iscurrent==True)).password.strip()
    attemptedPassword = request.form['password']
    if sha256_crypt.verify(attemptedPassword, hashedPassword):
        if attempted.accountdeactivated == True:
            return "Account deactivated"
        elif attempted.verified == False:
            return "Account not verified. Please check your email for instructions"
        elif attempted.accountlocked == True:
            return "Account is locked. Please check your email for instructions"
        else:
            revertAttempts = Client.update(loginattempts = 0).where(Client.username == attempted.username)
            with database.transaction():
                revertAttempts.execute()
            return "Authenticated"
    else:
        currentLoginAttempts = Client.get(Client.username == attempted.username).loginattempts
        if currentLoginAttempts >= 4:
            lockAccount(attempted.username)
            incrementAttempts = Client.update(loginattempts = (currentLoginAttempts + 1)).where(Client.username == attempted.username)
            incrementAttempts.execute()
            return "Account is locked"
        incrementAttempts = Client.update(loginattempts = (currentLoginAttempts + 1)).where(Client.username == attempted.username)
        with database.transaction():
            incrementAttempts.execute()
        return "Incorrect username/password"
    return "Something went wrong!"

@app.route('/api/deactivateaccount', methods=['POST'])
def deactivateAccount():
    try:
        username = request.form['username']
    except KeyError, e:
        return "No username supplied"

    try:
        if request.form['deletecheckbox'] == "on":
            delete = True
        else:
            delete = False
    except KeyError, e:
        delete = False

    try:
        comments = request.form['comments']
    except KeyError, e:
        comments = None

    try:
        reason = request.form['reason']
    except KeyError, e:
        return "Please select a reason"

    q = Userdeactivatereason.insert(
        reason = reason,
        comments = comments
    )
    with database.transaction():
        q.execute()

    if delete:
        # Delete User
        deletedUser = Client.delete().where(Client.username == request.form['username'])
        with database.transaction():
            deletedUser.execute()
        return "Deleted"
    else:
        # Keep user
        deactivatedUser = Client.update(accountdeactivated = True).where(Client.username == username)
        unverifyUser = Client.update(verified = False).where(Client.username == username)
        with database.transaction():
            deactivatedUser.execute()
            unverifyUser.execute()
        return "Kept"

@app.route('/api/resetpassword', methods=['POST'])
def resetPassword():
    try:
        profile = {}
        profile['username'] = request.form['username']
        profile['confirmemail'] = request.form['confirmemail']
        profile['newpassword'] = request.form['newpassword']
        profile['confirmnewpassword'] = request.form['confirmnewpassword']
        profile['confirmdob'] = request.form['confirmdob']
    except KeyError, e:
        return "All fields must be filled out"

    getEmail = Client.get(username=profile['username']).email.strip()
    getDob = str(Client.get(username=profile['username']).dob)

    if getEmail==profile['confirmemail'] and getDob==profile['confirmdob']:
        #set the old password to iscurrent = false
        notCurrent = uq8LnAWi7D.update(iscurrent = False).where(str(uq8LnAWi7D.username).strip() == profile['username'])
        notVerified = Client.update(verified = False).where(str(Client.username).strip() == profile['username'])

        #encrypt the password
        profile['newpassword'] = sha256_crypt.encrypt(profile['newpassword'])

        # Build insert password query
        newCredentials = uq8LnAWi7D.insert(
          username = profile['username'],
          password = profile['newpassword'],
          iscurrent = True,
          expirydate = str(datetime.date.today() + datetime.timedelta(days=90))
        )
        unlockAccount = Client.update(accountlocked=False).where(str(Client.username).strip() == profile['username'])
        setLoginCount = Client.update(loginattempts = 0).where(str(Client.username).strip() == profile['username'])

        with database.transaction():
            notCurrent.execute()
            notVerified.execute()
            newCredentials.execute()
            unlockAccount.execute()
            setLoginCount.execute()

        sendPasswordResetEmail(profile['username'])
        return "True"
    else:
        return "Invalid details"

####
# Get account type
####

@app.route('/api/getAccountInfo', methods=['POST'])
def getAccountInfo():
    return getAccountInfo(request.form['username'])

"""Get Account information from client and patient/carer table"""
def getAccountInfo(username):
    result = {}
    thisUser = str(username)
    try:
      patient = Patient.get(username=thisUser)
      user = Patient.select().join(Client).where(Client.username==thisUser).get()
      result['accounttype'] = "Patient"
      result['firstname'] = user.firstname
      result['surname'] = user.surname
      result['username'] = user.username.username
      result['email'] = user.username.email
      result['dob'] = str(user.username.dob)
      if user.ismale:
        result['gender'] = 'Male'
      else:
        result['gender'] ='Female'

      return json.dumps(result)
    except Patient.DoesNotExist:
      result['accounttype'] = "Carer"
      carer = Carer.get(username=thisUser)
      user = Carer.select().join(Client).where(Client.username==thisUser).get()
      result['firstname'] = user.firstname
      result['surname'] = user.surname
      result['username'] = user.username.username
      result['email'] = user.username.email
      result['dob'] = str(user.username.dob)
      if user.ismale:
        result['gender'] = 'Male'
      else:
        result['gender'] ='Female'
      return json.dumps(result)
    return None

####
# Account Helper Functions
####

def lockAccount(username):
    lockAccount = Client.update(accountlocked = True).where(Client.username == username)
    with database.transaction():
        lockAccount.execute()
    sendUnlockEmail(username)

####
# Email Functions
####
def getSerializer(secret_key=None):
    if secret_key is None:
        secret_key = app.secret_key
    return URLSafeSerializer(secret_key)

def sendVerificationEmail(username):
    # Generate Verification Link
    s = getSerializer()
    payload = s.dumps(username)
    verifyLink = url_for('verifyUser', payload=payload, _external=True)
    # Login to mail server
    server = smtplib.SMTP_SSL('smtp.zoho.com', 465)
    server.login('justhealth@richlogan.co.uk', "justhealth")
    # Build message
    sender = "'JustHealth' <justhealth@richlogan.co.uk>"
    recipient = Client.get(username = username).email
    subject = "JustHealth Verification"
    message = "Thanks for registering! Please verify your account here: " + str(verifyLink)
    m = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, recipient, subject)
    # Send
    server.sendmail(sender, recipient, m+message)
    server.quit()

def getUserFromEmail(email):
    try:
      username = Client.select(Client.username).where(Client.email == email).get()
      return username.username
    except Client.DoesNotExist:
      return "False"

def sendForgotPasswordEmail(username):
    #Generate reset password Link
    s = getSerializer()
    payload = s.dumps(username)
    resetLink = url_for('loadPasswordReset', payload=payload, _external=True)
    # Login to mail server
    server = smtplib.SMTP_SSL('smtp.zoho.com', 465)
    server.login('justhealth@richlogan.co.uk', "justhealth")
    # Build message
    sender = "'JustHealth' <justhealth@richlogan.co.uk>"
    recipient = Client.get(username = username).email
    subject = "JustHealth: Forgot Password"
    message = "Please reset your JustHealth account password here: " + str(resetLink)
    m = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, recipient, subject)
    # Send
    server.sendmail(sender, recipient, m+message)
    server.quit()

def sendUnlockEmail(username):
    # Login to mail server
    s = getSerializer()
    payload = s.dumps(username)
    resetLink = url_for('loadPasswordReset', payload=payload, _external=True)
    # Login to mail server
    server = smtplib.SMTP_SSL('smtp.zoho.com', 465)
    server.login('justhealth@richlogan.co.uk', "justhealth")
    # Build message
    sender = "'JustHealth' <justhealth@richlogan.co.uk>"
    recipient = Client.get(username = username).email
    subject = "JustHealth: Account Locked"
    message = "Due to too many failed login attempts, your JustHealth account has been locked and you will be required to reset your password. Please reset your JustHealth account password here: " + str(resetLink) + ". If it was not you who locked the account please notify JustHealth immediately by replying to this email. Thank you. "
    m = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, recipient, subject)
    # Send
    server.sendmail(sender, recipient, m+message)
    server.quit()

def sendPasswordResetEmail(username):
  s = getSerializer()
  payload = s.dumps(username)
  verifyLink = url_for('passwordReset', payload=payload, _external=True)

  #Login to mail server
  server = smtplib.SMTP_SSL('smtp.zoho.com', 465)
  server.login('justhealth@richlogan.co.uk', "justhealth")
  # Build Message
  sender = "'JustHealth' <justhealth@richlogan.co.uk>"
  recipient = Client.get(username = username).email
  subject = "JustHealth Password Reset Verification"
  message = "Your password has been reset. Please verify this here: " + str(verifyLink)
  m = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, recipient, subject)
  # Send
  server.sendmail(sender, recipient, m+message)
  server.quit()


####
# Search Patient Carer
####
@app.route('/api/searchPatientCarer', methods=['POST','GET'])
def searchPatientCarer():
    """Searches database for a user that can be connected to. POST [username, searchterm]"""
    return searchPatientCarer(request.form['username'], request.form['searchterm'])

def searchPatientCarer(username, searchterm):
    #get username, firstname and surname of current user
    result = {}
    thisUser = username
    try:
        patient = Patient.get(username=thisUser)
        searchterm = "%" + searchterm + "%"
        results = Carer.select().dicts().where((Carer.username % searchterm) | (Carer.firstname % searchterm) |(Carer.surname % searchterm))

        jsonResult = []
        for result in results:
            jsonResult.append(result)
        return json.dumps(jsonResult)

    except Patient.DoesNotExist:
        searchterm = "%" + searchterm + "%"
        results = Patient.select().dicts().where((Patient.username % searchterm) | (Patient.firstname % searchterm) |(Patient.surname % searchterm))

        jsonResult = []
        for result in results:
            jsonResult.append(result)
        return json.dumps(jsonResult)
    return None

####
# Client/Client relationships
####
@app.route('/api/createConnection', methods=['POST', 'GET'])
def createConnection():
    """Creates an initial connection between two users. POST [username, target]"""
    # Get users
    currentUser = request.form['username']
    targetUser = request.form['target']

    #Handle existing entries. Need to check all == 0
    with database.transaction():
        if Relationship.select().where(Relationship.requestor == currentUser and Relationship.target == targetUser).count() != 0:
            return "Connection already established"
        if Relationship.select().where(Relationship.requestor == targetUser and Relationship.target == currentUser).count() != 0:
            return "Connection already established"
        if Patientcarer.select().where(Patientcarer.patient == currentUser and Patientcarer.carer == targetUser).count() != 0:
            return "Connection already established"
        if Patientcarer.select().where(Patientcarer.patient == targetUser and Patientcarer.carer == currentUser).count() != 0:
            return "Connection already established"

    # Get user types
    currentUser_type = json.loads(getAccountInfo(currentUser))['accounttype']
    targetUser_type = json.loads(getAccountInfo(targetUser))['accounttype']

    # Generate 4 digit code
    x = ""
    for n in range(0,4):
        x += str(random.randrange(1,9))
    x = int(x)

    # Insert into Connection table
    newConnection = Relationship.insert(
        code = x,
        requestor = currentUser,
        requestortype = currentUser_type,
        target = targetUser,
        targettype = targetUser_type
    )
    with database.transaction():
        newConnection.execute()
    return str(x)

@app.route('/api/completeConnection', methods=['POST', 'GET'])
def completeConnection():
    """Verify an inputed code to allow the completion of an attempted connection. POST[ username, requestor, codeattempt] """
    #Take attempted code, match with a entry where they are target
    target = request.form['username']
    requestor = request.form['requestor']
    attemptedCode = int(request.form['codeattempt'])

    # get record
    instance = Relationship.select().where(Relationship.requestor == requestor and Relationship.target == target).get()
    if instance.code == attemptedCode:
        # Correct attempt, establish relationship in correct table
        # TODO place into relationship table
        requestor_accountType = json.loads(getAccountInfo(requestor))['accounttype']
        target_accountType = json.loads(getAccountInfo(target))['accounttype']

        if requestor_accountType == "Patient" and target_accountType == "Carer":
            newRelationship = Patientcarer.insert(
                patient = requestor,
                carer = target
            )
            with database.transaction():
                newRelationship.execute()
        elif requestor_accountType == "Carer" and target_accountType == "Patient":
            newRelationship = Patientcarer.insert(
                patient = target,
                carer = requestor
            )
            with database.transaction():
                newRelationship.execute()

        # Delete this Relationship instance
        with database.transaction():
            instance.delete_instance()
        return "Correct"
    else:
        return "Incorrect"
    return None

@app.route('/api/deleteConnection', methods=['POST'])
def deleteConnection():
    return deleteConnection(request.form['user'], request.form['connection'])

def deleteConnection(user,connection):
    userType = json.loads(getAccountInfo(user))['accounttype']
    connectionType = json.loads(getAccountInfo(connection))['accounttype']

    if (userType == "Patient" and connectionType == "Carer"):
        instance = Patientcarer.select().where(Patientcarer.patient == user and Patientcarer.carer == connection).get()
        with database.transaction():
            instance.delete_instance()
        return "True"
    elif (userType == "Carer" and connectionType == "Patient"):
        instance = Patientcarer.select().where(Patientcarer.patient == connection and Patientcarer.carer == user).get()
        with database.transaction():
            instance.delete_instance()
        return "True"
    else:
        return "False"

@app.route('/api/cancelConnection', methods=['POST'])
def cancelRequest():
    cancelRequest(request.form['user'], request.form['connection'])

def cancelRequest(user, connection):
    try:
        instance = Relationship.select().where(Relationship.requestor == user).get()
        with database.transaction():
            instance.delete_instance()
    except RelationshipDoesNotExist:
        instance = Relationship.select().where(Relationship.target == connection).get()
        with database.transaction():
            instance.delete_instance()

@app.route('/api/getConnections', methods=['POST'])
def getConnections():
    return getConnections(request.form['username'])

def getConnections(username):
    accountType = json.loads(getAccountInfo(username))['accounttype']
    user = Client.select().where(Client.username==username).get()

    outgoingConnections = Relationship.select().where(Relationship.requestor == user)
    incomingConnections = Relationship.select().where(Relationship.target == user)

    completedConnections = {}
    if accountType == "Patient":
        completedConnections = Patientcarer.select().where(Patientcarer.patient == user)
    elif accountType == "Carer":
        completedConnections = Patientcarer.select().where(Patientcarer.carer == user)
    else:
        completedConnections = None

    #username, firstname, surname, accountype
    outgoingConnectionsDetails = []
    for connection in outgoingConnections:
        person = {}
        details = json.loads(getAccountInfo(connection.target.username))
        person['username'] = details['username']
        person['firstname'] = details['firstname']
        person['surname'] = details['surname']
        person['accounttype'] = details['accounttype']
        person['code'] = str(connection.code)
        outgoingConnectionsDetails.append(person)
    outgoingFinal = json.dumps(outgoingConnectionsDetails)

    incomingConnectionsDetails = []
    for connection in incomingConnections:
        person = {}
        details = json.loads(getAccountInfo(connection.requestor.username))
        person['username'] = details['username']
        person['firstname'] = details['firstname']
        person['surname'] = details['surname']
        person['accounttype'] = details['accounttype']
        person['connectionid'] = str(connection.connectionid)
        incomingConnectionsDetails.append(person)
    incomingFinal = json.dumps(incomingConnectionsDetails)

    completedConnectionsDetails = []
    for connection in completedConnections:
        person = {}
        if accountType == "Patient":
            details = json.loads(getAccountInfo(connection.carer.username))
        elif accountType == "Carer":
            details = json.loads(getAccountInfo(connection.patient.username))
        else:
            details = None

        person['username'] = details['username']
        person['firstname'] = details['firstname']
        person['surname'] = details['surname']
        person['accounttype'] = details['accounttype']
        completedConnectionsDetails.append(person)
    completedFinal = json.dumps(completedConnectionsDetails)

    result = {}
    result['outgoing'] = outgoingFinal
    result['incoming'] = incomingFinal
    result['completed'] = completedFinal

    return json.dumps(result)

#receives the request from android allows a patient to add an appointment
@app.route('/api/addPatientAppointment', methods=['POST'])
def addPatientAppointment():
  return addPatientAppointment(request.form)

#allows a patient to add an appointment
def addPatientAppointment(details):
# Build insert user query
  appointmentInsert = Appointments.insert(
    creator = details['creator'],
    name = details['name'],
    apptype = details['apptype'],
    addressnamenumber = details['addressnamenumber'],
    postcode = details['postcode'],
    startdate = details['startdate'],
    starttime = details['starttime'],
    enddate = details['enddate'],
    endtime = details['endtime'],
    description = details['description'],
    private = details['private']
  )
  appointmentInsert.execute()

  return "Appointment Added"

@app.route('/api/addInviteeAppointment', methods=['POST'])
def addInviteeAppointment():
  return addInviteeAppointment(request.form)

def addInviteeAppointment(details):
  #Build insert user query
  appointmentInsert = Appointments.insert(
    creator = details['creator'],
    invitee = details['username'],
    name = details['name'],
    apptype = details['apptype'],
    addressnamenumber = details['addressnamenumber'],
    postcode = details['postcode'],
    startdate = details['startdate'],
    starttime = details['starttime'],
    enddate = details['enddate'],
    endtime = details['endtime'],
    description = details['description']
    )

  appointmentInsert.execute()
  return "Appointment Added"

#receives the request from android to allow a user to view their upcoming appointments
@app.route('/api/getAllAppointments', methods=['POST'])
def getAllAppointments():
  return getAllAppointments(request.form['loggedInUser'], request.form['targetUser'])

#gets the appointments from the database
def getAllAppointments(loggedInUser, targetUser):
  #get user account type 
  currentUser_type = json.loads(getAccountInfo(loggedInUser))['accounttype']

  if currentUser_type == "Carer":
    if loggedInUser == targetUser:
       appointments = Appointments.select().where((Appointments.creator == targetUser) | (Appointments.invitee == targetUser)).order_by(Appointments.startdate.asc(), Appointments.starttime.asc())
    else:
      appointments = Appointments.select().where(((Appointments.creator == targetUser) & (Appointments.private == False)) | ((Appointments.invitee == targetUser) & (Appointments.private == False))).order_by(Appointments.startdate.asc(), Appointments.starttime.asc())
  elif currentUser_type == "Patient":
    appointments = Appointments.select().where((Appointments.creator == targetUser) | (Appointments.invitee == targetUser)).order_by(Appointments.startdate.asc(), Appointments.starttime.asc())
  
  appointments.execute()

  currentDateTime = datetime.datetime.now()

  allAppointments = []
  for app in appointments:
    appointment = {}
    appointment['appid'] = app.appid
    appointment['creator'] = app.creator.username
    appointment['name'] = app.name
    appointment['apptype'] = str(app.apptype.type)
    appointment['addressnamenumber'] = app.addressnamenumber
    appointment['postcode'] = app.postcode
    appointment['startdate'] = str(app.startdate)
    appointment['starttime'] = str(app.starttime)
    appointment['enddate'] = str(app.enddate)
    appointment['endtime'] = str(app.endtime)
    appointment['description'] = app.description
    appointment['private'] = app.private
    
    dateTime = str(app.startdate) + " " + str(app.starttime)
    dateTime = datetime.datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S")

    if (dateTime >= currentDateTime):
      appointment['upcoming'] = True
    else:
      appointment['upcoming'] = False

    allAppointments.append(appointment)

  return json.dumps(allAppointments)


#deletes an appointment
@app.route('/api/deleteAppointment', methods=['POST'])
def deleteAppointment():
  return deleteAppointment(request.form['username'], request.form['appid'])

def deleteAppointment(user, appid):
  isCreator = Appointments.select().where(Appointments.appid == appid).get()

  if isCreator.creator.username == user:
    with database.transaction():
      isCreator.delete_instance()
    return "Appointment Deleted"

#gets the appointment that is to be updated
@app.route('/api/getUpdateAppointment', methods=['POST'])
def getUpdateAppointment():
  return updateAppointment(request.form['username'], request.form['appid'])

def getUpdateAppointment(user, appid):
  isCreator = Appointments.select().where(Appointments.appid == appid).get()

  if isCreator.creator.username == user:
    jsonResult = []

    appointment = {}
    appointment['appid'] = isCreator.appid
    appointment['creator'] = isCreator.creator.username
    appointment['name'] = isCreator.name
    appointment['apptype'] = str(isCreator.apptype.type)
    appointment['addressnamenumber'] = isCreator.addressnamenumber
    appointment['postcode'] = isCreator.postcode
    appointment['startdate'] = str(isCreator.startdate)
    appointment['starttime'] = str(isCreator.starttime)
    appointment['enddate'] = str(isCreator.enddate)
    appointment['endtime'] = str(isCreator.endtime)
    appointment['description'] = isCreator.description
    appointment['private'] = isCreator.private

    jsonResult.append(appointment)
    return json.dumps(jsonResult)

#update an appointment
@app.route('/api/updateAppointment', methods=['POST'])
def updateAppointment():
  return addPatientAppointment(request.form['appid'], request.form['name'], request.form['apptype'], request.form['addressnamenumber'], request.form['postcode'], request.form['startdate'], request.form['starttime'], request.form['enddate'], request.form['endtime'], request.form['other'], request.form['private'])

def updateAppointment(appid, name, apptype, addressnamenumber, postcode, startDate, startTime, endDate, endTime, description, private):
  updateAppointment = Appointments.update(
    name = name,
    apptype = apptype,
    addressnamenumber = addressnamenumber,
    postcode = postcode,
    startdate = startDate,
    starttime = startTime,
    enddate = endDate,
    endtime = endTime,
    description = description,
    private = private).where(Appointments.appid == appid)

  with database.transaction():
    updateAppointment.execute()

  return "Appointment Updated"


@app.route('/api/addMedication', methods=['POST'])
def addMedication():
    return addMedication(request.form['medicationname'])

def addMedication(medicationName):
    insertMedication = Medication.insert(
        name = medicationName
    )
    with database.transaction():
        try:
            insertMedication.execute()
        except IntegrityError:
            return medicationName + " already exists"
    return "Added " + medicationName

@app.route('/api/deleteMedication', methods=['POST'])
def deleteMedication():
    return deleteMedication(request.form['medicationname'])

def deleteMedication(medicationName):
    try:
        instance = Medication.select().where(Medication.name == medicationName).get()
        with database.transaction():
            instance.delete_instance()
        return "Deleted " + medicationName
    except:
        return medicationName + "not found"

@app.route('/api/addPrescription', methods=['POST'])
def addPrescription():
    return addPrescription(request.form['username'],request.form['medication'],request.form['dosage'],request.form['frequency'],request.form['quantity'],request.form['dosageunit'],request.form['frequencyunit'],request.form['startdate'],request.form['enddate'],request.form['repeat'],request.form['stockleft'],request.form['prerequisite'],request.form['dosageform'])

def addPrescription(username,medication,dosage,frequency,quantity,dosageunit,frequencyunit,startdate,enddate,repeat,stockleft,prerequisite,dosageform):
    insertPrescription = Prescription.insert(
        username = username,
        medication = medication,
        dosage = dosage,
        frequency = frequency,
        quantity = quantity,
        dosageunit = dosageunit,
        frequencyunit = frequencyunit,
        startdate = startdate,
        enddate = enddate,
        repeat = repeat,
        stockleft = stockleft,
        prerequisite = prerequisite,
        dosageform = dosageform)

    try:
        with database.transaction():
            insertPrescription.execute()
            return "Prescripton added for " + username
    except:
        return "Could not add prescription"

@app.route('/api/deletePrescription', methods=['POST'])
def deletePrescription():
    return deletePrescription(request.form['prescriptionid'])

def deletePrescription(prescriptionid):
    try:
        instance = Prescription.select().where(Prescription.prescriptionid == prescriptionid).get()
        with database.transaction():
            instance.delete_instance()
            "Deleted prescription " + prescriptionid
    except:
        return prescriptionid + " not found"

@app.route('/api/getPrescriptions', methods=['POST'])
def getPrescriptions():
    return getPrescriptions(request.form['username'])

def getPrescriptions(username):
    accountType = json.loads(getAccountInfo(username))['accounttype']
    user = Client.select().where(Client.username == username).get()

    if accountType == "Patient":
        jsonResult = []
        results = Prescription.select().dicts().where(Prescription.username == user)
        for result in results:
            result['startdate'] = str(result['startdate'])
            result['enddate'] = str(result['enddate'])
            jsonResult.append(result)
        return json.dumps(jsonResult)
    else:
        return "Must have Patient account type"

@app.route('/api/getDeactivateReasons', methods=['POST'])
def getDeactivateReasons():
    """Returns a JSON list of possible reasons a user can deactivate"""
    reasons = Deactivatereason.select()
    reasonList = []
    for reason in reasons:
        reasonList.append(reason.reason)
    reasonList = json.dumps(reasonList)
    return reasonList

@app.route('/api/getAppointmentTypes', methods=['POST'])
def getAppointmentTypes():
    """Returns a JSON list of possible appointment types"""
    types = Appointmenttype.select()
    typeList = []
    for appType in types:
      typeList.append(appType.type)
    typeList = json.dumps(typeList)
    return typeList
