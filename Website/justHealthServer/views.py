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
    jsonResult = getAccountInfo(session['username'])
    result = {}
    result = json.loads(jsonResult)
    name = result['firstname'] + " " + result['surname']
    if result['accounttype'] == "Patient":
      return render_template('patienthome.html', printname = name)
    elif result['accounttype'] == "Carer":
      return render_template('carerhome.html', printname = name)

"""Profile page to display all current users details"""
@app.route('/profile')
@needLogin
def profile():
    profileDetails = json.loads(getAccountInfo(session['username']))

    connections = json.loads(getConnections(session['username']))
    outgoingConnections = json.loads(connections['outgoing'])
    incomingConnections = json.loads(connections['incoming'])
    completedConnections = json.loads(connections['completed'])

    if profileDetails['accounttype'] == "Patient":
      return render_template('profile.html', profileDetails=profileDetails, outgoing=outgoingConnections, incoming=incomingConnections, completed=completedConnections, printaccounttype = 'Patient')
    elif profileDetails['accounttype'] == "Carer":
        return render_template('profile.html', profileDetails=profileDetails, outgoing=outgoingConnections, incoming=incomingConnections, completed=completedConnections, printaccounttype = 'Carer' )

"""terms and conditions page link"""
@app.route('/termsandconditions')
def terms():
  return render_template('termsandconditions.html')

@app.route('/search', methods=['POST', 'GET'])
@needLogin
def search():
    if request.method =='POST':
        result = searchPatientCarer(request.form['username'], request.form['searchTerm'])
        result = json.loads(result)
        return render_template ('search.html',results = result, username= session['username'])
    return render_template('search.html',username= session['username'])

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
    return render_template('login.html', type='success', message='Thank you for verifying your account.')

@app.route('/users/activate/<payload>')
def passwordReset(payload):
    s = getSerializer()
    try:
        retrievedUsername = s.loads(payload)
    except BadSignature:
        abort(404)

    verifiedTrue = Client.update(verified = True).where(Client.username == retrievedUsername)
    verifiedTrue.execute()
    return render_template('login.html', type='success', message='Thank you, your password has now been reset and verified.')

@app.route('/api/resetpassword/<payload>')
def loadPasswordReset(payload):
  s = getSerializer()
  try:
    user = s.loads(payload)
    user = str(user).strip()
  except BadSignature:
    abort(404)

  return render_template('resetpassword.html', user=user)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        result = authenticate()
        if result == "Authenticated":
            # Valid user, set SESSION
            session["username"] = request.form['username']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', type="danger", message = result)
    try:
      session['username']
    except KeyError, e:
      return render_template('login.html')
    return redirect(url_for('index'))

@app.route('/forgotPassword', methods=['POST', 'GET'])
def forgotPassword():
    if request.method == 'POST':
      username = getUserFromEmail(request.form['email'])
      if username == "False":
        return render_template('login.html', type='danger', message="An account with this email address does not exist.")
      else:
        sendForgotPasswordEmail(username)
        return render_template('login.html', type='success', message="An email has been sent to you containing a link, which will allow you to reset your password.")

# This method is run once the form to reset the password has been submitted
@app.route('/resetpassword', methods=['POST', 'GET'])
def resetPasswordRedirect():
  if request.method == 'POST':
    result = resetPassword()
    if result == "True":
        return render_template('login.html', type="success", message="Your password has been reset, please check your email and click the link to verify.")
    else:
        return render_template('resetpassword.html', type="danger", message=result)
  return render_template('resetpassword.html')


@app.route('/prescriptions')
def  prescriptions():
  return render_template('prescriptions.html')
