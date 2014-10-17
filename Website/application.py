from flask import Flask, render_template, request, session, redirect, url_for, abort
from itsdangerous import URLSafeSerializer, BadSignature
from functools import wraps
from passlib.hash import sha256_crypt
from database import *
import re
import smtplib
import datetime

app = Flask(__name__)

def getSerializer(secret_key=None):
    if secret_key is None:
        secret_key = app.secret_key
    return URLSafeSerializer(secret_key)

def sendVerificationEmail(username):
    s = getSerializer()
    payload = s.dumps(username)
    verifyLink = url_for('verifyUser', payload=payload, _external=True)

    #Send Link to users email
    server = smtplib.SMTP_SSL('smtp.zoho.com', 465)
    server.login('justhealth@richlogan.co.uk', "justhealth")

    sender = "'JustHealth' <justhealth@richlogan.co.uk>"
    recipient = Client.get(username = username).email
    subject = "JustHealth Verification"
    message = "Thanks for registering! Please verify your account here: " + str(verifyLink)
    m = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, recipient, subject)
    server.sendmail(sender, recipient, m+message)
    server.quit()

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
    message = "Hello, due to a repeated number of incorrect attempts, your password has been locked. Please visit: http://raptor.kent.ac.uk/resetpassword to reset your password."
    m = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, recipient, subject)
    server.sendmail(sender, recipient, m+message)
    server.quit()

@app.route('/users/activate/<payload>')
def verifyUser(payload):
    s = getSerializer()
    try:
        retrievedUsername = s.loads(payload)
    except BadSignature:
        abort(404)

    verifiedTrue = Client.update(verified = True).where(Client.username == retrievedUsername)
    verifiedTrue.execute()
    return render_template('login.html', verified='true')

@app.route('/users/activate/<payload>')
def passwordReset(payload):
    s = getSerializer()
    try:
        retrievedUsername = s.loads(payload)
    except BadSignature:
        abort(404)

    verifiedTrue = Client.update(verified = True).where(Client.username == retrievedUsername)
    verifiedTrue.execute()
    return redirect(url_for('index'))


# Checks to see if a session is set. If not, kicks to login screen.
def needLogin(f):
  @wraps(f)
  def loginCheck(*args, **kwargs):
    try:
      session['username']
    except KeyError, e:
      # session['username'] doesn't exist, kick to login screen
      return redirect(url_for('login'))
    # User logged in, continue as normal
    return f(*args, **kwargs)
  return loginCheck

@app.route('/')
@needLogin
def index():
    return session['username']

@app.route('/register', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':

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
        return 'Username can not be longer then 25 characters'

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
        return render_template('register.html', errorMessage = "Username already taken")

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
      return "You will see a verification email shortly!"
    else:
      return render_template('register.html')

#finds the value of the loginattempts field in the database
def getLoginAttempts(username):
  loginAttempts = Client.get(username=request.form['username']).loginattempts
  return loginAttempts

@app.route('/termsandconditions')
def terms():
  return render_template('termsandconditions.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
      session.pop('username', None)
      try:
        isAccountLocked = Client.get(username=request.form['username']).accountlocked
        isAccountVerified = Client.get(username=request.form['username']).verified
        if isAccountLocked == False:
          if isAccountVerified == True:
            # Retrieve and compare saved and entered passwords
            hashedPassword = uq8LnAWi7D.get((uq8LnAWi7D.username==request.form['username']) & (uq8LnAWi7D.iscurrent==True)).password.strip()
            password = request.form['password']

            # If valid, set SESSION on username
            if sha256_crypt.verify(password, hashedPassword):
              session['username'] = request.form['username']
              updateLoginAttempts = Client.update(loginattempts = 0).where(str(Client.username).strip() == request.form['username'])
              updateLoginAttempts.execute()
              return redirect(url_for('index'))
            else:
            # lock account if 5 attempts
              getLoginAttempts(request.form['username'])
              updateLoginAttempts = Client.update(loginattempts = getLoginAttempts(request.form['username']) + 1).where(str(Client.username).strip() == request.form['username'])
              updateLoginAttempts.execute()
              if getLoginAttempts(request.form['username']) >= 5:
                updateAccountLocked = Client.update(accountlocked = True).where(str(Client.username).strip() == request.form['username'])
                updateAccountLocked.execute()
                sendUnlockEmail(request.form['username'])
                return render_template('login.html',locked='true')
              else:
                return render_template('login.html',wrongCredentials='true')
          else:
            return render_template('login.html',verified='false')
        else:
          return render_template('login.html',locked='true')
      except Client.DoesNotExist:
        return render_template('login.html',wrongCredentials='true')
    return render_template('login.html')

@app.route('/logout')
@needLogin
def logout():
  session.pop('username', None)
  return redirect(url_for('index'))

@app.route('/resetpassword', methods=['POST', 'GET'])
def resetPassword():
  if request.method == 'POST':
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
      #notVerified = Client.update(verified = False).where(str(Client.username).strip() == profile['username'])

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

      notCurrent.execute()
      #notVerified.execute()
      newCredentials.execute()
      unlockAccount.execute()
      sendPasswordResetEmail(profile['username'])
      session.pop('username', None)
      return "You will receive a password reset verification email shortly."
    else:
      return render_template('resetpassword.html',invalid='true')
  return render_template('resetpassword.html')


app.secret_key = '^\x83J\xd3) \x1a\xa4\x05\xea\xd8,\t=\x14]\xfd\x8c%\x90\xd6\x9f\xa1Z'

if __name__ == '__main__':
    app.run(port=9999, debug=True)
