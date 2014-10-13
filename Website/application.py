from flask import Flask, render_template, request, session, redirect, url_for
from functools import wraps
from passlib.hash import sha256_crypt
from database import *
import re

app = Flask(__name__)

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
      if re.match(pattern, profile['email']):
        return True
      else:
        return False

      # Encrypt password with SHA 256
      profile['password'] = sha256_crypt.encrypt(profile['password'])

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
        expirydate = '10/10/2014'
      )

      # Execute Queries
      userInsert.execute()
      userPassword.execute()

      return 'Registered'
    else:
      return render_template('register.html')

#finds the value of the loginattempts field in the database
def getLoginAttempts(username):
  loginAttempts = Client.get(username=request.form['username']).loginattempts
  return loginAttempts

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
      isAccountLocked = Client.get(username=request.form['username']).accountlocked
      if isAccountLocked == False:

        # Retrieve and compare saved and entered passwords
        hashedPassword = uq8LnAWi7D.get(username=request.form['username'], iscurrent=True).password.strip()
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
            return render_template('login.html',locked='true')
      else:
        return render_template('login.html',locked='true')      
      # Retrieve and compare saved and entered passwords
      hashedPassword = uq8LnAWi7D.get(username=request.form['username']).password.strip()
      password = request.form['password']

      # If valid, set SESSION on username
      if sha256_crypt.verify(password, hashedPassword):
        session['username'] = request.form['username']
        return redirect(url_for('index'))
      else:
        return render_template('login.html',wrongCredentials='true')
    return render_template('login.html')
@app.route('/logout')
@needLogin
def logout():
  session.pop('username', None)
  return redirect(url_for('index'))

@app.route('/resetpassword', methods=['POST', 'GET'])
def resetPassword(): 
  return render_template('resetpassword.html')
  if request.method == 'POST':
    try:
        profile = {}
        profile['username'] = request.form['username']
        profile['confirmemail'] = request.form['email']
        profile['newpassword'] = request.form['password']
        profile['confirmnewpassword'] = request.form['confirmpassword']
        profile['confirmdob'] = request.form['dob']
    except KeyError, e:
      return "All fields must be filled out"
      
      getEmail = client.get(username=profile['username']).email
      getDob = client.get(username=profile['username']).dob

      if getEmail==profile['confirmemail'] and getDob==profile['confirmdob']:

        #set the old password to iscurrent = false
        notCurrent = uq8LnAWi7D.update(iscurrent=false).where(username=profile['username'])
       
        # Build insert password query
        newCredentials = uq8LnAWi7D.insert(
          username = profile['username'],
          password = profile['password'],
          iscurrent = 'TRUE',
          expirydate = '10/10/2014'
        )

        notCurrent.execute()
        newCredentials.execute()
      else:
        return render_template('login.html',invalid='true')
  return render_template('resetpassword.html')


app.secret_key = '^\x83J\xd3) \x1a\xa4\x05\xea\xd8,\t=\x14]\xfd\x8c%\x90\xd6\x9f\xa1Z'

if __name__ == '__main__':
    app.run(debug=True)

