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
