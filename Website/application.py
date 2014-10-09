from flask import Flask, render_template, request
from database import *
app = Flask(__name__)

@app.route('/register', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
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


      userInsert = Client.insert(username = profile['username'],
                                firstname = profile['firstName'],
                                surname = profile['surname'],
                                dob = profile['dob'],
                                ismale = profile['isMale'],
                                iscarer = profile['isCarer'],
                                email = profile['email'])

      userPassword = uq8LnAWi7D.insert(username = profile['username'],
                                      password = profile['password'],
                                      iscurrent = 'TRUE',
                                      expirydate = '10/10/2014')
      userInsert.execute()
      userPassword.execute()

      return 'Registered'


    else:
      return render_template('register.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/resetpassword')
def resetpassword():
  return render_template('resetpassword.html')



if __name__ == '__main__':
    app.run(debug=True)
