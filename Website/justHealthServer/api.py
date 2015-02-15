from justHealthServer import app
from flask import Flask, render_template, request, session, redirect, url_for, abort
from flask.ext.httpauth import HTTPBasicAuth
# Line 5 !!!MUST!!! be the database import in order for /runTests.sh to work. Please do not change without also altering /runTests.sh
from database import *
from itsdangerous import URLSafeSerializer, BadSignature
from passlib.hash import sha256_crypt
from werkzeug import secure_filename
#used to encrypt and decrypt the password in the method encryptPassword() and decryptPassword()
from simplecrypt import encrypt, decrypt
import binascii
import re
import os
import sys
import datetime
from datetime import date
import time
import smtplib
import json
import random


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username,password):
    """Checks if the password entered is the current password for that account"""
    plaintextPassword = decryptPassword(password)
    try:
        hashedPassword = uq8LnAWi7D.get((uq8LnAWi7D.username == username) & (uq8LnAWi7D.iscurrent==True)).password
        return sha256_crypt.verify(plaintextPassword, hashedPassword)
    except:
        return False

@app.route("/api/encryptPassword", methods=["POST"])
def encryptPassword():
    """Encrypts the users password and returns it to them"""
    #used so that we are able to store the encrypted users password in android SharedPreferences
    plaintext = request.form['password']
    cipherText = encrypt(app.secret_key, plaintext)
    stringCipher = binascii.hexlify(cipherText)
    return stringCipher


def decryptPassword(cipherText):
    """Decrypts the users password and returns it so that we are able to authenticate them"""
    #used so that we are able to store the encrypted users password in android SharedPreferences
    bytesCipher = binascii.unhexlify(cipherText)
    plaintext = decrypt(app.secret_key, bytesCipher)
    return plaintext


@app.route("/api/registerUser", methods=["POST"])
def registerUser():
    """Builds the user profile using the information input in the form"""
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
      return "Email failed validation"

    # Encrypt password with SHA 256
    profile['password'] = sha256_crypt.encrypt(profile['password'])

    isMale = False
    if profile['ismale'] == "true":
        isMale = True

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
        ismale = isMale,
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

@app.route('/api/usernameCheck', methods=['POST'])
def usernameCheck():
    """Returns True if a username has already been taken"""
    return str(Client.select().where(Client.username == request.form['username']).count() != 0)

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    """Authenticates a username and password and returns the result of the authentication check"""
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
                #Password expiry methods need to be added here
            status = passwordExpiration(attempted.username)
            return status
    else:
        currentLoginAttempts = Client.get(Client.username == attempted.username).loginattempts
        if currentLoginAttempts >= 4:
            lockAccount(attempted.username)
            incrementAttempts = Client.update(loginattempts = (currentLoginAttempts + 1)).where(Client.username == attempted.username)
            incrementAttempts.execute()
            return "Account is locked. Please check your email for instructions"
        incrementAttempts = Client.update(loginattempts = (currentLoginAttempts + 1)).where(Client.username == attempted.username)
        with database.transaction():
            incrementAttempts.execute()
        return "Incorrect username/password"

@app.route('/api/deactivateaccount', methods=['POST'])
@auth.login_required
def deactivateAccount():
    return deactivateAccount(request.form)

def deactivateAccount(details):
    """Form validation for account deactivation"""
    try:
        username = details['username']
    except KeyError, e:
        return "No username supplied"

    try:
        if details['deletecheckbox'] == "on":
            delete = True
        else:
            delete = False
    except KeyError, e:
        delete = False

    try:
        comments = details['comments']
    except KeyError, e:
        comments = None

    try:
        reason = details['reason']
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
        deletedUser = Client.get(Client.username == request.form['username'])
        with database.transaction():
            deletedUser.delete_instance(recursive=True)
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
    """Form validation and database checks for user when they forget a password (overrides the old password)"""
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
        notCurrent = uq8LnAWi7D.update(iscurrent = False).where(uq8LnAWi7D.username == profile['username'])
        notVerified = Client.update(verified = False).where(Client.username == profile['username'])

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
# Account Information
####

@app.route('/api/getAccountInfo', methods=['POST'])
@auth.login_required
def getAccountInfo():
    return getAccountInfo(request.form['username'])

def getAccountInfo(username):
    """Get Account information from client and patient/carer table"""
    result = {}
    try:
      user = Patient.select().join(Client).where(Client.username==str(username)).get()
      result['accounttype'] = "Patient"
    except Patient.DoesNotExist:
        user = Carer.select().join(Client).where(Client.username==str(username)).get()
        result['accounttype'] = "Carer"

    result['firstname'] = user.firstname
    result['surname'] = user.surname
    result['username'] = user.username.username
    result['email'] = user.username.email
    result['dob'] = str(user.username.dob)
    result['profilepicture'] = user.username.profilepicture
    if user.ismale:
        result['gender'] = 'Male'
    else:
        result['gender'] ='Female'
    return json.dumps(result)

@app.route('/api/setProfilePicture', methods=['POST'])
def setProfilePicture():
    return setProfilePicture(request.files)

def setProfilePicture(details):
    dest = "/static/images/profilePictures"
    allowedExtension = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'svg'])

    file = details['image']

    if file and ('.' in file.filename and file.filename.rsplit('.', 1)[1] in allowedExtension):
        filename = secure_filename(file.filename)
        file.save(os.path.join(dest, filename))
        return filename
    return False

@app.route('/api/editProfile', methods=['POST'])
@auth.login_required
def editProfile():
    return editProfile(request.form, request.files)

def editProfile(profile, picture):
    user = None
    # What type of user are we dealing with?
    try:
        user = Patient.select().join(Client).where(Client.username==profile['username']).get()
    except Patient.DoesNotExist:
        user = Carer.select().join(Client).where(Client.username==profile['username']).get()

    # Access to their corresponding Client entry
    clientObject = Client.select().where(Client.username == user.username).get()

    gender = False
    if profile['ismale'] == "true":
        gender = True

    # Update
    user.firstname = profile['firstname']
    user.surname = profile['surname']
    user.ismale = gender
    clientObject.dob = profile['dob']
    clientObject.email = profile['email']

    # Profile Picture Upload
    allowedExtension = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'svg'])
    file = picture['image']
    filename = file.filename
    fileExtension = filename.rsplit('.', 1)[1]
    if file and ('.' in filename and fileExtension in allowedExtension):
        filename = secure_filename(getSerializer().dumps(filename)) + "." + fileExtension
        file.save(os.path.join(app.config['PROFILE_PICTURE'], filename))
        clientObject.profilepicture = filename

    # Execute Updated
    with database.transaction():
        user.save()
        clientObject.save()
        return "Edit Successful"
    return "Failed"

@app.route('/api/changePassword', methods=['POST'])
@auth.login_required
def changePasswordAPI():
    return changePasswordAPI(request.form)

def changePasswordAPI(details):
    """Allows a user to change their password. POST [username, oldpassword, newpassword]"""
    try:
        currentPassword = uq8LnAWi7D.get((uq8LnAWi7D.username == details['username']) & (uq8LnAWi7D.iscurrent==True))
        # If old password is correct
        if sha256_crypt.verify(details['oldpassword'], currentPassword.password):
            # Invalidate Old Password
            currentPassword.iscurrent = False
        
            # Insert New Password
            newPassword = uq8LnAWi7D.insert(
                username = details['username'],
                password = sha256_crypt.encrypt(details['newpassword']),
                iscurrent = 'TRUE',
                expirydate = str(datetime.date.today() + datetime.timedelta(days=90))
            )

            # Execute
            with database.transaction():
                currentPassword.save()
                newPassword.execute()
                return "Password changed"
        else: return "Incorrect password"
    except: return "User does not exist"

####
# Account Helper Functions
####

def lockAccount(username):
    """Emails the user if their account gets locked"""
    lockAccount = Client.update(accountlocked = True).where(Client.username == username)
    with database.transaction():
        lockAccount.execute()
    sendUnlockEmail(username)

####
# Email Functions
####
def getSerializer(secret_key=None):
    """Converts a username into a random key, in order to create a unique link"""
    if secret_key is None:
        secret_key = app.secret_key
    return URLSafeSerializer(secret_key)

def sendVerificationEmail(username):
    """Sends email to the user after registration asking for account verification"""
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
    """Get username from the database for a valid email address"""
    try:
      username = Client.select(Client.username).where(Client.email == email).get()
      return username.username
    except Client.DoesNotExist:
      return "False"

def sendForgotPasswordEmail(username):
    """Sends email to the user on completion of reset password form"""
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
    """Sends email to a user when account is locked due to too many unsuccessful attempts"""
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
    """Sends user email confirming password reset"""
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

def sendContactUs(details):
    """Sends email to justhealth when a user has a question"""
    #Login to mail server
    server = smtplib.SMTP_SSL('smtp.zoho.com', 465)
    server.login('justhealth@richlogan.co.uk', "justhealth")
    # Build Message
    sender = "'JustHealth User Question' <justhealth@richlogan.co.uk>"
    cc = Client.get(username = details['username']).email
    recipient = 'justhealth@richlogan.co.uk'
    subject = "JustHealth User Question"
    message = details['message']
    m = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, recipient, subject)
    # Send
    server.sendmail(sender, recipient, m+message)
    server.quit()

####
# Search Patient Carer
####
@app.route('/api/searchPatientCarer', methods=['POST','GET'])
@auth.login_required
def searchPatientCarer():
    """Searches database for a user that can be connected to. POST [username, searchterm]"""
    return searchPatientCarer(request.form['username'], request.form['searchterm'])

def searchPatientCarer(username, searchterm):
    #get username, firstname and surname of current user
    results = {}
    searchterm = "%" + searchterm + "%"
    try:
        patient = Patient.get(username=username)
        results = Carer.select().dicts().where((Carer.username % searchterm) | (Carer.firstname % searchterm) |(Carer.surname % searchterm))
    except Patient.DoesNotExist:
        results = Patient.select().dicts().where((Patient.username % searchterm) | (Patient.firstname % searchterm) |(Patient.surname % searchterm))

    jsonResult = []
    for result in results:
        # Check if result is already a connection
        currentConnections = json.loads(getConnections(username))

        for connection in json.loads(currentConnections['outgoing']):
            if connection['username'] == result['username']:
                result['message'] = "Already Requested"
        
        for connection in json.loads(currentConnections['incoming']):
            if connection['username'] == result['username']:
                result['message'] = "Request Waiting"

        for connection in json.loads(currentConnections['completed']):
            if connection['username'] == result['username']:
                result['message'] = "Already Connected"

        jsonResult.append(result)
    return json.dumps(jsonResult)

def getConnectionStatus(username, target):
    currentConnections = json.loads(getConnections(username))

    for connection in json.loads(currentConnections['outgoing']):
        if connection['username'] == target:
            return "Already Requested"
    
    for connection in json.loads(currentConnections['incoming']):
        if connection['username'] == target:
            return "Request Waiting"

    for connection in json.loads(currentConnections['completed']):
        if connection['username'] == target:
            return "Already Connected"
    return "None"

####
# Client/Client relationships
####
@app.route('/api/createConnection', methods=['POST', 'GET'])
@auth.login_required
def createConnection():
    return createConnection(request.form)

def createConnection(details):
    """Creates an initial connection between two users. POST [username, target]"""
    # Get users
    currentUser = details['username']
    targetUser = details['target']

    # Get user types
    currentUser_type = json.loads(getAccountInfo(currentUser))['accounttype']
    targetUser_type = json.loads(getAccountInfo(targetUser))['accounttype']

    # Need to check if connection already exists, requested, or if they have requested for you.
    check = getConnectionStatus(currentUser, targetUser)
    if check != "None":
        return check

    # Generate 4 digit code
    x = ""
    for n in range(0,4):
        x += str(random.randrange(1,9))
    x = int(x)

    # Insert into Connection table
    newConnection = Relationship.create(
        code = x,
        requestor = currentUser,
        requestortype = currentUser_type,
        target = targetUser,
        targettype = targetUser_type
    )
    with database.transaction():
        newConnection.save()
        createNotificationRecord(targetUser, "Connection Request", int(newConnection.connectionid))
        return str(x)
    return "False"

@app.route('/api/completeConnection', methods=['POST', 'GET'])
@auth.login_required
def completeConnection():
    return completeConnection(request.form)

def completeConnection(details):
    """Verify a code on input to allow the completion of an attempted connection. POST[ username, requestor, codeattempt] """
    #Take attempted code, match with a entry where they are target
    target = details['username']
    requestor = details['requestor']
    attemptedCode = int(details['codeattempt'])

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
            
            #creates the notification to inform the original requestor
            createNotificationRecord(requestor, "New Connection", None)

        return "Connection to " + requestor + " completed"
    else:
        return "Incorrect code"
    return None

@app.route('/api/deleteConnection', methods=['POST'])
@auth.login_required
def deleteConnection():
    """Deletes connection between a patient and carer POST[user, connection]"""
    return deleteConnection(request.form)

def deleteConnection(details):
    userType = json.loads(getAccountInfo(details['user']))['accounttype']
    connectionType = json.loads(getAccountInfo(details['connection']))['accounttype']

    if (userType == "Patient" and connectionType == "Carer"):
        instance = Patientcarer.select().where(Patientcarer.patient == details['user'] and Patientcarer.carer == details['connection']).get()
        with database.transaction():
            instance.delete_instance()
            return "True"
    elif (userType == "Carer" and connectionType == "Patient"):
        instance = Patientcarer.select().where(Patientcarer.patient == details['connection'] and Patientcarer.carer == details['user']).get()
        with database.transaction():
            instance.delete_instance()
            return "True"
    return "False"

@app.route('/api/cancelConnection', methods=['POST'])
@auth.login_required
def cancelRequest():
    return cancelRequest(request.form)

def cancelRequest(details):
    """Cancels the user request to connect before completion"""
    try:
        instance = Relationship.select().where(Relationship.requestor == user).get()
        with database.transaction():
            instance.delete_instance()
            return "True"
    except RelationshipDoesNotExist:
        instance = Relationship.select().where(Relationship.target == connection).get()
        with database.transaction():
            instance = Relationship.select().where(Relationship.requestor == details['user'] and Relationship.target == details['connection']).get()
            instance.delete_instance()
            return "True"
    except Relationship.DoesNotExist:
        try:
            with database.transaction():
                instance = Relationship.select().where(Relationship.requestor == details['connection'] and Relationship.target == details['user']).get()
                instance.delete_instance()
                return "True"
        except:
            return "False"
    return "False"

@app.route('/api/getConnections', methods=['POST'])
@auth.login_required
def getConnections():
    return getConnections(request.form['username'])

def getConnections(username):
    """Gets the valid connections between two users"""
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
@auth.login_required
def addPatientAppointment():
  return addPatientAppointment(request.form)

#allows a all self appointments to be added 
#Note originally there was going to be a seperate method for carers, however this is no longer the case. 
def addPatientAppointment(details):
# Build insert user query
  if details['private'] == "True":
    isPrivate = True
  else: 
    isPrivate = False

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
    private = isPrivate
  )

  appId = str(appointmentInsert.execute())
  
  return appId

@app.route('/api/addInviteeAppointment', methods=['POST'])
@auth.login_required
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
    description = details['description'],
    private = False
    )

  appId = str(appointmentInsert.execute())
  createNotificationRecord(details['username'], "Appointment Invite", appId)
  
  return appId

#receives the request from android to allow a user to view their upcoming appointments
@app.route('/api/getAllAppointments', methods=['POST'])
@auth.login_required
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
    appointment['androideventid'] = app.androideventid
    
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
@auth.login_required
def deleteAppointment():
  return deleteAppointment(request.form['username'], request.form['appid'])

def deleteAppointment(user, appid):
  isCreator = Appointments.select().where(Appointments.appid == appid).get()

  if isCreator.creator.username == user:
    with database.transaction():
        if isCreator.invitee.username != None:
            invitee = isCreator.invitee.username
            createNotificationRecord(invitee, "Appointment Cancelled", None)
        isCreator.delete_instance()

    return "Appointment Deleted"

#gets the appointment that is to be updated
@app.route('/api/getUpdateAppointment', methods=['POST'])
@auth.login_required
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
@auth.login_required
def updateAppointment():
  return updateAppointment(request.form['appid'], request.form['name'], request.form['apptype'], request.form['addressnamenumber'], request.form['postcode'], request.form['startdate'], request.form['starttime'], request.form['enddate'], request.form['endtime'], request.form['other'], request.form['private'])

def updateAppointment(appid, name, apptype, addressnamenumber, postcode, startDate, startTime, endDate, endTime, description, private):
  if private == "True":
    isPrivate = True
  else: 
    isPrivate = False

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
    private = isPrivate).where(Appointments.appid == appid)

  with database.transaction():
    updateAppointment.execute()

    #check if the appointment has an invitee
    appointment = Appointments.select().where(Appointments.appid == appid).get()
    if appointment.invitee.username != None:
        createNotificationRecord(appointment.invitee.username, "Appointment Updated", appid)


  return "Appointment Updated"

@app.route('/api/addMedication', methods=['POST'])
@auth.login_required
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
@auth.login_required
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

@app.route('/api/getMedications')
@auth.login_required
def getMedications():
    return getMedications()

def getMedications():
    medicationList = []
    result = Medication.select()
    for x in result:
        medicationList.append(x.name)
    return json.dumps(medicationList)

@app.route('/api/addPrescription', methods=['POST'])
@auth.login_required
def addPrescription():
    return addPrescription(request.form)

def addPrescription(details):
    insertPrescription = Prescription.create(
        username = details['username'],
        medication = details['medication'],
        dosage = details['dosage'],
        frequency = details['frequency'],
        quantity = details['quantity'],
        dosageunit = details['dosageunit'],
        frequencyunit = details['frequencyunit'],
        startdate = details['startdate'],
        enddate = details['enddate'],
        repeat = details['repeat'],
        stockleft = details['stockleft'],
        prerequisite = details['prerequisite'],
        dosageform = details['dosageform'])

    try:
        with database.transaction():
            insertPrescription.save()
            createNotificationRecord(details['username'], "Prescription Added", int(insertPrescription.prescriptionid))
            return details['medication'] + " " + details['dosage'] + details['dosageunit'] + "  added for " + details['username']
    except:
        return "Failed"

@app.route('/api/editPrescription', methods=['POST'])
@auth.login_required
def editPrescription():
    return editPrescription(request.form)

def editPrescription(details):
    updatePrescription = Prescription.update(
        medication = details['medication'],
        dosage = details['dosage'],
        frequency = details['frequency'],
        quantity = details['quantity'],
        dosageunit = details['dosageunit'],
        frequencyunit = details['frequencyunit'],
        startdate = details['startdate'],
        enddate = details['enddate'],
        repeat = details['repeat'],
        stockleft = details['stockleft'],
        prerequisite = details['prerequisite'],
        dosageform = details['dosageform']).where(Prescription.prescriptionid == details['prescriptionid'])

    try:
        updatePrescription.execute()
        patient = Prescription.select().where(Prescription.prescriptionid == details['prescriptionid']).get()
        createNotificationRecord(patient.username.username, "Prescription Updated", details['prescriptionid'])

        return details['medication'] + " " + details['dosage'] + details['dosageunit'] + "  updated for " + details['username']
    except:
        return "Failed"

@app.route('/api/deletePrescription', methods=['POST'])
@auth.login_required
def deletePrescription():
    return deletePrescription(request.form['prescriptionid'])

def deletePrescription(prescriptionid):
    try:
        instance = Prescription.select().where(Prescription.prescriptionid == prescriptionid).get()
        with database.transaction():
            instance.delete_instance()
            return "Deleted"
    except:
        return "Failed"

@app.route('/api/getPrescriptions', methods=['POST'])
@auth.login_required
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

@app.route('/api/getActivePrescriptions', methods=['POST'])
@auth.login_required
def getActivePrescriptions():
    return getActivePrescriptions(request.form['username'])

def getActivePrescriptions(username):
    allPrescriptions = json.loads(getPrescriptions(username))
    return json.dumps([prescription for prescription in allPrescriptions if (datetime.datetime.strptime(prescription['startdate'], "%Y-%m-%d") < datetime.datetime.now() and datetime.datetime.strptime(prescription['enddate'], "%Y-%m-%d") > datetime.datetime.now())])

@app.route('/api/getUpcomingPrescriptions', methods=['POST'])
@auth.login_required
def getUpcomingPrescriptions():
    return getUpcomingPrescriptions(request.form['username'])

def getUpcomingPrescriptions(username):
    allPrescriptions = json.loads(getPrescriptions(username))
    return json.dumps([prescription for prescription in allPrescriptions if (datetime.datetime.strptime(prescription['startdate'], "%Y-%m-%d") >= datetime.datetime.now())])

@app.route('/api/getExpiredPrescriptions', methods=['POST'])
@auth.login_required
def getExpiredPrescriptions():
    return getExpiredPrescriptions(request.form['username'])

def getExpiredPrescriptions(username):
    allPrescriptions = json.loads(getPrescriptions(username))
    return json.dumps([prescription for prescription in allPrescriptions if (datetime.datetime.strptime(prescription['enddate'], "%Y-%m-%d") < datetime.datetime.now())])

@app.route('/api/getPrescription', methods=['POST'])
@auth.login_required
def getPrescription():
    return getPrescription(request.form)

def getPrescription(details):
    prescriptionid = details['prescriptionid']
    prescription = Prescription.select().where(Prescription.prescriptionid == prescriptionid).dicts().get()
    prescription['startdate'] = str(prescription['startdate'])
    prescription['enddate'] = str(prescription['enddate'])
    return json.dumps(prescription)


@app.route('/api/searchNHSDirectWebsite', methods=['POST'])
@auth.login_required
def searchNHSDirect():
    return searchNHSDirect(request.form['searchterms'])

def searchNHSDirect(search):
    newTerm = search.replace(" ", "+")
    website = "http://www.nhs.uk/Search/Pages/Results.aspx?___JSSniffer=true&q="
    searchWeb = website + newTerm
    return searchWeb

@app.route('/api/getDeactivateReasons', methods=['POST','GET'])
@auth.login_required
def getDeactivateReasons():
    return getDeactivateReasons()

def getDeactivateReasons():
    """Returns a JSON list of possible reasons a user can deactivate"""
    reasons = Deactivatereason.select()
    reasonList = []
    for reason in reasons:
        reasonList.append(reason.reason)
    reasonList = json.dumps(reasonList)
    return reasonList

@app.route('/api/getAppointmentTypes', methods=['POST','GET'])
@auth.login_required
def getAppointmentTypes():
    return getAppointmentTypes()

def getAppointmentTypes():
    """Returns a JSON list of possible appointment types"""
    types = Appointmenttype.select()
    typeList = []
    for appType in types:
      typeList.append(appType.type)
    typeList = json.dumps(typeList)
    return typeList

@app.route('/api/addAndroidEventId', methods=['POST'])
@auth.login_required
def addAndroidEventId():
  dbId = request.form['dbid']
  androidId = request.form['androidid']
  addAndroidId = Appointments.update(androideventid=androidId).where(Appointments.appid==dbId).execute()
  return "Android ID added to database"

def createNotificationRecord(user, notificationType, relatedObject):
    #dictionary mapping notificationType to referencing table
    notificationTypeTable = {}
    notificationTypeTable['Connection Request'] = "Relationship"
    notificationTypeTable['New Connection'] = ""
    notificationTypeTable['Prescription Added'] = "Prescription"
    notificationTypeTable['Prescription Updated'] = "Prescription"
    notificationTypeTable['Appointment Invite'] = "Appointments"
    notificationTypeTable['Appointment Updated'] = "Appointments"
    notificationTypeTable['Appointment Cancelled'] = ""
    notificationTypeTable['Password Reset'] = ""

    createNotification = Notification.insert(
        username = user,
        notificationtype = notificationType,
        relatedObjectTable = notificationTypeTable[notificationType], 
        relatedObject = relatedObject
    )

    with database.transaction():
        createNotification.execute()
        return "True"
    return "False"

@app.route('/api/getNotifications', methods=['POST'])
@auth.login_required
def getNotifications():
    return getNotifications(request.form['username'])

def getNotifications(username):
    """Returns all of the notifications that have been associated with a user"""
    notifications = Notification.select().dicts().where(Notification.username == username and Notification.dismissed == False)

    notificationList = []
    for notification in notifications:
        notification['content'] = getNotificationContent(notification)
        notification['link'] = getNotificationLink(notification)
        notification['type'] = getNotificationTypeClass(notification)
        notificationList.append(notification)

    return json.dumps(notificationList)

def getNotificationContent(notification):
    """gets the body/content of the notification"""
    if notification['notificationtype'] == "Connection Request":
        requestor = Relationship.select().where(Relationship.connectionid == notification['relatedObject']).get()
        content = "You have a new connection request from " + requestor.requestor.username
    
    if notification['notificationtype'] == "New Connection":
        content = "You have a new connection, click above to view."
    
    if notification['notificationtype'] == "Prescription Added":
        prescription = Prescription.select().where(Prescription.prescriptionid == notification['relatedObject']).get()
        content = "A new prescription for " + prescription.medication.name + " has been added to your profile."

    if notification['notificationtype'] == "Prescription Updated":
        prescription = Prescription.select().where(Prescription.prescriptionid == notification['relatedObject']).get()
        content = "Your prescription for " + prescription.medication.name + " has been updated."
    
    if notification['notificationtype'] == "Appointment Invite":
        appointment = Appointments.select().where(Appointments.appid == notification['relatedObject']).get()
        content = appointment.creator.username + " has added an appointment with you on" + str(appointment.startdate) + "."

    if notification['notificationtype'] == "Appointment Updated":
        appointment = Appointments.select().where(Appointments.appid == notification['relatedObject']).get()
        content = appointment.creator.username + " has updated the following appointment with you: " + str(appointment.name) + "."

    if notification['notificationtype'] == "Appointment Cancelled":
        content = "One of your appointments has been cancelled, click above to view your updated calendar."

    if notification['notificationtype'] == "Password Reset":
        content = "Your password has been changed successfully."
    
    return content

def getNotificationLink(notification):
    """gets the notification link that will make it clickable"""
    if notification['notificationtype'] == "Connection Request":
        link = "/profile?go=connections"
    
    if notification['notificationtype'] == "New Connection":
        link = "/profile?go=connections"
    
    if notification['notificationtype'] == "Prescription Added":
        link = "/prescriptions"

    if notification['notificationtype'] == "Prescription Updated":
        link = "/prescriptions"
    
    if notification['notificationtype'] == "Appointment Invite":
        link = "/appointments"

    if notification['notificationtype'] == "Appointment Updated":
        link = "/appointments"

    if notification['notificationtype'] == "Appointment Cancelled":
        link = "/appointments"

    if notification['notificationtype'] == "Password Reset":
        link = "/"
    return link

def getNotificationTypeClass(notification):
    """gets the class which in turn will decide the background colour of the notification"""
    notificationClass = Notificationtype.select().where(Notificationtype.typename == notification['notificationtype']).get()
    return notificationClass.typeclass

@app.route('/api/dismissNotification', methods=['POST'])
@auth.login_required
def dismissNotification():
    return dismissNotification(request.form['notificationid'])

def dismissNotification(notificationid):
    """This sets the dismiss boolean field in the database to true"""
    dismiss = Notification.update(dismissed=True).where(Notification.notificationid == notificationid)

    with database.transaction():
        dismiss.execute()
        return "True"
    return "False"

def passwordExpiration(username):
    """This checks whether the password that the user is using is about to expire"""
    passwordDetails = uq8LnAWi7D.select().where((uq8LnAWi7D.username == username) & (uq8LnAWi7D.iscurrent==True)).get()
    expirationDate = passwordDetails.expirydate
    today = datetime.datetime.now().date()
    remainingDays = ((expirationDate - today).total_seconds())/86400
    #check the number of days until expiration
    if int(remainingDays) < 1:
        return "Reset"
    elif int(remainingDays) < 11: 
        return "<11"
    else:
        return "Authenticated"

@app.route('/api/expiredResetPassword', methods=['POST'])
@auth.login_required
def expiredResetPassword():
    return expiredResetPassword(request.form)

def expiredResetPassword(request):
    """reset a password that has expired or is expiring"""
    user = request['username']
    newPassword = request['newpassword']

    #set existing passwords to not current
    notCurrent = uq8LnAWi7D.update(iscurrent = False).where(uq8LnAWi7D.username == user)
    
    # Build insert password query
    newCredentials = uq8LnAWi7D.insert(
      username = user,
      password = sha256_crypt.encrypt(newPassword),
      iscurrent = True,
      expirydate = str(datetime.date.today() + datetime.timedelta(days=90))
    )

    with database.transaction():
        notCurrent.execute()
        newCredentials.execute()

        createNotificationRecord(user, "Password Reset", None)
        return "True"
    return "False"
