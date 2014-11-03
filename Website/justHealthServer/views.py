from justHealthServer import *

from itsdangerous import URLSafeSerializer, BadSignature
from passlib.hash import sha256_crypt

from functools import wraps

import re
import smtplib
import datetime

from database import *

# Decorator Functions
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

@app.route('/termsandconditions')
def terms():
  return render_template('termsandconditions.html')

@app.route('/logout')
@needLogin
def logout():
  session.pop('username', None)
  return redirect(url_for('index'))


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

@app.route('/register', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        result = api.register(request.form)
        if result == True:
            return "Success"
        else:
            render_template('register.html', errorMessage = result)
    else:
      return render_template('register.html')

#finds the value of the loginattempts field in the database
def getLoginAttempts(username):
  loginAttempts = Client.get(username=request.form['username']).loginattempts
  return loginAttempts

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
              updateLoginAttempts = Client.update(loginattempts = 0).where(Client.username == request.form['username'])
              updateLoginAttempts.execute()
              accountType = Client.get(username=request.form['username']).iscarer
              if (accountType == True):
                return 'carer'
              elif (accountType == False):
                return render_template('patienthome.html')
            else:
            # lock account if 5 attempts
              getLoginAttempts(request.form['username'])
              updateLoginAttempts = Client.update(loginattempts = getLoginAttempts(request.form['username']) + 1).where(Client.username == request.form['username'])
              updateLoginAttempts.execute()
              if getLoginAttempts(request.form['username']) >= 5:
                updateAccountLocked = Client.update(accountlocked = True).where(Client.username == request.form['username'])
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
      session.pop('username', None)
      return "You will receive a password reset verification email shortly."
    else:
      return render_template('resetpassword.html',invalid='true')
  return render_template('resetpassword.html')
