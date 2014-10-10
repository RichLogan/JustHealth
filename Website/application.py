from flask import Flask, render_template, request
from passlib.hash import sha256_crypt
from database import *

app = Flask(__name__)

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
      # Retrieve and compare saved and entered passwords
      hashedPassword = uq8LnAWi7D.get(username=request.form['username']).password.strip()
      password = request.form['password']
      return str(sha256_crypt.verify(password, hashedPassword))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
