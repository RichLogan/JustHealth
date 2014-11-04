from justHealthServer import app
from flask import Flask, render_template, request, session, redirect, url_for, abort
from database import *
import re
from passlib.hash import sha256_crypt
import datetime
import smtplib
from itsdangerous import URLSafeSerializer, BadSignature

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
      return "Username can not be longer then 25 characters"

    if Client.select().where(Client.username == profile['username']).count() != 0:
       return "Username already taken"

    # Validate firstname, surname and email >25
    if len(profile['firstname']) > 100 or len(profile['surname']) > 100 or len(profile['email']) > 100:
      return 'Firstname, surname and email can not be longer then 100 characters'

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
      email = profile['email']
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
        if attempted.verified == False:
            return "Account not verified. Please check your email for instructions"
        elif attempted.accountlocked == True:
            return "Account is locked. Please check your email for instructions"
        else:
            revertAttempts = Client.update(loginattempts = 0).where(Client.username == attempted.username)
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
        incrementAttempts.execute()
        return "Incorrect username/password"
    return "Something went wrong!"

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
# Account Helper Functions
####

def lockAccount(username):
    lockAccount = Client.update(accountlocked = True).where(Client.username == username)
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

def sendUnlockEmail(username):
    # Login to mail server
    server = smtplib.SMTP_SSL('smtp.zoho.com', 465)
    server.login('justhealth@richlogan.co.uk', "justhealth")
    # Build message
    sender = "'JustHealth' <justhealth@richlogan.co.uk>"
    recipient = Client.get(username = username).email
    subject = "JustHealth Accounts Locked"
    message = "Hello, due to a repeated number of incorrect attempts, your password has been locked. Please visit: http://raptor.kent.ac.uk:5000/resetpassword to reset your password."
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
