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
    result = json.loads(getAccountInfo(session['username']))
    name = result['firstname'] + " " + result['surname']
    if result['accounttype'] == "Patient":
      return render_template('patienthome.html', printname = name)
    elif result['accounttype'] == "Carer":
      return render_template('carerhome.html', printname = name)

@app.route('/profile')
@needLogin
def profile():
    """Profile page to display all current users details"""
    profileDetails = json.loads(getAccountInfo(session['username']))

    connections = json.loads(getConnections(session['username']))
    outgoingConnections = json.loads(connections['outgoing'])
    incomingConnections = json.loads(connections['incoming'])
    completedConnections = json.loads(connections['completed'])

    if profileDetails['accounttype'] == "Patient":
      return render_template('profile.html', profileDetails=profileDetails, outgoing=outgoingConnections, incoming=incomingConnections, completed=completedConnections, printaccounttype = 'Patient')
    elif profileDetails['accounttype'] == "Carer":
        return render_template('profile.html', profileDetails=profileDetails, outgoing=outgoingConnections, incoming=incomingConnections, completed=completedConnections, printaccounttype = 'Carer' )


@app.route('/termsandconditions')
def terms():
    """terms and conditions page link"""
    return render_template('termsandconditions.html')

@app.route('/corpusindex')
def corpus():
  return render_template('indexCorpus.html')

@app.route('/legal')
def legal():
  return render_template('legal.html')

@app.route('/privacypolicy')
def privacy():
  return render_template('privacypolicy.html')

@app.route('/references')
def references():
  return render_template('references.html')

@app.route('/sitemap')
def sitemap():
  return render_template('sitemap.html')

@app.route('/settings')
@needLogin
def settings():
    profileDetails = json.loads(getAccountInfo(session['username']))
    if profileDetails['accounttype'] == "Patient":
        return render_template('settings.html', profileDetails=profileDetails, printaccounttype = 'Patient')
    elif profileDetails['accounttype'] == "Carer":
        return render_template('settings.html', profileDetails=profileDetails, printaccounttype = 'Carer' )


@app.route('/search', methods=['POST', 'GET'])
@needLogin
def search():
    if request.method =='POST':
        result = searchPatientCarer(request.form['username'], request.form['searchterm'])
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
            return render_template('login.html', type="success",  message="Thanks for registering! Please check your email for a verification link")
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


@app.route('/completeConnection', methods=['POST', 'GET'])
def completeConnection():
    return completeConnection(request.form)

@app.route('/appointments', methods=['POST', 'GET'])
def appointments():
  appointments = json.loads(getAllAppointments(session['username'], session['username']))

  if request.method == 'POST':
    #The tick box is not sent if it isn't ticked, so we have to catch it here.
    try:
      private = request.form['private']
    except KeyError, e:
      private = "False"

    details = {}
    details['creator'] = session['username']
    details['name'] = request.form['name']
    details['apptype'] = request.form['apptype']
    details['addressnamenumber'] = request.form['addressnamenumber']
    details['postcode'] = request.form['postcode']
    details['startdate'] = request.form['startdate']
    details['starttime'] = request.form['starttime']
    details['enddate'] = request.form['enddate']
    details['endtime'] = request.form['endtime']
    details['description'] = request.form['description']
    details['private'] = private 

    added = int(addPatientAppointment(details))

    #checks that an id is returned
    if added > 0: 
      flash("Appointment Added", 'success')
      return redirect(url_for('appointments'))
  return render_template('patientAppointments.html', appType=Appointmenttype.select(), appointments=appointments, request=None)


@app.route('/deleteAppointment', methods=['POST', 'GET'])
def deleteAppointment_view():
  if request.method == 'GET':
    appid = request.args.get("appid")
    deleted = deleteAppointment(session['username'], appid)
    flash(deleted, 'success')
    return redirect(url_for('appointments'))

@app.route('/updateAppointment', methods=['POST', 'GET'])
def getUpdateAppointment_view():
  if request.method == 'GET':
    appid = request.args.get('appid')
    getUpdate = json.loads(getUpdateAppointment(session['username'], appid))
    return render_template('patientUpdateAppointment.html', appType=Appointmenttype.select(), request=getUpdate)

@app.route('/patientUpdateAppointment', methods=['POST'])
def updateAppointment_view():
  if request.method == 'POST':
    #The tick box is not sent if it isn't ticked, so we have to catch it here.
    try:
      private = request.form['private']
    except KeyError, e:
      private = "False"

    updated = updateAppointment(request.form['appid'], request.form['name'], request.form['type'], request.form['nameNumber'], request.form['postcode'], request.form['dateFrom'], request.form['startTime'], request.form['dateTo'], request.form['endTime'], request.form['other'], private)
    flash(updated, 'success')
    return redirect(url_for('appointments'))

@app.route('/myPatients')
def myPatients():
    # Get Patients
    if json.loads(api.getAccountInfo(session['username']))['accounttype'] == 'Carer':
        # Get all patients connected to this user
        connections = json.loads(getConnections(session['username']))
        completedConnections = json.loads(connections['completed'])
        patients = []
        for connection in completedConnections:
            if connection['accounttype'] == "Patient":
                patients.append(connection)
    # Get all appointments
    appointmentsMapping = {}
    # Get all prescriptions
    activePrescriptions = {}
    upcomingPrescriptions = {}
    expiredPrescriptions = {}
    for patient in patients:
        appointmentsMapping[patient['username']] = json.loads(getAllAppointments(session['username'], patient['username']))

        activePrescriptions[patient['username']] = json.loads(getActivePrescriptions(patient['username']))
        upcomingPrescriptions[patient['username']] = json.loads(getUpcomingPrescriptions(patient['username']))
        expiredPrescriptions[patient['username']] = json.loads(getExpiredPrescriptions(patient['username']))
    return render_template('myPatients.html', patients = patients, appointmentsMapping = appointmentsMapping, activePrescriptions = activePrescriptions, upcomingPrescriptions = upcomingPrescriptions, expiredPrescriptions = expiredPrescriptions)

@app.route('/deletePrescription')
def deletePrescription_view():
    prescriptionid = request.args.get('id', '')
    prescription = Prescription.select().where(Prescription.prescriptionid == prescriptionid).get()
    username = request.args.get('username', '')
    result = deletePrescription(prescriptionid)
    if result != "Failed":
        result = "Deleted " + prescription.medication.name + " (" + str(prescription.quantity) + "x" + str(prescription.dosage) + ") " + prescription.dosageunit + " for " + username
        flash(result, 'result')
        flash('success', 'class')
        flash(username, 'user')
        flash('prescription', 'type')
        return redirect(url_for('myPatients'))
    else:
        flash('prescription', 'type')
        flash('danger', 'class')
        flash(result, 'result')
        flash(username, 'user')
        return redirect(url_for('myPatients'))

@app.route('/addPrescription', methods=['POST'])
def addPrescription_view():
    result = addPrescription(request.form)
    username = request.form['username']
    if result != "Could not add prescription":
        flash(result, 'result')
        flash('success', 'class')
        flash(username, 'user')
        flash('prescription', 'type')
        return redirect(url_for('myPatients'))
    else:
        flash('prescription', 'type')
        flash('danger', 'class')
        flash(result, 'result')
        flash(username, 'user')
        return redirect(url_for('myPatients'))

@app.route('/updatePrescription', methods=['POST'])
def updatePrescription_view():
    result = editPrescription(request.form)
    username = request.form['username']
    if result != "Failed":
        flash(result, 'result')
        flash('success', 'class')
        flash(username, 'user')
        flash('prescription', 'type')
        return redirect(url_for('myPatients'))
    else:
        flash('prescription', 'type')
        flash('danger', 'class')
        flash(result, 'result')
        flash(username, 'user')
        return redirect(url_for('myPatients'))

@app.route('/prescriptions')
def  prescriptions():
    prescriptions = json.loads(getPrescriptions(session['username']))
    return render_template('prescriptions.html', prescriptions = prescriptions)


@app.route('/carerAppointments', methods=['POST', 'GET'])
def carerappointments():
  if request.method == 'POST':

    private = "True"

    details = {}
    details['creator'] = session['username']
    details['name'] = request.form['name']
    details['apptype'] = request.form['apptype']
    details['addressnamenumber'] = request.form['addressnamenumber']
    details['postcode'] = request.form['postcode']
    details['startdate'] = request.form['startdate']
    details['starttime'] = request.form['starttime']
    details['enddate'] = request.form['enddate']
    details['endtime'] = request.form['endtime']
    details['description'] = request.form['description']
    details['private'] = private 

    added = int(addPatientAppointment(details))

    #checks that an id is returned
    if added > 0: 
      flash("Appointment Added", 'success')
  upcoming = json.loads(getAllAppointments(session['username'], session['username']))
  return render_template('carerAppointments.html', appType=Appointmenttype.select(), appointments=upcoming, request=None)

@app.route('/inviteeappointments', methods=['POST', 'GET'])
def inviteeappointments():
  if request.method == 'POST':

    details = {}
    details['creator'] = session['username']
    details['username'] = request.form['username']
    details['name'] = request.form['name']
    details['apptype'] = request.form['apptype']
    details['addressnamenumber'] = request.form['addressnamenumber']
    details['postcode'] = request.form['postcode']
    details['startdate'] = request.form['startdate']
    details['starttime'] = request.form['starttime']
    details['enddate'] = request.form['enddate']
    details['endtime'] = request.form['endtime']
    details['description'] = request.form['description']

    added = addInviteeAppointment(details)
    return redirect(url_for("myPatients"))

@app.errorhandler(500)
def internal_error(error):
    return render_template('internalError.html'), 500

@app.errorhandler(408)
def internal_error(error):
  return render_template('internalError.html'), 408

@app.errorhandler(404)
def internal_error(error):
  return render_template('404Error.html'), 404

@app.errorhandler(400)
def internal_error(error):
  return render_template('400RequestMalformed.html'), 400

@app.errorhandler(401)
def internal_error(error):
  return render_template('400RequestMalformed.html'), 401
