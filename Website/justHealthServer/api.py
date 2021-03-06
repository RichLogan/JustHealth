from justHealthServer import app
from flask import Flask, render_template, request, session, redirect, url_for, abort, send_from_directory, request_started
from flask.ext.httpauth import HTTPBasicAuth
# Line 5 !!!MUST!!! be the database import in order for /runTests.sh to work. Please do not change without also altering /runTests.sh
from database import *
from gcm import *
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
import base64

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username,password):
    """
    Checks if a supplied password is correct for a specific user.

    :param username: The username submitting the request.
    :type username: str.

    :param password: The encrypted password.
    :type password: str.

    :returns: boolean -- Success
    """
    plaintextPassword = decryptPassword(password)
    try:
        hashedPassword = uq8LnAWi7D.get((uq8LnAWi7D.username == username) & (uq8LnAWi7D.iscurrent==True)).password
        return sha256_crypt.verify(plaintextPassword, hashedPassword)
    except:
        return False

def getUsernameFromHeader():
    """
    Decodes the HTTP Basic header and retrieves the username. 

    :returns: str -- Username submitting the request.
    """
    authHeader = str(request.headers.get('Authorization'))
    authHeader = authHeader.replace("Basic ", "")
    decodedAuthHeader = base64.b64decode(authHeader)
    authUsername = decodedAuthHeader.split(':')[0]
    return authUsername

def verifyContentRequest(username, targetUsername):
    """
    This co-ordinates the running of the other methods, depending on the parameters that are passed.

    This method can be called from anywhere and if the method is retrieving records for the same person that is authenticated targetUsername should be sent accross as an empty string

    :param username: The username of the request originator.
    :type username: str.

    :param targetUsername: The username owning the resource being accessed, if any.
    :type targetUsername: str.

    :returns: boolean -- Success.
    :raises: HTTP 401.
    """
    authUsername = getUsernameFromHeader()
    if targetUsername == "":
        return verifySelf(authUsername, username)
    elif verifySelf(authUsername, username):
        return verifyCarer(username, targetUsername)
    else:
        return abort(401)

def verifySelf(authUsername, methodUsername):
    """
    Checks that the user authenticated by HTTP Basic is the same as user that is associated with the records being read/written

    :param authUsername: username from HTTP header.
    :type authUsername: str.

    :param methodUsername: The username being password to the method.
    :type methodUsername: str.

    :returns: boolean -- success.
    :raises: HTTP 401.
    """
    if authUsername == methodUsername:
        return True
    else:
        return abort(401)

def verifyCarer(username, targetUsername):
    """
    Checks that the user authenticated by HTTP Basic is connected to the user that is associated with the records being read/written

    :param username: Username of user sending the request. 
    :type username: str. 

    :param targetUsername: Username of the owner of the requested resource. 
    :type targetUsername: str. 

    :returns: True if successful, else HTTP 401 Unauthorized. 

    """
    accountInfo = json.loads(getAccountInfo(username))
    if accountInfo['accounttype'] == "Carer":
        if getConnectionStatus(username, targetUsername) == "Already Connected":
            return True
        else:
            return abort(401)
    else:
        return abort(401)

@app.route("/api/encryptPassword", methods=["POST"])
def encryptPassword():
    """
    Encrypts the users password and returns it to them

    :link: /api/encryptPassword

    :param request.form: POST request containing plaintext [password].
    :type request.form: dict.

    :returns: str -- Encrypted password.
    """
    # Used so that we are able to store the encrypted users password in android SharedPreferences
    plaintext = request.form['password']
    cipherText = encrypt(app.secret_key, plaintext)
    stringCipher = binascii.hexlify(cipherText)
    return stringCipher

def decryptPassword(cipherText):
    """
    Decrypts the users password and returns it so that we are able to authenticate them.

    :param cipherText: Encrypted password.
    :type cipherText: str.

    :returns: str -- Plaintext password.
    """
    #used so that we are able to store the encrypted users password in android SharedPreferences
    bytesCipher = binascii.unhexlify(cipherText)
    plaintext = decrypt(app.secret_key, bytesCipher)
    return plaintext

@app.route("/api/registerUser", methods=["POST"])
def registerUser():
    return registerUser(request.form)

def registerUser(details):
    """
    Allows registration of an account. 

    :link: /api/registerUser

    :param details: The dictionary of user details. Includes[username], [firstname], [surname], [dob], [ismale], [email], [password], [confirmpassword], [accounttype], [terms]
    :type details: dict. 

    :returns: str -- Success as String
    """
    # Build User Registration
    try:
      profile = {}
      profile['username'] = details['username']
      profile['firstname'] = details['firstname']
      profile['surname'] = details['surname']
      profile['dob'] = details['dob']
      profile['ismale'] = details['ismale']
      profile['email'] = details['email']
      profile['password'] = details['password']
      profile['confirmpassword'] = details['confirmpassword']
      accountType = details['accounttype']
      profile['profilepicture'] = "default.png"
    except KeyError, e:
      return "All fields must be filled out"
    try:
      profile['terms'] = details['terms']
    except KeyError, e:
      return "Terms and Conditions must be accepted"

    # Validate all input
    for key, value in profile.iteritems():
      value = value.strip()

    # Validate Dates
    try:
        profile['dob'] = datetime.datetime.strptime(profile['dob'], '%Y-%m-%d')
    except ValueError:
        return "Invalid date"

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
      verified  = False,
      profilepicture = profile['profilepicture']
    )

    if accountType == "patient":
        accountType = Patient
    elif accountType == "carer":
        accountType = Carer
    elif accountType == "Admin":
        accountType = Admin

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
    """
    Checks to see if a username has already been taken

    :link: /api/usernameCheck

    :param request.form: The [username] to check.
    :type request.form: dict.

    :returns: boolean - If username is available or not.
    """
    return str(Client.select().where(Client.username == request.form['username']).count() != 0)

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    """
    Authenticates a username and password and returns the result of the authentication check.

    :link: /api/authenticate

    :param request.form: [username, password]. 
    :type request.form: dict. 

    :returns: str -- Result message of authentication attempt.
    """
    try:
        attempted = Client.get(username=request.form['username'])
    except Client.DoesNotExist:
        return "Incorrect username/password"

    # Check Password
    try:
        hashedPassword = uq8LnAWi7D.get((uq8LnAWi7D.username == attempted.username) & (uq8LnAWi7D.iscurrent==True)).password.strip()
    except uq8LnAWi7D.DoesNotExist:
        return "There is no current password for this username. Please use the forgot password link to reset your account."
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
    if verifyContentRequest(request.form['username'], ""):
        return deactivateAccount(request.form)

def deactivateAccount(details):
    """
    Ability to deactivate an account. A user can choose to have their data deleted or kept. 

    :link: /api/deactivateaccount

    :param details: Dictionary of [username], [comments], [reason]. 
    :type details: dict. 

    :returns: str -- Deleted, Kept or an error message. 
    """
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
        deleteAppointments = Appointments.delete().where(Appointments.invitee == username)
        deletedUser = Client.get(Client.username == username)
        with database.transaction():
            deleteAppointments.execute()
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
    return resetPassword(request.form)

def resetPassword(details):
    """
    Ability to reset a password if one is forgotton.

    :link: /api/resetpassword

    :param details: Dictionary of profile and password details [username], [confirmemail], [newpassword], [confirmnewpassword], [confirmdob].
    :type details: dict.

    :returns: str -- 'True' is successful. 
    """
    try:
        profile = {}
        profile['username'] = details['username']
        profile['confirmemail'] = details['confirmemail']
        profile['newpassword'] = details['newpassword']
        profile['confirmnewpassword'] = details['confirmnewpassword']
        profile['confirmdob'] = details['confirmdob']
    except KeyError, e:
        return "All fields must be filled out"

    getEmail = Client.get(username=profile['username']).email.strip()
    getDob = str(Client.get(username=profile['username']).dob)

    if (getEmail == profile['confirmemail']) and (getDob == profile['confirmdob']):
        # Set the old password to iscurrent = false
        notCurrent = uq8LnAWi7D.update(iscurrent = False).where(uq8LnAWi7D.username == profile['username'])
        notVerified = Client.update(verified = False).where(Client.username == profile['username'])

        # Encrypt the password
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
        return profile['username']

####
# Account Information
####

@app.route('/api/images/<filename>')
@auth.login_required
def getProfilePictureAPI(filename):
    """
    Returns profile picture with the specified filename. 

    :link: /api/images/<filename>

    :param filename: The name of the file to return. 
    :type filename: str. 

    :returns: file -- Image requested. 
    """
    return send_from_directory(app.config['PROFILE_PICTURE'], filename)

@app.route('/api/getAccountInfo', methods=['POST'])
@auth.login_required
def getAccountInfo():
    if verifyContentRequest(request.form['username'], ""):
        return getAccountInfo(request.form['username'])

def getAccountInfo(username):
    """
    Returns all information about a user. 

    :link: /api/getAccountInfo
    
    :param username: The username whose details are desired. 
    :type username: str. 

    :returns: json -- Dictionary of user's details. 
    """
    result = {}
    try:
      user = Patient.select().join(Client).where(Client.username==str(username)).get()
      result['accounttype'] = "Patient"
    except Patient.DoesNotExist:
        try:
            user = Carer.select().join(Client).where(Client.username==str(username)).get()
            result['accounttype'] = "Carer"
        except Carer.DoesNotExist:
            try:
                user = Admin.select().join(Client).where(Client.username==str(username)).get()
                result['accounttype'] = "Admin"
            except Admin.DoesNotExist:
                return "User does not exist"

    result['firstname'] = user.firstname
    result['surname'] = user.surname
    result['username'] = user.username.username
    result['email'] = user.username.email
    result['dob'] = str(user.username.dob)
    result['profilepicture'] = user.username.profilepicture
    result['telephonenumber'] = user.username.telephonenumber
    if user.ismale:
        result['gender'] = 'Male'
    else:
        result['gender'] ='Female'
    return json.dumps(result)

def getCarers(username):
    """
    Returns all carers connected to a patient. 

    :param username: The patient whose carers should be retrieved. 
    :type username: str. 

    :returns: list -- List of carers usernames. 
    """
    results = []
    for c in Patientcarer.select().where(Patientcarer.patient == username):
        results.append(c.carer.username)
    return results

@app.route('/api/setProfilePicture', methods=['POST'])
def setProfilePicture():
    return setProfilePicture(request.files)

def setProfilePicture(details):
    """
    Sets a profile picture for a user

    :link: /api/setProfilePicture

    :param details: Files to upload, although only accepts one file of key [image], is retained as a dictionary due to request standards. 
    :type details: dict. 

    :returns: Filename/path of newly uploaded file, or False. 
    """
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
    if verifyContentRequest(request.form['username'], ""):
        return editProfile(request.form, request.files)

def editProfile(profile, picture):
    """
    Allows a user to edit their profile details. 

    :link: /api/editProfile

    :param profile: Dictionary of profile details. 
    :type profile: dict. 

    :param picture: Optional profile picture to update. 
    :type picture: file. 

    :returns: str -- Message. 
    """
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
    if (filename != "") and (filename != None):
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
    if verifyContentRequest(request.form['username'], ""):
        return changePasswordAPI(request.form)

def changePasswordAPI(details):
    """
    Allows a user to change their password.

    :link: /api/changePassword

    :param details: Details of the user [username, oldpassword, newpassword, confirmnewpassword]. 
    :type details: dict. 

    :returns: str -- Success/Failure message. 
    """
    if details['newpassword'] != details['confirmnewpassword']:
        return "Passwords do not match"
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
                iscurrent = True,
                expirydate = str(datetime.date.today() + datetime.timedelta(days=90))
            )

            # Execute
            with database.transaction():
                currentPassword.save()
                newPassword.execute()
                return "Password changed successfully"
            return "Failed"
        else: return "Incorrect password"
    except: return "User does not exist"

####
# Account Helper Functions
####

def lockAccount(username):
    """
    Locks a user's account and sends an unlock email.  

    :param username: The username of the account to lock. 
    :type username: str. 
    """
    lockAccount = Client.update(accountlocked = True).where(Client.username == username)
    with database.transaction():
        lockAccount.execute()
    sendUnlockEmail(username)

####
# Email Functions
####
def getSerializer(secret_key=None):
    """
    Converts a username into a random key, in order to create a unique link

    :param secret_key: The secret key to use. Defaults to the applications secret key. 
    :type secret_key: str. 

    :returns: str -- Serialized username. 
    """
    if secret_key is None:
        secret_key = app.secret_key
    return URLSafeSerializer(secret_key)

def sendVerificationEmail(username):
    """
    Sends email to the user after registration asking for account verification

    :param username: The username to send the email to. 
    :type username: str. 
    """
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
    """
    Returns the username an email address belongs to. 

    :param email: The email whose owner should be returned. 
    :type email: str. 

    :returns: str -- The username or 'Failed'. 
    """
    try:
      username = Client.select(Client.username).where(Client.email == email).get()
      return username.username
    except Client.DoesNotExist:
      return "False"

def sendForgotPasswordEmail(username):
    """
    Sends email when password is forgotton. 

    :param username: Username to send email to.
    :type username: str. 
    """
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
    message = "Please reset your JustHealth account password here:\n" + str(resetLink) + " \n \n(Please do not use Internet Explorer to open this link)"
    m = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, recipient, subject)
    # Send
    server.sendmail(sender, recipient, m+message)
    server.quit()

def sendUnlockEmail(username):
    """
    Sends email to a user when account is locked due to too many unsuccessful attempts

    :param username: Username to send email to.
    :type username: str. 
    """
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
    """
    Sends user email confirming password reset

    :param username: Username to send email to.
    :type username: str. 
    """
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
    """
    Sends email to justhealth when a user has a question

    :param details: Contains the [message] and [username] who asked the question. 
    :type details: dict. 
    """
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
    if verifyContentRequest(request.form['username'], ""):
        return searchPatientCarer(request.form['username'], request.form['searchterm'])

def searchPatientCarer(username, searchterm):
    """
    Allows users to search for other users. 

    :link: /api/searchPatientCarer

    :param username: The username who has submitted the search. 
    :type username: str. 

    :param searchterm: The search term the user has submitted. 
    :type searchterm: str. 

    :returns: str/json -- The resultant message or list of search results. 
    """
    #get username, firstname and surname of current user
    results = {}
    searchterm = "%" + searchterm + "%"
    try:
        patient = Patient.get(username=username)
        results = Carer.select().dicts().where((Carer.username ** searchterm) | (Carer.firstname ** searchterm) |(Carer.surname ** searchterm))
    except Patient.DoesNotExist:
        results = Patient.select().dicts().where((Patient.username ** searchterm) | (Patient.firstname ** searchterm) |(Patient.surname ** searchterm))

    if results.count() == 0:
        return "No users found"

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
    """
    Returns the connection status between the two users. 
    Helper method for search. 

    :param username: The first username. 
    :type username: str. 

    :param target: The second username:
    :type target: str. 

    :returns: str -- The connection status. 
    """
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
    #although this is for a patient and a carer we only need to check the patient
    # because they aren't yet connected
    if verifyContentRequest(request.form['username'], ""):
        return createConnection(request.form)

def createConnection(details):
    """
    Creates an initial connection between two users.

    :link: /api/createConnection

    :param details: The two usernames as [username] and [target]. 
    :type details: dict. 

    :returns: str -- Result message. 
    """
    # Get users
    currentUser = details['username']
    targetUser = details['target']

    # Test Users
    try:
        doesUserExist = Client.select().where(Client.username == currentUser).get()
    except Client.DoesNotExist:
        return "User does not exist"
    try:
        doesTargetExist = Client.select().where(Client.username == targetUser).get()
    except Client.DoesNotExist:
        return "Target does not exist"

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
        return "Give the code '" + str(x) + "' to " + targetUser + " so they can accept your request"
    return "False"

@app.route('/api/completeConnection', methods=['POST', 'GET'])
@auth.login_required
def completeConnection():
    #The patient and carer are yet to be connected so therefore we only need to check
    # the account of the user that is making the request
    if verifyContentRequest(request.form['username'], ""):
        return completeConnection(request.form)

def completeConnection(details):
    """
    Verifies the connection code to allow the completion of an attempted connection.

    :link: /api/completeConnection

    :param details: A [codeattempt] to connect [username] with [requestor]. 
    :type details: dict. 

    :returns: str -- Result message. 
    """
    #Take attempted code, match with a entry where they are target
    target = details['username']
    requestor = details['requestor']
    attemptedCode = int(details['codeattempt'])

    # get record
    instance = Relationship.select().where((Relationship.requestor == requestor) & (Relationship.target == target)).get()
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
    #We only need to check the user and not the carer's authenticity
    # as no information about the patient is being returned.
    if verifyContentRequest(request.form['user'], ""):
        return deleteConnection(request.form)

def deleteConnection(details):
    """
    Delete an existing connection

    :link: /api/deleteConnection

    :param details: The dictionary of connection details: [user] (The deletion request), [connection] (The username of the connection delete). 
    :type details: dict. 

    :returns: str -- 'True' or 'False' for success. 
    """
    try:
        userType = json.loads(getAccountInfo(details['user']))['accounttype']
        connectionType = json.loads(getAccountInfo(details['connection']))['accounttype']
    except ValueError:
        return "Connection does not exist"

    try:
        instance = Patientcarer.select().where((Patientcarer.patient == details['user']) & (Patientcarer.carer == details['connection'])).get()
        with database.transaction():
            instance.delete_instance()
            return "True"
    except Patientcarer.DoesNotExist:
        try:
            instance = Patientcarer.select().where((Patientcarer.patient == details['connection']) & (Patientcarer.carer == details['user'])).get()
            with database.transaction():
                instance.delete_instance()
                return "True"

        except Patientcarer.DoesNotExist:
            return "False"
    return "False"

@app.route('/api/cancelConnection', methods=['POST'])
@auth.login_required
def cancelRequest():
    if verifyContentRequest(request.form['user'], ""):
        return cancelRequest(request.form)

def cancelRequest(details):
    """
    Cancels a request before it is established. 

    :link: /api/cancelConnection

    :param details: Dictionary giving [user]: The username of the cancelling party, [connection] The username user is connecting to. 
    :type details: dict. 

    :returns: str -- 'True' or 'False' for success. 
    """
    try:
        instance = Relationship.select().where((Relationship.requestor == details['user']) & (Relationship.target == details['connection'])).get()
        with database.transaction():
            instance.delete_instance()
            return "True"
    except Relationship.DoesNotExist:
        try:
            instance = Relationship.select().where((Relationship.target == details['user']) & (Relationship.requestor == details['connection'])).get()
            with database.transaction():
                instance.delete_instance()
                return "True"
        except Relationship.DoesNotExist:
            return "False"
    return "False"

@app.route('/api/getConnections', methods=['POST'])
@auth.login_required
def getConnections():
    #Any authenticated user is entitled to retrieve their connections
    # we do not need to check the persons that they are connected too.
    if verifyContentRequest(request.form['username'], ""):
        return getConnections(request.form['username'])

def getConnections(username):
    """
    Gets all connections for a specific user. 

    :link: /api/getConnections

    :param username: The username of the user to check. 
    :type username: str. 

    :returns: json -- Dictionary of incoming, outgoing, completed connections. Each value is a list of dictionaries representing each connection. 
    """
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
        person['profilepicture'] = details['profilepicture']
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
        person['profilepicture'] = details['profilepicture']
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
        person['email'] = details ['email']
        person['telephonenumber'] = details ['telephonenumber']
        person['accounttype'] = details['accounttype']
        person['profilepicture'] = details['profilepicture']
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
    if verifyContentRequest(request.form['creator'], ""):
        return addPatientAppointment(request.form)

#allows a all self appointments to be added
#Note originally there was going to be a seperate method for carers, however this is no longer the case.
def addPatientAppointment(details):
  """
  Allows a patient to add their own appointment

  :link: /api/addPatientAppointment

  :param details: Details of the appointment. 
    [creator]
    [name]
    [apptype]
    [addressnamenumber]
    [postcode]
    [startdate]
    [starttime]
    [enddate]
    [endtime]
    [description]
    [private]
  :type details: dict. 

  :returns: str -- The id of the newly created appointment. 
  """
  # Build insert user query
  if details['private'] == "False":
    isPrivate = False
  else:
    isPrivate = True

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
    #The creator will always be a carer, therefore we have to check that they are connected
    # to the patient that they are making the appointment with
    if verifyContentRequest(request.form['creator'], request.form['username']):
        return addInviteeAppointment(request.form)

def addInviteeAppointment(details):
  """
  Allows a carer to create an appointment with their patient

  :link: /api/addInviteeAppointment

  :param details: Details of appointment. 
    [creator]
    [name]
    [apptype]
    [addressnamenumber]
    [postcode]
    [startdate]
    [starttime]
    [enddate]
    [endtime]
    [description]
  :type details: dict. 

  :returns: str -- The id of the appointment. 
  """
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
    private = False,
    accepted = None
  )

  with database.transaction():
    appId = str(appointmentInsert.execute())
    createNotificationRecord(details['username'], "Appointment Invite", appId)
    return appId
  return"False"

#receives the request from android to allow a user to view their upcoming appointments
@app.route('/api/getAllAppointments', methods=['POST'])
@auth.login_required
def getAllAppointments():
    if request.form['loggedInUser'] == request.form['targetUser']:
        if verifyContentRequest(request.form['loggedInUser'], ""):
            return getAllAppointments(request.form['loggedInUser'], request.form['targetUser'])
    if verifyContentRequest(request.form['loggedInUser'], request.form['targetUser']):
        return getAllAppointments(request.form['loggedInUser'], request.form['targetUser'])

#gets the appointments from the database
def getAllAppointments(loggedInUser, targetUser):
  """
  Returns all appointments for a user. 

  :link: /api/getAllAppointments

  :param loggedInUser: The user requesting. 
  :type loggedInUser: str. 

  :param targetUser: The user whose appointments are being requested. 
  :type targetUser: str. 

  :returns: json -- List of appointments.
  """
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
    if app.invitee == None:
        appointment['invitee'] = ""
    else:
        appointment['invitee'] = app.invitee.username
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
    appointment['accepted'] = app.accepted

    dateTime = str(app.enddate) + " " + str(app.endtime)
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
    #if verifyContentRequest(request.form['username'], ""):
    return deleteAppointment(request.form['username'], request.form['appid'])

def deleteAppointment(user, appid):
  """
  Allows an appointment to be deleted. 

  :link: /api/deleteAppointment

  :param user: The username of the user attempting to delete. 
  :type user: str. 

  :param appid: The id of the appointment to deleted. 
  :type appid: int. 

  :returns: str -- Success message. 
  """
  try:
    isCreator = Appointments.select().where(Appointments.appid == appid).get()
  except Appointments.DoesNotExist:
    return "Appointment does not exist"

  if isCreator.creator.username == user:
    with database.transaction():
        if isCreator.invitee != None:
            invitee = isCreator.invitee.username
            createNotificationRecord(invitee, "Appointment Cancelled", None)
        isCreator.delete_instance()

    return "Appointment Deleted"

#gets the appointment that is to be updated
@app.route('/api/getUpdateAppointment', methods=['POST'])
@auth.login_required
def getUpdateAppointment():
    if verifyContentRequest(request.form['username'], ""):
        return updateAppointment(request.form['username'], request.form['appid'])

def getUpdateAppointment(user, appid):
  """
  Returns the details of the specified appointment. 

  :link: /api/getUpdateAppointment

  :param user: The user requesting the resource. 
  :type user: str. 

  :param appid: The id of the requested appointment. 
  :type appid: int. 

  :returns: json -- Details of the appointment. 
  """
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
    #username isn't sent with the request, so here we need to get the creator of the appointment from the database.
    appointment = Appointments.select().where(Appointments.appid == request.form['appid']).get()
    user = appointment.creator.username
    if verifyContentRequest(user, ""):
        return updateAppointment(request.form['appid'], request.form['name'], request.form['apptype'], request.form['addressnamenumber'], request.form['postcode'], request.form['startdate'], request.form['starttime'], request.form['enddate'], request.form['endtime'], request.form['other'], request.form['private'])

def updateAppointment(appid, name, apptype, addressnamenumber, postcode, startDate, startTime, endDate, endTime, description, private):
  """
  Updates a specified appointment. 

  :link: /api/updateAppointment

  :param appid: The id of the appointment to update. 
  :type appid: int. 
  
  :param name: Appointment name. 
  :type name: str. 
  
  :param apptype: Appointment type. 
  :type apptype: str. 
  
  :param addressnamenumber: Address. 
  :type addressnamenumber: str. 
  
  :param postcode: Postcode. 
  :type postcode: str. 
  
  :param startDate: Start Date. 
  :type startDate: date. 
  
  :param startTime: Start Time. 
  :type startTime: time. 
  
  :param endDate: End Date. 
  :type endDate: date. 
  
  :param endTime: End Time. 
  :type endTime: time. 
  
  :param description: Description. 
  :type description: str. 
  
  :param private: If the appointment is private or not. 
  :type private: boolean. 

  :returns: str -- Success message. 
  """
  checkInvitee = Appointments.select().where(Appointments.appid == appid).get()
  #This stops the appointment from being marked as private when it is an invitee appointment
  if checkInvitee.invitee != None:
    isPrivate = False
  else:
    if private == "False":
      isPrivate = False
    else:
      isPrivate = True

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
    private = isPrivate,
    accepted = None).where(Appointments.appid == appid)

  with database.transaction():
    updateAppointment.execute()

    #check if the appointment has an invitee
    appointment = Appointments.select().where(Appointments.appid == appid).get()
    if appointment.invitee != None:
        createNotificationRecord(appointment.invitee.username, "Appointment Updated", appid)
  return "Appointment Updated"

@app.route('/api/getAppointment', methods=['POST'])
# @auth.login_required
def getAppointment():
    # if verifyContentRequest(request.form['user'], ""):
    return getAppointment(request.form['user'], request.form['appid'])

def getAppointment(user, appid):
    """
    Returns details of an appointment

    :link: /api/getAppointment

    :param user: The user submitting the request.
    :type user: str.

    :param appid: The id of the appointment.
    :type appid: int.

    :returns: json -- Details of the appointment.
    """
    try: 
        isRelated = Appointments.select().where(Appointments.appid == appid).get()
    except Appointments.DoesNotExist:
        return "Appointment does not exist"

    if (isRelated.creator.username == user) or (isRelated.invitee.username):
        appointment = {}
        appointment['appid'] = isRelated.appid
        appointment['creator'] = isRelated.creator.username
        appointment['name'] = isRelated.name
        appointment['apptype'] = str(isRelated.apptype.type)
        appointment['addressnamenumber'] = isRelated.addressnamenumber
        appointment['postcode'] = isRelated.postcode
        appointment['startdate'] = str(isRelated.startdate)
        appointment['starttime'] = str(isRelated.starttime)
        appointment['enddate'] = str(isRelated.enddate)
        appointment['endtime'] = str(isRelated.endtime)
        appointment['description'] = isRelated.description
        appointment['private'] = isRelated.private

        return json.dumps(appointment)

@app.route('/api/acceptDeclineAppointment', methods=['POST'])
@auth.login_required
def acceptDeclineAppointment():
    if verifyContentRequest(request.form['username'], ""):
        return acceptDeclineAppointment(request.form['username'], request.form['action'], request.form['appid'])

def acceptDeclineAppointment(user, action, appointmentId):
    """
    Allows an appointment to be accepted or declined.

    :link: /api/acceptDeclineAppointment    

    :param user: The user submitting the action.
    :type user: str.

    :param action: "Accept" to accept or anything else to "Decline".
    :type action: str.

    :param appointmentId: The id of the appointment to accept / decline.
    :type appointmentId: int.
    """
    appointment = Appointments.select().where(Appointments.appid == appointmentId).get()
    if user == appointment.invitee.username:
        if action == "Accept":
            accepted = True
            notificationType = "Appointment Accepted"
            result = "You have accepted this appointment."
        else:
            accepted = False
            notificationType = "Appointment Declined"
            result = "You have declined this appointment."
        submitAction = Appointments.update(accepted = accepted).where(Appointments.appid == appointmentId)

        with database.transaction():
            submitAction.execute()
            createNotificationRecord(appointment.creator.username, notificationType, appointmentId)
            return result

        return "Failed"
    return "You have not been invited to this appointment."

def addMedication(medicationName):
    """
    Allows a medication to be added to the system.

    :param medicationName: The name of the medication to be added.
    :type medicationName: str.

    :returns: "Added" or "Already Exists" or "False" for other error.
    """
    if medicationName != None:
        insertMedication = Medication.insert(
            name = medicationName
        )
        with database.transaction():
            try:
                insertMedication.execute()
                return "Added " + medicationName
            except IntegrityError:
                return medicationName + " already exists"
        return "False"
    return "False"

def deleteMedication(medicationName):
    """
    Allows a medication to be removed from the system.

    :param medicationName: The name of the medication to remove.
    :type medicationName: str.

    :returns: "Deleted" or "Not Found".
    """
    if medicationName != None:
        try:
            instance = Medication.select().where(Medication.name == medicationName).get()
            with database.transaction():
                instance.delete_instance()
            return "Deleted " + medicationName
        except:
            return medicationName + " not found" 
    return "Unable to accept none type"

@app.route('/api/getMedications')
@auth.login_required
def getMedications():
    return getMedications()

def getMedications():
    """
    Returns list of all medications in JustHealth system.

    :link: /api/getMedications

    :returns: json -- List of medication names.
    """
    medicationList = []
    result = Medication.select()
    for x in result:
        medicationList.append(x.name)
    return json.dumps(medicationList)

@app.route('/api/addPrescription', methods=['POST'])
@auth.login_required
def addPrescription():
    username = getUsernameFromHeader()
    if verifyContentRequest(username, request.form['username']):
        return addPrescription(request.form)

def addPrescription(details):
    """
    Allows creation of a prescription

    :link: /api/addPrescription

    :param details: Dictionary containing:
        [prescriptionid]
        [Monday],
        [Tuesday],
        [Wednesday],
        [Thursday],
        [Friday],
        [Saturday],
        [Sunday],
        [medication],
        [dosage],
        [frequency],
        [quantity],
        [dosageunit],
        [startdate],
        [enddate],
        [stockleft],
        [prerequisite],
        [dosageform]
    :type details: dict.

    :returns: str -- Failed or details of success.
    """
    Monday = False;
    try:
      if (details['Monday'] == True) or (details['Monday'] == "True") or (details['Monday'] == "true") or (details['Monday'] == "on"):
        Monday = True
    except KeyError, e:
      Monday = False

    Tuesday = False;
    try:
      if (details['Tuesday'] == True) or (details['Tuesday'] == "True") or (details['Tuesday'] == "true") or (details['Tuesday'] == "on"):
        Tuesday = True
    except KeyError, e:
      Tuesday = False

    Wednesday = False;
    try:
      if (details['Wednesday'] == True) or (details['Wednesday'] == "True") or (details['Wednesday'] == "true") or (details['Wednesday'] == "on"):
        Wednesday = True
    except KeyError, e:
      Wednesday = False

    Thursday = False;
    try:
      if (details['Thursday'] == True) or (details['Thursday'] == "True") or (details['Thursday'] == "true") or (details['Thursday'] == "on"):
        Thursday = True
    except KeyError, e:
      Thursday = False

    Friday = False;
    try:
      if (details['Friday'] == True) or (details['Friday'] == "True") or (details['Friday'] == "true") or (details['Friday'] == "on"):
        Friday = True
    except KeyError, e:
      Friday = False

    Saturday = False;
    try:
      if (details['Saturday'] == True) or (details['Saturday'] == "True") or (details['Saturday'] == "true") or (details['Saturday'] == "on"):
        Saturday = True
    except KeyError, e:
      Saturday = False

    Sunday = False;
    try:
      if (details['Sunday'] == True) or (details['Sunday'] == "True") or (details['Sunday'] == "true") or (details['Sunday'] == "on"):
        Sunday = True
    except KeyError, e:
        Sunday = False;

    insertPrescription = Prescription.insert(
        username = details['username'],
        medication = details['medication'],
        dosage = details['dosage'],
        frequency = details['frequency'],
        quantity = details['quantity'],
        dosageunit = details['dosageunit'],
        startdate = details['startdate'],
        enddate = details['enddate'],
        stockleft = details['stockleft'],
        prerequisite = details['prerequisite'],
        dosageform = details['dosageform'],
        Monday = Monday,
        Tuesday = Tuesday,
        Wednesday = Wednesday,
        Thursday = Thursday,
        Friday = Friday,
        Saturday = Saturday,
        Sunday  = Sunday
    )

    with database.transaction():
        result = insertPrescription.execute()
        createNotificationRecord(details['username'], "Prescription Added", int(result))
        return details['medication'] + " " + details['dosage'] + details['dosageunit'] + "  added for " + details['username']

@app.route('/api/editPrescription', methods=['POST'])
@auth.login_required
def editPrescription():
    username = getUsernameFromHeader()
    if verifyContentRequest(username, request.form['username']):
        return editPrescription(request.form)

def editPrescription(details):
    """
    Allows facility to edit a prescription.

    :link: /api/editPrescription

    :param details: Dictionary containing:
        [prescriptionid]
        [Monday],
        [Tuesday],
        [Wednesday],
        [Thursday],
        [Friday],
        [Saturday],
        [Sunday],
        [medication],
        [dosage],
        [frequency],
        [quantity],
        [dosageunit],
        [startdate],
        [enddate],
        [stockleft],
        [prerequisite],
        [dosageform]
    :type details: dict.

    :returns: str -- Failed or updated details.
    """
    Monday = False;
    try:
      if (details['Monday'] == True) or (details['Monday'] == "True") or (details['Monday'] == "true") or (details['Monday'] == "on"):
        Monday = True
    except KeyError, e:
      Monday = False

    Tuesday = False;
    try:
      if (details['Tuesday'] == True) or (details['Tuesday'] == "True") or (details['Tuesday'] == "true") or (details['Tuesday'] == "on"):
        Tuesday = True
    except KeyError, e:
      Tuesday = False

    Wednesday = False;
    try:
      if (details['Wednesday'] == True) or (details['Wednesday'] == "True") or (details['Wednesday'] == "true") or (details['Wednesday'] == "on"):
        Wednesday = True
    except KeyError, e:
      Wednesday = False

    Thursday = False;
    try:
      if (details['Thursday'] == True) or (details['Thursday'] == "True") or (details['Thursday'] == "true") or (details['Thursday'] == "on"):
        Thursday = True
    except KeyError, e:
      Thursday = False

    Friday = False;
    try:
      if (details['Friday'] == True) or (details['Friday'] == "True") or (details['Friday'] == "true") or (details['Friday'] == "on"):
        Friday = True
    except KeyError, e:
      Friday = False

    Saturday = False;
    try:
      if (details['Saturday'] == True) or (details['Saturday'] == "True") or (details['Saturday'] == "true") or (details['Saturday'] == "on"):
        Saturday = True
    except KeyError, e:
      Saturday = False

    Sunday = False;
    try:
      if (details['Sunday'] == True) or (details['Sunday'] == "True") or (details['Sunday'] == "true") or (details['Sunday'] == "on"):
        Sunday = True
    except KeyError, e:
        Sunday = False;

    updatePrescription = Prescription.update(
        medication = details['medication'],
        dosage = details['dosage'],
        frequency = details['frequency'],
        quantity = details['quantity'],
        dosageunit = details['dosageunit'],
        startdate = details['startdate'],
        enddate = details['enddate'],
        stockleft = details['stockleft'],
        prerequisite = details['prerequisite'],
        dosageform = details['dosageform'],
        Monday = Monday,
        Tuesday = Tuesday,
        Wednesday = Wednesday,
        Thursday = Thursday,
        Friday = Friday,
        Saturday = Saturday,
        Sunday = Sunday).where(Prescription.prescriptionid == details['prescriptionid'])

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
    try: 
        prescription = Prescription.select().where(Prescription.prescriptionid == request.form['prescriptionid']).get()
    except Prescription.DoesNotExist:
        return "Failed"
    patient = prescription.username.username
    username = getUsernameFromHeader()
    if verifyContentRequest(username, patient):
        return deletePrescription(request.form['prescriptionid'])

def deletePrescription(prescriptionid):
    """
    Deletes a specified prescriptions.

    :link: /api/deletePrescription

    :param prescriptionid: The id of the prescription to delete.
    :type prescriptionid: int.

    :returns: str -- 'Deleted' or 'Failed'.
    """
    try:
        instance = Prescription.select().where(Prescription.prescriptionid == prescriptionid).get()
    except Prescription.DoesNotExist:
        return "Failed"
    with database.transaction():
        instance.delete_instance(recursive=True)
        return "Deleted"
    return "Failed"


@app.route('/api/getPrescriptions', methods=['POST'])
@auth.login_required
def getPrescriptions():
    getAccountType = json.loads(getAccountInfo(getUsernameFromHeader()))['accounttype']
    if getAccountType == "Carer":
        if verifyContentRequest(getUsernameFromHeader(), request.form['username']):
            return getPrescriptions(request.form['username'])
    elif getAccountType == "Patient":
        if verifyContentRequest(request.form['username'], ""):
            return getPrescriptions(request.form['username'])

def getPrescriptions(username):
    """
    Returns all (active, upcoming and expired) prescriptions for a specified user.

    :link: /api/getPrescriptions

    :param username: The user to check for.
    :type username: str.

    :returns: json -- The list of prescriptions.
    """
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

#UpToHere
@app.route('/api/getActivePrescriptions', methods=['POST'])
@auth.login_required
def getActivePrescriptions():
    getAccountType = json.loads(getAccountInfo(getUsernameFromHeader()))['accounttype']
    if getAccountType == "Carer":
        if verifyContentRequest(getUsernameFromHeader(), request.form['username']):
            return getActivePrescriptions(request.form['username'])
    elif getAccountType == "Patient":
        if verifyContentRequest(request.form['username'], ""):
            return getActivePrescriptions(request.form['username'])

def getActivePrescriptions(username):
    """
    Returns all active prescriptions for a specified user.

    :link: /api/getActivePrescriptions

    :param username: The specified user.
    :type username: str.

    :returns: json -- List of prescriptions.
    """
    allPrescriptions = json.loads(getPrescriptions(username))
    return json.dumps([prescription for prescription in allPrescriptions if (datetime.datetime.strptime(prescription['startdate'], "%Y-%m-%d") < datetime.datetime.now() and datetime.datetime.strptime(prescription['enddate'], "%Y-%m-%d") > datetime.datetime.now())])

@app.route('/api/getUpcomingPrescriptions', methods=['POST'])
@auth.login_required
def getUpcomingPrescriptions():
    getAccountType = json.loads(getAccountInfo(getUsernameFromHeader()))['accounttype']
    if getAccountType == "Carer":
        if verifyContentRequest(getUsernameFromHeader(), request.form['username']):
            return getUpcomingPrescriptions(request.form['username'])
    elif getAccountType == "Patient":
        if verifyContentRequest(request.form['username'], ""):
            return getUpcomingPrescriptions(request.form['username'])

def getUpcomingPrescriptions(username):
    """
    Returns all upcoming prescriptions for a specified user.

    :link: /api/getUpcomingPrescriptions

    :param username: The username to check for.
    :type username: str.

    :returns: json -- List of prescriptions.
    """
    allPrescriptions = json.loads(getPrescriptions(username))
    return json.dumps([prescription for prescription in allPrescriptions if (datetime.datetime.strptime(prescription['startdate'], "%Y-%m-%d") >= datetime.datetime.now())])

@app.route('/api/getExpiredPrescriptions', methods=['POST'])
@auth.login_required
def getExpiredPrescriptions():
    getAccountType = json.loads(getAccountInfo(getUsernameFromHeader()))['accounttype']
    if getAccountType == "Carer":
        if verifyContentRequest(getUsernameFromHeader(), request.form['username']):
            return getExpiredPrescriptions(request.form['username'])
    elif getAccountType == "Patient":
        if verifyContentRequest(request.form['username'], ""):
            return getExpiredPrescriptions(request.form['username'])

def getExpiredPrescriptions(username):
    """
    Returns all expired prescriptions for a specified user.

    :link: /api/getExpiredPrescriptions

    :param username: The username to check for.
    :type username: str.

    :returns: json -- List of expired prescriptions.
    """
    allPrescriptions = json.loads(getPrescriptions(username))
    return json.dumps([prescription for prescription in allPrescriptions if (datetime.datetime.strptime(prescription['enddate'], "%Y-%m-%d") < datetime.datetime.now())])

@app.route('/api/getPrescription', methods=['POST'])
@auth.login_required
def getPrescription():
    getAccountType = json.loads(getAccountInfo(getUsernameFromHeader()))['accounttype']
    if getAccountType == "Carer":
        if verifyContentRequest(getUsernameFromHeader(), request.form['username']):
            return getExpiredPrescriptions(request.form['username'])
    elif getAccountType == "Patient":
        if verifyContentRequest(request.form['username'], ""):
            return getPrescription(request.form)

def getPrescription(details):
    """
    Returns the details of a specified prescription.

    :link: /api/getPrescription

    :param details: Dictionary containing [prescriptionid].
    :type details: dict.

    :returns: json -- Details of prescription.
    """
    prescriptionid = details['prescriptionid']
    prescription = Prescription.select().where(Prescription.prescriptionid == prescriptionid).dicts().get()
    prescription['startdate'] = str(prescription['startdate'])
    prescription['enddate'] = str(prescription['enddate'])
    return json.dumps(prescription)

@app.route('/api/takeprescription', methods=['POST'])
def takePrescription():
    prescriptionid = request.form['prescriptionid']
    try:
        prescription = Prescription.select().dicts().where(Prescription.prescriptionid == prescriptionid).get()
        user = prescription['username']
        if verifyContentRequest(user, ""):
            return takePrescription(request.form)
    except Prescription.DoesNotExist:
        return "Specified prescription does not exist"

def takePrescription(details):
    """
    Allows a prescription to be taken.

    :link: /api/takeprescription

    :param details: Dictionary containing [currentcount] (number taken today), [prescriptionid].
    :type details: dict.

    :returns: True for success or 'Invalid current count'
    """
    try:
        prescription = Prescription.get(Prescription.prescriptionid == details['prescriptionid'])
    except Prescription.DoesNotExist:
        return "Specified prescription does not exist"

    try:
        currentCount = int(details['currentcount'])
        # If a record already exists for this day, update
        takeInstance = TakePrescription.select().where((TakePrescription.prescriptionid == details['prescriptionid']) & (TakePrescription.currentdate == datetime.datetime.now().date())).get()
        takeInstance = TakePrescription.update(
            currentcount = currentCount
        ).where(
            (TakePrescription.prescriptionid == details['prescriptionid']) &
            (TakePrescription.currentdate == datetime.datetime.now().date())
        )
        with database.transaction():
            takeInstance.execute()
            checkStockLevel(details['prescriptionid'], currentCount)
            return "True"
    except TakePrescription.DoesNotExist:
        # No record exists for today, create a new one
        takeInstance = TakePrescription.insert(
            prescriptionid = details['prescriptionid'],
            currentcount = details['currentcount'],
            startingcount = prescription.stockleft,
            currentdate = datetime.datetime.now().date())
        with database.transaction():
            takeInstance.execute()
            checkStockLevel(details['prescriptionid'], currentCount)
            return "True"
    except TypeError:
        return "Invalid current count (is it an integer?)"
    return "False"

def checkStockLevel(prescription, count):
    """
    Returns the stock level of a prescription after taking.
    Creates a notification is appropriate.

    :param prescription: The id of the prescription.
    :type prescription: int.

    :param count: The amount just taken.
    :type count: int.
    """
    thisPrescription = Prescription.get(Prescription.prescriptionid == prescription)
    takeInstance = TakePrescription.select().where(
        (TakePrescription.prescriptionid == prescription) &
        (TakePrescription.currentdate == datetime.datetime.now().date())
    ).get()

    # Level to decrease stock by is number of times taken today * number of tablets etc. taken each time
    levelToDecrease = (count * thisPrescription.quantity)

    # If they have increased their stock, reflect that change
    if thisPrescription.stockleft > takeInstance.startingcount:
        takeInstance.startingcount = thisPrescription.stockleft

    # Remove the amount taken today from stock
    thisPrescription.stockleft = (takeInstance.startingcount - levelToDecrease)

    # Commit all changes
    thisPrescription.save()

    # Do they have 3 days worth?
    if (thisPrescription.stockleft < ((thisPrescription.frequency * thisPrescription.quantity)*3)):
        patient = thisPrescription.username
        carer = Patientcarer.get(Patientcarer.patient == patient).carer
        # Has the patient currently been alerted?
        try:
            n = Notification.select().where(
                    Notification.username == patient.username,
                    Notification.notificationtype == "Medication Low",
                    Notification.relatedObject == thisPrescription.prescriptionid,
                    Notification.dismissed == False,
                    Notification.relatedObjectTable == "Prescription"
                ).get()
        except Notification.DoesNotExist:
            createNotificationRecord(patient.username, "Medication Low", thisPrescription.prescriptionid)

        try:
            n = Notification.select().where(
                    Notification.username == carer.username,
                    Notification.notificationtype == "Patient Medication Low",
                    Notification.relatedObject == thisPrescription.prescriptionid,
                    Notification.dismissed == False,
                    Notification.relatedObjectTable == "Prescription"
                ).get()
        except Notification.DoesNotExist:
            createNotificationRecord(carer.username, "Patient Medication Low", thisPrescription.prescriptionid)

@app.route('/api/getPrescriptionCount', methods=['POST'])
def getPrescriptionCount():
    prescriptionid = request.form['prescriptionid']
    try:
        prescription = Prescription.select().where(Prescription.prescriptionid == prescriptionid).dicts().get()
    except Prescription.DoesNotExist:
        return "Prescription does not exist"
    user = prescription['username']
    if verifyContentRequest(user, ""):
        return getPrescriptionCount(request.form)

def getPrescriptionCount(details):
    """
    Returns the number of times a user has taken a prescription on the current day.

    :link: /api/getPrescriptionCount

    :param details: Dictionary containing [prescriptionid].
    :type details: dict.

    :returns: int -- The count.
    """
    try:
        takeInstance = TakePrescription.select().where(
                (TakePrescription.prescriptionid == details['prescriptionid']) &
                (TakePrescription.currentdate == datetime.datetime.now().date())) \
            .get()
        return str(takeInstance.currentcount)
    except TakePrescription.DoesNotExist:
        return str(0)

@app.route('/api/searchNHSDirectWebsite', methods=['POST'])
@auth.login_required
def searchNHSDirect():
    return searchNHSDirect(request.form['searchterms'])

def searchNHSDirect(search):
    """
    Allows a search term to be passed to the NHS website.

    :link: /api/searchNHSDirectWebsite

    :param search: The search term.
    :type search: str.

    :returns: str -- The url of the website.
    """
    newTerm = search.replace(" ", "+")
    website = "http://www.nhs.uk/Search/Pages/Results.aspx?___JSSniffer=true&q="
    searchWeb = website + newTerm
    return searchWeb

@app.route('/api/getDeactivateReasons', methods=['POST','GET'])
@auth.login_required
def getDeactivateReasons():
    return getDeactivateReasons()

def getDeactivateReasons():
    """
    Returns a list of possible reasons a user can deactivate

    :link: /api/getDeactivateReasons

    :returns: json -- List of possible reasons.
    """
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
    """
    Returns a list of possible appointment types

    :link: /api/getAppointmentTypes

    :returns: json -- List of appointment types
    """
    types = Appointmenttype.select()
    typeList = []
    for appType in types:
      typeList.append(appType.type)
    typeList = json.dumps(typeList)
    return typeList

@app.route('/api/getCorrespondence', methods=['GET', 'POST'])
@auth.login_required
def getCorrespondence():
    if verifyContentRequest(request.form['carer'], request.form['patient']):
        return getCorrespondence(request.form['carer'], request.form['patient'])

def getCorrespondence(carer, patient):
    """
    Returns all notes for a patient/carer relationship.

    :link: /api/getCorrespondence

    :param carer: The username of the carer.
    :type carer: str.

    :param patient: The username of the patient.
    :type patient: str.

    :returns: json -- List of notes.
    """
    allNotes = Notes.select().where((Notes.carer == carer) & (Notes.patient == patient))

    results = []
    for n in allNotes:
        note = {}
        note['noteid'] = n.noteid
        note['carer'] = n.carer.username
        note['patient'] = n.patient.username
        note['notes'] = n.notes
        note['title'] = n.title
        note['datetime'] = str(n.datetime)
        results.append(note)
    return json.dumps(results)

@app.route('/api/getPatientNotes', methods=['GET', 'POST'])
@auth.login_required
def getPatientNotes():
    if verifyContentRequest(request.form['username'], ""):
        return getPatientNotes(request.form)

def getPatientNotes(details):
    """
    Returns all notes for a specific patient.

    :link: getPatientNotes

    :param details: Dictionary containing [username] of target patient.
    :type details: dict.

    :returns: json -- List of notes
    """
    allNotes = Notes.select().where(Notes.patient == details['username'])

    results = []
    for n in allNotes:
        note = {}
        note['noteid'] = n.noteid
        note['carer'] = n.carer.username
        note['patient'] = n.patient.username
        note['notes'] = n.notes
        note['title'] = n.title
        note['datetime'] = str(n.datetime)
        results.append(note)
    return json.dumps(results)

@app.route('/api/addCorrespondence', methods=['POST'])
def addCorrespondence():
    if verifyContentRequest(request.form['carer'], request.form['patient']):
        return addCorrespondence(request.form)

def addCorrespondence(details):
    """
    Adds a note for a patient.

    :link: /api/addCorrespondence

    :param details: Dictionary containing [carer], [patient], [notes] (note content), [title].
    :type details: dict.

    :returns: str -- True or False for success.
    """
    insert = Notes.insert(
        carer = details['carer'],
        patient = details['patient'],
        notes = details['notes'],
        title = details['title'],
        datetime = datetime.datetime.now()
    )

    with database.transaction():
        insert.execute()
        return "True"
    return "False"

@app.route('/api/deleteNote', methods=['POST'])
@auth.login_required
def deleteNote():
    noteid = request.form['noteid']
    try:
        note = Notes.select().where(Notes.noteid == noteid).get()
        patient = note.patient.username
        if verifyContentRequest(getUsernameFromHeader(), patient):
            return deleteNote(noteid)
    except Notes.DoesNotExist:
        return "Failed"    

def deleteNote(noteid):
    """
    Delete a specific note

    :link: /api/deleteNote

    :param noteid: The id of the note to delete.
    :type noteid: int.

    :returns: str - Either 'Deleted' or 'Failed'.
    """
    try:
        instance = Notes.select().where(Notes.noteid == noteid).get()
        with database.transaction():
            instance.delete_instance()
            return "Deleted"
    except Notes.DoesNotExist:
        return "Failed"

@app.route('/api/addAndroidEventId', methods=['POST'])
@auth.login_required
def addAndroidEventId():
    """
    Allows an android event id of a calendar event to be stored.

    :link: /api/addAndroidEventId

    :param request.form: POST request containing [dbid](id of event) and [androidid](the android event id).
    :type request.form: dict.

    :returns: str -- Success message
    """
    dbId = request.form['dbid']
    androidId = request.form['androidid']
    addAndroidId = Appointments.update(androideventid=androidId).where(Appointments.appid==dbId).execute()
    return "Android ID added to database"

##
#Admin Portal Pages
##
def addDeactivate(reason):
    """
    Allows a new add deactivate reasons to be added to the database.

    :param reason: The reason to add.
    :type reason: str.

    :returns: str -- True or False for success.
    """
    insert = Deactivatereason.insert(
        reason = request.form['reason']
    )

    with database.transaction():
        insert.execute()
        return "True"
    return "False"

def newMedication(medication):
    """
    Allows a new medication to be inserted into the database.

    :param medication: The name of the medication to add.
    :type medication: str.

    :returns: str -- True or False.
    """
    insert = Medication.insert(
        name = request.form['medication']
    )

    with database.transaction():
        insert.execute()
        return "True"
    return "False"

@app.route('/api/getReasons', methods=['GET', 'POST'])
@auth.login_required
def getReasons():
    return getReasons()

def getReasons():
    """
    Returns all pre-set reasons to deactivate.

    :link: /api/getReasons

    :returns: json -- List of reasons.
    """
    result = {}
    a = Userdeactivatereason.select()
    reasons = Userdeactivatereason.select(Userdeactivatereason.reason).distinct()
    for reason in reasons:
      result[reason.reason.reason] = a.select().where(Userdeactivatereason.reason == reason.reason).count()
    return json.dumps(result)

def getAllUsers():
    """
    Returns information about all users.

    :returns: json -- List containing dictionaries representing all users.
    """
    results = []
    for u in Client.select(Client.username):
        userDetails = {}
        try:
            user = Admin.select().join(Client).where(Client.username==u.username).get()
            userDetails['accounttype'] = "Admin"
        except Admin.DoesNotExist:
            try:
                user = Carer.select().join(Client).where(Client.username==u.username).get()
                userDetails['accounttype'] = "Carer"
            except Carer.DoesNotExist:
                user = Patient.select().join(Client).where(Client.username==u.username).get()
                userDetails['accounttype'] = "Patient"

            userDetails['firstname'] = user.firstname
            userDetails['surname'] = user.surname
            userDetails['username'] = user.username.username
            userDetails['email'] = user.username.email
            userDetails['dob'] = str(user.username.dob)
            userDetails['accountdeactivated'] = user.username.accountdeactivated
            userDetails['accountlocked'] = user.username.accountlocked
            userDetails['loginattempts'] = user.username.loginattempts
            userDetails['verified'] = user.username.verified
            if user.ismale:
                userDetails['gender'] = 'Male'
            else:
                userDetails['gender'] ='Female'
            results.append(userDetails)
    return json.dumps(results)

#Update user account settings in Admin Portal
def updateAccountSettings(settings, accountlocked, accountdeactivated, verified):
    """
    Allows an admin to alter a user's account settings.

    :param settings: Dictionary of users settings [username, ismale, firstname, surname, email, dob,
                    accounttype, loginattempts].
    :type settings: dict.

    :param accountlocked: Whether the account should be locked or not.
    :type accountlocked: boolean.

    :param verified: Whether the account is verified.
    :type verified: boolean.
    """
    user = None
    # What type of user are we dealing with?
    try:
        user = Admin.select().join(Client).where(Client.username==settings['username']).get()
    except Admin.DoesNotExist:
        try:
            user = Carer.select().join(Client).where(Client.username==settings['username']).get()
        except Carer.DoesNotExist:
            user = Patient.select().join(Client).where(Client.username==settings['username']).get()

    # Access to their corresponding Client entry
    clientObject = Client.select().where(Client.username == user.username).get()

    gender = False
    if settings['ismale'] == "true":
        gender = True

    # Update
    user.firstname = settings['firstname']
    user.surname = settings['surname']
    user.ismale = gender

    clientObject.username = settings['username']
    clientObject.email = settings['email']
    clientObject.dob = settings['dob']
    clientObject.accounttype = settings['accounttype']
    clientObject.accountdeactivated = accountdeactivated
    clientObject.accountlocked = accountlocked
    clientObject.loginattempts = settings['loginattempts']
    clientObject.verified = verified

    with database.transaction():
        user.save()
        clientObject.save()
        return "True"
    return "False"

def deleteAccount(username):
    """
    Deletes a user's account.

    :param username: The username who's account should be deleted.
    :type username: str.

    :returns: str -- 'Deleted' if successful, else 'Failed'.
    """
    try:
        instance = Client.select().where(Client.username == username).get()
    except:
        return "Failed"
    with database.transaction():
        instance.delete_instance(recursive=True)
        return "Deleted"
    return "Failed"

def createNotificationRecord(user, notificationType, relatedObject):
    """
    Creates a notification on the JustHealth platform.

    :param user: The user the notification belongs to.
    :type user: str.

    :param notificationType: The type of notification to be created
    :type notificationType: str.

    :param relatedObject: The resource a notification pertains to, if any.
    :type relatedObject: int.

    :returns: str -- 'True' if successful, else 'False'
    """
    # Dictionary mapping notificationType to referencing table
    notificationTypeTable = {}
    notificationTypeTable['Connection Request'] = "Relationship"
    notificationTypeTable['New Connection'] = ""
    notificationTypeTable['Prescription Added'] = "Prescription"
    notificationTypeTable['Prescription Updated'] = "Prescription"
    notificationTypeTable['Appointment Invite'] = "Appointments"
    notificationTypeTable['Appointment Updated'] = "Appointments"
    notificationTypeTable['Appointment Cancelled'] = ""
    notificationTypeTable['Password Reset'] = ""
    notificationTypeTable['Appointment Declined'] = "Appointments"
    notificationTypeTable['Appointment Accepted'] = "Appointments"
    notificationTypeTable['Patient Medication Low'] = "Prescription"
    notificationTypeTable['Medication Low'] = "Prescription"
    notificationTypeTable['Missed Prescription'] = "TakePrescription"
    notificationTypeTable['Carer Missed Prescription'] = "TakePrescription"

    try:
        createNotification = Notification.insert(
            username = user,
            notificationtype = notificationType,
            relatedObjectTable = notificationTypeTable[notificationType],
            relatedObject = relatedObject
        )
    except KeyError, e:
        return "Invalid Notification Type"

    with database.transaction():
        notificationId = str(createNotification.execute())
        createPushNotification(notificationId)
        return "True"
    return "False"

@app.route('/api/getNotifications', methods=['POST'])
@auth.login_required
def getNotifications():
    if verifyContentRequest(request.form['username'], ""):
        return getNotifications(request.form['username'])

def getNotifications(username):
    """
    Returns all of the notifications that have been associated with a user that have not been dismissed. 

    :link: /api/getNotifications

    :param username: The username to get dismissed notifications for.
    :type username: str.

    :returns: json -- The list of notifications each as a json dictionary.
    """
    notifications = Notification.select().dicts().where((Notification.username == username) & (Notification.dismissed == False))    
    notificationList = []
    for notification in notifications:
        notification['content'] = getNotificationContent(notification)
        notification['link'] = getNotificationLink(notification)
        notification['type'] = getNotificationTypeClass(notification)
        if (notification['content'] != "DoesNotExist"):
            notificationList.append(notification)

    return json.dumps(notificationList)

@app.route('/api/getAllNotifications', methods=['POST'])
@auth.login_required
def getAllNotifications():
    if verifyContentRequest(request.form['username'], ""):
        return getAllNotifications(request.form['username'])

def getAllNotifications(username):
    """
    Returns all of the notifications that have been associated with a user, whether or not they have been dismissed

    :link: /api/getAllNotifications

    :param username: The username to get dismissed notifications for.
    :type username: str.

    :returns: json -- The list of notifications each as a json dictionary.
    """
    notifications = Notification.select().dicts().where(Notification.username == username)
    notificationList = []
    for notification in notifications:
        notification['content'] = getNotificationContent(notification)
        notification['link'] = getNotificationLink(notification)
        notification['type'] = getNotificationTypeClass(notification)
        if (notification['content'] != "DoesNotExist"):
            notificationList.append(notification)

    return json.dumps(notificationList)

@app.route('/api/getDismissedNotifications', methods=['POST'])
@auth.login_required
def getDismissedNotifications():
    if verifyContentRequest(request.form['username'], ""):
        return getDismissedNotifications(request.form['username'])

def getDismissedNotifications(username):
    """
    Returns all of the notifications that have been dismissed for a username

    :link: /api/getDismissedNotifications

    :param username: The username to get dismissed notifications for.
    :type username: str.

    :returns: json -- The list of notifications each as a json dictionary.
    """
    notifications = Notification.select().dicts().where((Notification.username == username) & (Notification.dismissed == True))
    notificationList = []
    for notification in notifications:
        notification['content'] = getNotificationContent(notification)
        notification['link'] = getNotificationLink(notification)
        notification['type'] = getNotificationTypeClass(notification)
        if (notification['content'] != "DoesNotExist"):
            notificationList.append(notification)

    return json.dumps(notificationList)

def getNotificationContent(notification):
    """
    Gets the body/content of the notification depending on its type.

    :param notification: Dictionary containing [notificationtype] element listing the type being queried.
    :type notification: dict.

    :returns: str -- The content of the notification or 'DoesNotExist' if the queried object no longer exists.
    """
    if notification['notificationtype'] == "Connection Request":
        try:
            requestor = Relationship.select().where(Relationship.connectionid == notification['relatedObject']).get()
        except:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = "You have a new connection request from " + requestor.requestor.username

    if notification['notificationtype'] == "New Connection":
        content = "You have a new connection, click above to view."

    if notification['notificationtype'] == "Prescription Added":
        try:
            prescription = Prescription.select().where(Prescription.prescriptionid == notification['relatedObject']).get()
        except:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = "A new prescription for " + prescription.medication.name + " has been added to your profile."

    if notification['notificationtype'] == "Prescription Updated":
        try:
            prescription = Prescription.select().where(Prescription.prescriptionid == notification['relatedObject']).get()
        except:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = "Your prescription for " + prescription.medication.name + " has been updated."

    if notification['notificationtype'] == "Appointment Invite":
        try:
            appointment = Appointments.select().where(Appointments.appid == notification['relatedObject']).get()
        except:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = appointment.creator.username + " has added an appointment with you on " + str(appointment.startdate) + ". Click the link to accept/decline."

    if notification['notificationtype'] == "Appointment Updated":
        try:
            appointment = Appointments.select().where(Appointments.appid == notification['relatedObject']).get()
        except:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = appointment.creator.username + " has updated the following appointment with you: " + str(appointment.name) + ". Click the link to accept/decline."

    if notification['notificationtype'] == "Appointment Cancelled":
        content = "One of your appointments has been cancelled, click above to view your updated calendar."

    if notification['notificationtype'] == "Password Reset":
        content = "Your password has been changed successfully."

    if notification['notificationtype'] == "Appointment Accepted":
        try:
            appointment = Appointments.select().where(Appointments.appid == notification['relatedObject']).get()
        except:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = appointment.invitee.username + " has accepted the appointment with you on " + str(appointment.startdate) + "."

    if notification['notificationtype'] == "Appointment Declined":
        try:
            appointment = Appointments.select().where(Appointments.appid == notification['relatedObject']).get()
        except:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = appointment.invitee.username + " has declined the appointment with you on " + str(appointment.startdate) + "."

    if notification['notificationtype'] == "Medication Low":
        try:
            prescription = Prescription.select().where(Prescription.prescriptionid == notification['relatedObject']).get()
        except:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = "You have less than 3 days stock of " + prescription.medication.name + " left."

    if notification['notificationtype'] == "Patient Medication Low":
        try:
            prescription = Prescription.select().where(Prescription.prescriptionid == notification['relatedObject']).get()
        except:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = prescription.username.username + " has less than 3 days stock of " + prescription.medication.name + " left."

    if notification['notificationtype'] == "Missed Prescription":
        try:
            takeInstance = TakePrescription.select().where(TakePrescription.takeid == notification['relatedObject']).get()
            prescription = Prescription.select().where(Prescription.prescriptionid == takeInstance.prescriptionid).get()
        except:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = "You only took " + str(takeInstance.currentcount) + " out of " + str(prescription.frequency) + \
                    " of " + str(prescription.medication.name) + " " + prescription.dosageform + "(s) " + \
                    " on " + str(takeInstance.currentdate)

    if notification['notificationtype'] == "Carer Missed Prescription":
        try:
            takeInstance = TakePrescription.select().where(TakePrescription.takeid == notification['relatedObject']).get()
            prescription = Prescription.select().where(Prescription.prescriptionid == takeInstance.prescriptionid).get()
        except:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = "Your patient " + str(prescription.username.username) + \
                    " only took " + str(takeInstance.currentcount) + " out of " + str(prescription.frequency) + \
                    " of " + str(prescription.medication.name) + " " + prescription.dosageform + "(s) " + \
                    " on " + str(takeInstance.currentdate)

    return content

def getNotificationLink(notification):
    """
    Returns the link that a specific notification type will link to for web usage.

    :param notification: Dictionary containing [notificationtype] element listing the type being queried.
    :type notification: dict.

    :returns: str -- The web address of the notification subject for JustHealth Web Application.
    """
    if notification['notificationtype'] == "Connection Request":
        link = "/?go=connections"

    if notification['notificationtype'] == "New Connection":
        link = "/?go=connections"

    if notification['notificationtype'] == "Prescription Added":
        link = "/prescriptions"

    if notification['notificationtype'] == "Prescription Updated":
        link = "/prescriptions"

    if notification['notificationtype'] == "Appointment Invite":
        link = "/appointmentDetails?id=" + str(notification['relatedObject'])

    if notification['notificationtype'] == "Appointment Updated":
        link = "/appointmentDetails?id=" + str(notification['relatedObject'])

    if notification['notificationtype'] == "Appointment Cancelled":
        link = "/appointments"

    if notification['notificationtype'] == "Appointment Accepted":
        link = "/appointments?open=" + str(notification['relatedObject'])

    if notification['notificationtype'] == "Appointment Declined":
        link = "/appointments?open=" + str(notification['relatedObject'])

    if notification['notificationtype'] == "Password Reset":
        link = "/"

    if notification['notificationtype'] == "Medication Low":
        link = "/prescriptions"

    if notification['notificationtype'] == "Patient Medication Low":
        link = "/"

    if notification['notificationtype'] == "Missed Prescription":
        link = "/"

    if notification['notificationtype'] == "Carer Missed Prescription":
        link = "/"

    return link

def getNotificationTypeClass(notification):
    """
    Returns the 'class' of a notification type, used to identify importance / meaning.

    :param notification: Dictionary containing [notificationtype] element listing the type being queried.
    :type notification: dict.

    :returns: str -- One of 'danger', 'warning', 'success', 'info'.
    """
    notificationClass = Notificationtype.select().where(Notificationtype.typename == notification['notificationtype']).get()
    return notificationClass.typeclass

@app.route('/api/dismissNotification', methods=['POST'])
@auth.login_required
def dismissNotification():
    try: 
        notification = Notification.select().dicts().where(Notification.notificationid == request.form['notificationid']).get()
    except Notification.DoesNotExist:
        return "Notification Does Not Exist"
    user = notification['username']
    if verifyContentRequest(user, ""):
        return dismissNotification(request.form['notificationid'])

def dismissNotification(notificationid):
    """
    Dismisses a notification to hide from the user's immediate view.

    :link: /api/dismissNotification

    :param notificationid: The id of the notification to dismiss.
    :type notificationid: int.

    :returns: str -- 'True' if successful, 'False' if not.
    """
    try:
        dismiss = Notification.update(dismissed=True).where(Notification.notificationid == notificationid)
    except Notification.DoesNotExist:
        return "Notification Does Not Exist"

    with database.transaction():
        dismiss.execute()
        return "True"
    return "False"

##
# Reminder Functionality
##

def getMinutesDifference(dateTimeOne,dateTimeTwo):
    """
    Returns the difference found by dateTimeOne - dateTimeTwo in minutes.

    :param dateTimeOne: The first datetime.
    :type dateTimeOne: datetime.

    :param dateTimeTwo: The second datetime.
    :type dateTimeTwo: datetime.

    :returns: int -- The number of minutes between the two times.
    """
    return int((dateTimeOne - dateTimeTwo).total_seconds()/60)

def getAppointmentsDueIn30(username, currentTime):
    """
    Returns a list of appointments that are due in 30 minutes or less.

    :param username: The username to check for.
    :type username: str.

    :param currentTime: The current datetime.
    :type currentTime: datetime.

    :returns: list -- A list of appointments represented by dicts.
    """
    select = Appointments.select().dicts().where((Appointments.creator == username) | (Appointments.invitee == username))
    result = []
    for appointment in select:
        appointmentStartTime = datetime.datetime.combine(appointment['startdate'], appointment['starttime'])
        timeUntil = getMinutesDifference(appointmentStartTime, currentTime)
        if timeUntil <= 30 and timeUntil > 0:
            result.append(appointment)
    return result

def getAppointmentsDueNow(username, currentTime):
    """
    Returns a list of appointments that are due now or are in progress.

    :param username: The username to check for.
    :type username: str.

    :param currentTime: The current datetime.
    :type currentTime: datetime.

    :returns: list -- A list of appointments represented by dicts.
    """
    select = Appointments.select().dicts().where((Appointments.creator == username) | (Appointments.invitee == username))
    result = []
    for appointment in select:
        appointmentStartTime = datetime.datetime.combine(appointment['startdate'], appointment['starttime'])
        timeUntilStart = getMinutesDifference(appointmentStartTime, currentTime)
        appointmentEndTime = datetime.datetime.combine(appointment['enddate'], appointment['endtime'])
        timeUntilEnd = getMinutesDifference(appointmentEndTime, currentTime)
        if timeUntilStart <= 0 and timeUntilEnd > 0:
            result.append(appointment)
    return result

def getPrescriptionsDueToday(username, currentDateTime):
    """
    Returns a list of prescriptions that are due today.

    :param username: The username to check for.
    :type username: str.

    :param currentDateTime: The current datetime.
    :type currentDateTime: datetime.

    :returns: list -- A list of prescriptions represented by dicts.
    """
    currentDate = currentDateTime.date()
    currentDay = currentDateTime.strftime("%A")

    activePrescriptions = Prescription.select().where(
        (Prescription.username == username) &
        (Prescription.startdate <= currentDate) &
        (Prescription.enddate >= currentDate) &
        (eval("Prescription." + currentDay) == True)
    ).dicts()

    results = []
    for r in activePrescriptions:
        results.append(r)
    return results

def checkMissedPrescriptions(username, currentDate):
    """
    Checks to see if a patient has missed any prescriptions
    and creates notifications if so.

    :param username: The username to check for.
    :type username: str.

    :param currentDate: The current datetime.
    :type currentDate: datetime.
    """
    listOfPrescriptions = Prescription.select().where(Prescription.username == username)
    for x in listOfPrescriptions:
        takeInstance = TakePrescription.select().where(TakePrescription.prescriptionid == x)
        for i in takeInstance:
            if (i.currentdate < currentDate) and (i.currentcount < x.frequency):
                # Does notification already exist?
                try:
                    Notification.select().where(
                        (Notification.notificationtype == "Missed Prescription") &
                        (Notification.relatedObject == i.takeid)
                    ).get()
                except Notification.DoesNotExist:
                    createNotificationRecord(username, "Missed Prescription", i.takeid)
                    for carer in getCarers(username):
                        createNotificationRecord(carer, "Carer Missed Prescription", i.takeid)

def createTakePrescriptionInstances(username, currentDateTime):
    """
    Creates all TakePrescription instances for any prescription that needs to be taken today.

    :param username: The username to check for.
    :type username: str.

    :param currentDateTime: The current datetime.
    :type currentDateTime: datetime.
    """
    listOfPrescriptions = Prescription.select().where(Prescription.username == username)
    currentDay = currentDateTime.strftime("%A")
    for p in listOfPrescriptions:
        dateField = eval("p." + currentDay)
        if (dateField == True) and (p.startdate <= currentDateTime.date()):
            try:
                TakePrescription.select().where(
                    (TakePrescription.prescriptionid == p.prescriptionid) &
                    (TakePrescription.currentdate == currentDateTime.date())
                ).get()
            except TakePrescription.DoesNotExist:
                content = "You are due to take " + str(p.quantity) + " " + str(p.dosageform) + "(s) of " + p.medication.name + " " + str(p.frequency) + " time(s) today."
                sendPushNotification(username, "Prescription Due Today", content)
                with database.transaction():
                    insert = TakePrescription.insert(
                                prescriptionid = p.prescriptionid,
                                currentcount = 0,
                                startingcount = p.stockleft,
                                currentdate = currentDateTime.date())
                    takePrescriptionId = insert.execute()

def pingServer(sender, **extra):
    """
    Checks to see if there are any reminders to create/delete, runs on every request.

    Also called by a scheduled task for all users. See :func:`generation`.
    """
    try:
        loggedInUser = session['username']
        dt = datetime.datetime.now()

        deleteReminders(loggedInUser, dt)

        if (len(getAppointmentsDueIn30(loggedInUser, dt)) != 0) or (len(getAppointmentsDueNow(loggedInUser, dt)) != 0) or (len(getPrescriptionsDueToday(loggedInUser, dt)) != 0):
            addReminders(loggedInUser, dt)

        createTakePrescriptionInstances(loggedInUser, dt)
        checkMissedPrescriptions(loggedInUser, dt.date())

    # No-one logged in
    except KeyError, e:
        return

def addReminders(username, now):
    """
    Add all new reminders to the Reminder table.

    :param username: The username to add reminders for.
    :type username: str.

    :param now: The current datetime.
    :type now: datetime.
    """
    # Get All Reminders (Saving on performance hits later)
    allReminders = Reminder.select().where(Reminder.username == username)

    appointmentsDueIn30 = getAppointmentsDueIn30(username, now)
    for a in appointmentsDueIn30:
        withUser = a['creator']
        if withUser == username:
            withUser = a['invitee']

        try:
            r = allReminders.select().where((Reminder.relatedObjectTable == 'Appointments') & (Reminder.relatedObject == a['appid'])).get()
            if r.reminderClass == "danger":
                with database.transaction():
                    r.delete_instance()
                raise Reminder.DoesNotExist
        except Reminder.DoesNotExist:

            # Is the appointment with another user?
            if withUser == None:
                insertContent = "Your " + a['apptype'] + " appointment starts at " + str(a['starttime'])
            else:
                insertContent = "Your " + a['apptype'] + " appointment with " + withUser + " starts at " + str(a['starttime'])

            # Create the reminder
            insertReminder = Reminder.insert(
                username = username,
                content = insertContent,
                reminderClass = "warning",
                relatedObjectTable = "Appointments",
                relatedObject = a['appid'],
                extraDate = str(datetime.datetime.combine(a['startdate'], a['starttime']))
            )
            with database.transaction():
                insertReminder.execute()

    appointmentsDueNow = getAppointmentsDueNow(username, now)
    for a in appointmentsDueNow:
        withUser = a['creator']
        if withUser == username:
            withUser = a['invitee']
        try:
            r = allReminders.select().where((Reminder.relatedObjectTable == 'Appointments') & (Reminder.relatedObject == a['appid'])).get()
            if r.reminderClass == "warning":
                with database.transaction():
                    r.delete_instance()
                raise Reminder.DoesNotExist
        except Reminder.DoesNotExist:

            # Is the appointment with another user?
            if withUser == None:
                insertContent = "Your " + a['apptype'] + " appointment starts at " + str(a['starttime'])
            else:
                insertContent = "Your " + a['apptype'] + " appointment with " + withUser + " starts at " + str(a['starttime'])

            # Create the reminder
            insertReminder = Reminder.insert(
                username = username,
                content = insertContent,
                reminderClass = "danger",
                relatedObjectTable = "Appointments",
                relatedObject = a['appid'],
                extraDate = str(datetime.datetime.combine(a['enddate'], a['endtime']))
            )
            with database.transaction():
                insertReminder.execute()

    prescriptionsDueToday = getPrescriptionsDueToday(username, now)
    for p in prescriptionsDueToday:
        try:
            r = allReminders.select().where((Reminder.relatedObjectTable == "Prescription") & (Reminder.relatedObject == p['prescriptionid'])).get()
        except Reminder.DoesNotExist:
            content = "You are due to take " + str(p['quantity']) + " " + str(p['dosageform']) + "(s) of " + p['medication'] + " " + str(p['frequency']) + " time(s) today."

            insertReminder = Reminder.insert(
                username = username,
                content = content,
                reminderClass = "info",
                relatedObjectTable = "Prescription",
                relatedObject = p['prescriptionid'],
                extraFrequency = int(p['frequency']))

            with database.transaction():
                insertReminder.execute()

def deleteReminders(username, now):
    """
    Deletes any reminders for appointments or prescriptions
    that have expired or are no longer current.

    :param username: The username to check.
    :type username: str.

    :param now: The current datetime
    :type now: datetime.
    """
    # Get all Reminders
    allReminders = Reminder.select().where(Reminder.username == username)

    # Appointments
    # Need to remove all reminders that are no longer immediately happening / 15mins.
    appointmentReminders = allReminders.where(Reminder.relatedObjectTable == "Appointments")
    if appointmentReminders.count() !=0:
        allAppointments = Appointments.select().where((Appointments.creator == username) | (Appointments.invitee == username))
        for reminder in appointmentReminders:
            try:
                appointment = allAppointments.select(Appointments.enddate, Appointments.endtime).where(Appointments.appid == reminder.relatedObject).get()
                appointmentEndDateTime = datetime.datetime.combine(appointment.enddate, appointment.endtime)
                if appointmentEndDateTime < now:
                    with database.transaction():
                        reminder.delete_instance()
            except Appointments.DoesNotExist:
                with database.transaction():
                    reminder.delete_instance()

    # Prescriptions
    # Need to remove all prescriptions that are not on the current day or start date > now or end date < now.
    prescriptionReminders = allReminders.where(Reminder.relatedObjectTable == "Prescription")
    if appointmentReminders.count() !=0:
        allPrescriptions = Prescription.select().where(Prescription.username == username)
        currentDay = now.strftime("%A")
        for reminder in prescriptionReminders:
            try:
                prescription = allPrescriptions.select().where(Prescription.prescriptionid == reminder.relatedObject).get()
                if ((eval("prescription." + currentDay) == False) or (Prescription.startdate > now.date()) or (Prescription.enddate < now.date())):
                    with database.transaction():
                        reminder.delete_instance()
            except Prescription.DoesNotExist:
                with database.transaction():
                    reminder.delete_instance()

def getReminders(username):
    """
    Returns all reminders for a specific user.

    :param username: The username to get reminders for.
    :type username: str.
    """
    allReminders = Reminder.select().dicts().where(Reminder.username == username)
    reminders = []
    for r in allReminders:
        reminders.append(r)
    return json.dumps(reminders)

def passwordExpiration(username):
    """
    This checks whether the password that the user is using is about to expire.

    :param username: The username to check password for.
    :type username: str.

    :returns: result -- Whether the password is valid, expiring soon or needs to be reset.
    """
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
    if verifyContentRequest(request.form['username'], ""):
        return expiredResetPassword(request.form)

def expiredResetPassword(request):
    """
    Resets a password that has expired or is expiring.

    :link: /api/expiredResetPassword

    :param request: Dictionary of user and password details [username, newpassword, confirmnewpassword].
    :type request: dict.

    :returns: str -- True if successful, False if not.
    """
    user = request['username']
    if request['confirmnewpassword'] != request['newpassword']:
        return "Unmatched"

    newPassword = sha256_crypt.encrypt(request['newpassword'])

    # Set existing passwords to not current
    notCurrent = uq8LnAWi7D.update(iscurrent = False).where(uq8LnAWi7D.username == user)

    #check its not the same as old passwords - this does not work as passwords hash as something different each time due to the different salt used.
    # oldPasswords = uq8LnAWi7D.select(uq8LnAWi7D.password).dicts().where(uq8LnAWi7D.username == user).order_by(uq8LnAWi7D.expirydate.desc()).limit(5)
    # oldPasswords.execute()
    # for this in oldPasswords:
    #     if newPassword == this:
    #         return "Exists"

    # Build insert password query
    newCredentials = uq8LnAWi7D.insert(
      username = user,
      password = newPassword,
      iscurrent = True,
      expirydate = str(datetime.date.today() + datetime.timedelta(days=90))
    )

    with database.transaction():
        notCurrent.execute()
        newCredentials.execute()

        createNotificationRecord(user, "Password Reset", None)
        return "True"
    return "False"


# def checkPrescriptionLevel(username, activePrescriptions):
#     today = datetime.datetime.now().date()
#     for prescription in activePrescriptions:
#         if(prescription['stockleft'] < 10):
#             if Notification.select().where((Notification.username == username) & (Notification.dismissed == False) & (Notification.notificationtype == "Medication Low") & (Notification.relatedObject == prescription['prescriptionid'])).count() == 0:
#                 createNotificationRecord(username, "Medication Low", prescription['prescriptionid'])

@app.route('/api/generate')
def generation():
    """
    Cleans up all Notifications / Reminders for all users, run via a scheduled task on the server.

    :link: /api/generate

    :returns: str -- The number of reminders created/deleted.
    """
    startReminderCount = Reminder.select().count()
    dt = datetime.datetime.now()
    for user in Client.select():
        deleteReminders(user.username, dt)
        addReminders(user.username, dt)
        createTakePrescriptionInstances(user.username, dt)
        checkMissedPrescriptions(user.username, dt.date())
    endReminderCount = Reminder.select().count()
    return "Generated " + str((startReminderCount - endReminderCount)) + " reminders"

##
# Signalling
##

# Causes the reminder ping to execute every time the server recieves a request.
request_started.connect(pingServer, app)
