from flask import Flask, render_template, request
import database
app = Flask(__name__)

@app.route('/register')
def registration():
    if request.method == 'POST':
      profile['username'] = request.form['username']
      profile['firstName'] = request.form['firstName']
      profile['surname'] = request.form['surname']
      profile['dob'] = request.form['dob']
      profile['isMale'] = request.form['isMale']
      profile['isCarer'] = request.form['isCarer']
      profile['email'] = request.form['email']
      profile['password'] = request.form['password']
      profile['confirmPassword'] = request.form['confirmPassword']



    else:
      return render_template('register.html')

@app.route('/login')
def login():
  return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
