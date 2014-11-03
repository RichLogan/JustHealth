from justHealthServer import *
from api import *
from functools import wraps

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
            # Valid user, set SESSION and send them where they need to go.
            session["username"] = request.form['username']
            accountType = Client.get(Client.username == request.form['username']).iscarer
            if accountType == True:
                return "Carer"
            else:
                return "Patient"
        else:
            return render_template('login.html', type="danger", message = result)
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
