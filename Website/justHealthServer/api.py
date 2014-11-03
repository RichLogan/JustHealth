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
      profile['iscarer'] = request.form['iscarer']
      profile['email'] = request.form['email']
      profile['password'] = request.form['password']
      profile['confirmpassword'] = request.form['confirmpassword']
    except KeyError, e:
      return "All fields must be filled out"
    try:
      profile['terms'] = request.form['terms']
    except KeyError, e:
      return "Terms and Conditions must be accepted"

    # Validate all input
    for key in profile:
      profile[key] = profile[key].strip()

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
      firstname = profile['firstname'],
      surname = profile['surname'],
      dob = profile['dob'],
      ismale = profile['ismale'],
      iscarer = profile['iscarer'],
      email = profile['email']
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
    userPassword.execute()

    sendVerificationEmail(profile['username'])
    return True

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












def getSerializer(secret_key=None):
    if secret_key is None:
        secret_key = app.secret_key
    return URLSafeSerializer(secret_key)

def sendPasswordResetEmail(username):
  s = getSerializer()
  payload = s.dumps(username)
  verifyLink = url_for('passwordReset', payload=payload, _external=True)

  #Send Link to users email
  server = smtplib.SMTP_SSL('smtp.zoho.com', 465)
  server.login('justhealth@richlogan.co.uk', "justhealth")

  sender = "'JustHealth' <justhealth@richlogan.co.uk>"
  recipient = Client.get(username = username).email
  subject = "JustHealth Password Reset Verification"
  message = "Your password has been reset. Please verify this here: " + str(verifyLink)
  m = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, recipient, subject)
  server.sendmail(sender, recipient, m+message)
  server.quit()

def sendUnlockEmail(username):
    #Send Link to users email
    server = smtplib.SMTP_SSL('smtp.zoho.com', 465)
    server.login('justhealth@richlogan.co.uk', "justhealth")

    sender = "'JustHealth' <justhealth@richlogan.co.uk>"
    recipient = Client.get(username = username).email
    subject = "JustHealth Accounts Locked"
    message = "Hello, due to a repeated number of incorrect attempts, your password has been locked. Please visit: http://raptor.kent.ac.uk:5000/resetpassword to reset your password."
    m = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, recipient, subject)
    server.sendmail(sender, recipient, m+message)
    server.quit()
