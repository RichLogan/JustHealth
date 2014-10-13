from flask import Flask, render_template, request, session, redirect, url_for
from functools import wraps
from passlib.hash import sha256_crypt
from database import *

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
      profile = {}
      profile['username'] = request.form['username']
      profile['firstName'] = request.form['firstName']
      profile['surname'] = request.form['surname']
      profile['dob'] = request.form['dob']
      profile['isMale'] = request.form['isMale']
      profile['isCarer'] = request.form['isCarer']
      profile['email'] = request.form['email']
      profile['password'] = request.form['password']
      profile['confirmPassword'] = request.form['confirmPassword']

      # Validate all input
      for key in profile:
        profile[key] = profile[key].strip()

      # Encrypt password with SHA 256
      profile['password'] = sha256_crypt.encrypt(profile['password'])

      # Build insert user query
      userInsert = Client.insert(
        username = profile['username'],
        firstname = profile['firstName'],
        surname = profile['surname'],
        dob = profile['dob'],
        ismale = profile['isMale'],
        iscarer = profile['isCarer'],
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

@app.route('/resetpassword')
def resetpassword():
  return render_template('resetpassword.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
      isAccountLocked = Client.get(username=request.form['username']).accountlocked
      if isAccountLocked == False:
      
        # Retrieve and compare saved and entered passwords
        hashedPassword = uq8LnAWi7D.get(username=request.form['username']).password.strip()
        password = request.form['password']

        # If valid, set SESSION on username
        if sha256_crypt.verify(password, hashedPassword):
          session['username'] = request.form['username']
          session['count'] = 0
          return redirect(url_for('index'))
        else:
          # lock account if 5 attempts
          try: 
            session['count'] += 1
          except KeyError, e:
            session['count'] = 1
          if session['count'] >= 5:
            updateAccountLocked = Client.update(accountlocked = True).where(str(Client.username).strip() == request.form['username'])
            updateAccountLocked.execute()
            return str(Client.username)
      else:
        return "Account locked Bro"
        session['count'] = 0
    return render_template('login.html')

@app.route('/logout')
@needLogin
def logout():
  session.pop('username', None)
  return redirect(url_for('index'))

app.secret_key = '^\x83J\xd3) \x1a\xa4\x05\xea\xd8,\t=\x14]\xfd\x8c%\x90\xd6\x9f\xa1Z'

if __name__ == '__main__':
    app.run(debug=True)
