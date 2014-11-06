from justHealthServer import *
from api import *
from functools import wraps
import json

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

@app.route('/deactivate', methods=['POST', 'GET'])
@needLogin
def deactivate():
    if request.method == 'POST':
        result = deactivateAccount()
        if result == "Deleted":
            session.pop('username', None)
            return render_template('login.html', type="success", message = "Your account has been deleted")
        elif result == "Kept":
            session.pop('username', None)
            return render_template('login.html', type="success", message = "Your account has been deactivated")
        else:
            return render_template('deactivate.html', reasons = Deactivatereason.select(), user = session['username'], type="danger", message = result)
    return render_template('deactivate.html', reasons = Deactivatereason.select(), user = session['username'])

# Account Pages
@app.route('/register', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        result = registerUser()
        if result == "True":
            return render_template('login.html', type="success", message="Thanks for registering! Please check your email for a verification link")
        else:
            render_template('register.html', type="danger", message = result)
    return render_template('register.html')

@app.route('/logout')
@needLogin
def logout():
  session.pop('username', None)
  return redirect(url_for('index'))

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

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        result = authenticate()
        if result == "Authenticated":
            # Valid user, set SESSION
            session["username"] = request.form['username']
            # Find the account type, first name, surname of the user and direct them to the relevant portal page
            jsonResult = getAccountInfo()
            result = {}
            result = json.loads(jsonResult)
            name = result['firstname'] + " " + result['surname']
            if result['accounttype'] == "Patient":
              return render_template('patienthome.html', printname = name)
            elif result['accounttype'] == "Carer":
              return render_template('carerhome.html', printname = name)
        else:
            return render_template('login.html', type="danger", message = result)
    try:
        session['username']
    except KeyError, e:
        return render_template('login.html')
    return redirect(url_for('index'))

@app.route('/resetpassword', methods=['POST', 'GET'])
def resetPasswordView():
  if request.method == 'POST':
    result = resetPassword()
    if result == "True":
        return render_template('login.html', type="success", message="Your password has been reset, please check your email.")
    else:
        return render_template('resetpassword.html', type="danger", message=result)
  return render_template('resetpassword.html')
