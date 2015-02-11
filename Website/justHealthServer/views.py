from flask import send_from_directory
from justHealthServer import *
from api import *
from functools import wraps
import json
import webbrowser

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

@app.route('/images/<filename>')
@needLogin
def getProfilePicture(filename):
    return send_from_directory(app.config['PROFILE_PICTURE'], filename)

@app.route('/')
@needLogin
def index():
    """Sends user to home page according to account type if session is active"""
    result = json.loads(getAccountInfo(session['username']))
    name = result['firstname'] + " " + result['surname']
    if result['accounttype'] == "Patient":
      return render_template('patienthome.html', printname = name)
    elif result['accounttype'] == "Carer":
      return render_template('carerhome.html', printname = name)

@app.route('/home')
@needLogin
def home():
    """Dashboard home page patient"""
    accountInfo = json.loads(getAccountInfo(session['username']))
    #notifications = json.loads(getNotifications(session['username']))
    connections = json.loads(getConnections(session['username']))
    appointments = json.loads(getAllAppointments(session['username'], session['username']))
    prescriptions = json.loads(getPrescriptions(session['username']))
    outgoingConnections = json.loads(connections['outgoing'])
    incomingConnections = json.loads(connections['incoming'])
    completedConnections = json.loads(connections['completed'])
    
    # Notification example
    notifications = []
    notification1 = {}
    notification1['type'] = "danger"
    notification1['content'] = "Testing"
    notifications.append(notification1)
    notification2 = {}
    notification2['type'] = "success"
    notification2['content'] = "Testing 2"
    notifications.append(notification2)

    return render_template('dashboard.html', accountInfo=accountInfo, notifications=notifications, connections=connections, appType=Appointmenttype.select(), appointments=appointments, prescriptions = prescriptions, outgoing=outgoingConnections, incoming=incomingConnections, completed=completedConnections)

@app.route('/homecarer')
@needLogin
def homecarer():
    """Dashboard home page carer"""
    accountInfo = json.loads(getAccountInfo(session['username']))
    #notifications = json.loads(getNotifications(session['username']))
    connections = json.loads(getConnections(session['username']))
    appointments = json.loads(getAllAppointments(session['username'], session['username']))
    outgoingConnections = json.loads(connections['outgoing'])
    incomingConnections = json.loads(connections['incoming'])
    completedConnections = json.loads(connections['completed'])
    
    # Notification example
    notifications = []
    notification1 = {}
    notification1['type'] = "danger"
    notification1['content'] = "Testing"
    notifications.append(notification1)
    notification2 = {}
    notification2['type'] = "success"
    notification2['content'] = "Testing 2"
    notifications.append(notification2)

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

    return render_template('dashboardCarer.html', accountInfo=accountInfo, notifications=notifications, connections=connections, appType=Appointmenttype.select(), appointments=appointments, outgoing=outgoingConnections, incoming=incomingConnections, completed=completedConnections,patients = patients, appointmentsMapping = appointmentsMapping, activePrescriptions = activePrescriptions, upcomingPrescriptions = upcomingPrescriptions, expiredPrescriptions = expiredPrescriptions)

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

@app.route('/editProfile', methods=['POST', 'GET'])
def getEditDetails_view():
    if request.method == 'GET':
        username = request.args.get('username')
        getUpdate = json.loads(getAccountInfo(session['username']))
    return render_template('editProfile.html', request=getUpdate)
   
@app.route('/updateProfile', methods=['POST'])
def editDetails_view():
    updated = editProfile(request.form, request.files)
    if updated == "Failed":
        flash(updated, 'danger')
    else:
        flash(updated, 'success')
    return redirect(url_for('profile'))

@app.route('/termsandconditions')
def terms():
    """JustHealth terms and conditions reference page for all users"""
    return render_template('termsandconditions.html')

@app.route('/corpusindex')
def corpus():
    return render_template('indexCorpus.html')

@app.route('/legal')
def legal():
    """This page hold 4 tiles each a link onto the respective legal page"""
    return render_template('legal.html')

@app.route('/privacypolicy')
def privacy():
    """JustHealth privacy policy and data protection reference page"""
    return render_template('privacypolicy.html')

@app.route('/references')
def references():
    return render_template('references.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/sitemap')
def sitemap():
    return render_template('sitemap.html')

@app.route('/contactUs', methods=['POST', 'GET'])
def contactUs():
    profileDetails = json.loads(getAccountInfo(session['username']))
    if request.method == 'POST': 
        result = sendContactUs(request.form)
        return render_template('contactUs.html', type="success", message = 'Your message has been sent, please allow up to 24 hours for a response', profileDetails=profileDetails, printaccounttype = profileDetails['accounttype'])
    else: 
       return render_template('contactUs.html', profileDetails=profileDetails, printaccounttype = profileDetails['accounttype'])
    

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
    """Search to find a different user's profile"""
    if request.method =='POST':
        result = searchPatientCarer(request.form['username'], request.form['searchterm'])
        result = json.loads(result)
        return render_template ('search.html',results = result, username= session['username'])
    return render_template('search.html', username= session['username'])

@app.route('/deactivate', methods=['POST', 'GET'])
@needLogin
def deactivate():
    """Handles account deactivation form"""
    if request.method == 'POST':
        result = deactivateAccount(request.form)
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
    """Handles user registration form"""
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
    """Terminates user session"""
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/users/activate/<payload>')
def verifyUser(payload):
    """User confirmation of account verification"""
    s = getSerializer()
    try:
        retrievedUsername = s.loads(payload)
    except BadSignature:
        abort(404)

    verifiedTrue = Client.update(verified = True).where(Client.username == retrievedUsername)
    verifiedTrue.execute()
    return render_template('login.html', type='success', message='Thank you for verifying your account.')

@app.route('/password')
def changePassword():
    """Change password form (when user knows their current password)"""
    return render_template('changePassword.html')

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
    """Gets username from login in order to authenticate session"""
    if request.method == 'POST':
        result = authenticate()
        if result == "Authenticated":
            # Valid user, set SESSION
            session["username"] = request.form['username']
            nameresult = json.loads(getAccountInfo(session['username']))
            session['firstname'] = nameresult['firstname']
            session['surname'] = nameresult['surname']
            fullname = session['firstname'] + " " + session['surname']

            return redirect(url_for('index'))
        else:
            return render_template('login.html', printname = fullname, type="danger", message = result)
    try:
      session['username']
    except KeyError, e:
      return render_template('login.html')
    return redirect(url_for('index'))

@app.route('/forgotPassword', methods=['POST', 'GET'])
def forgotPassword():
    """Finds the user's account from the email address it was registered with"""
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
    """Follows unique link in email to allow user to reset password, only after forgotPassword form is submitted."""
    if request.method == 'POST':
        result = resetPassword()
    if result == "True":
        return render_template('login.html', type="success", message="Your password has been reset, please check your email and click the link to verify.")
    else:
        return render_template('resetpassword.html', type="danger", message=result)
    return render_template('resetpassword.html')


@app.route('/createConnectionWeb', methods=['POST', 'GET'])
def createConnectionWeb():
    result = createConnection(request.form)
    if result != "Connection already established":
        flash(result, 'success')
        return redirect('/profile?go=connections')
    else:
        flash(result, 'danger')
        return redirect(url_for('search'))

@app.route('/completeConnectionWeb', methods=['POST', 'GET'])
def completeConnectionWeb():
    result = completeConnection(request.form)
    if result == "Incorrect code":
        flash(result, 'danger')
    else:
        flash(result, 'success')
    return redirect('/profile?go=connections')

@app.route('/deleteConnectionWeb', methods=['POST', 'GET'])
def deleteConnectionWeb():
    result = deleteConnection(request.form)
    if result == "True":
        flash("Delete successful", 'success')
    else:
        flash("Delete failed. Please contact an administrator", 'danger')
    return redirect('/profile?go=connections')

@app.route('/cancelConnectionWeb', methods=['POST', 'GET'])
def cancelConnectionWeb():
    result = cancelRequest(request.form)
    if result == "True":
        flash("Cancellation successful", 'success')
    else:
        flash("Cancel failed. Please contact an administrator", 'danger')
    return redirect('/profile?go=connections')

@app.route('/appointments', methods=['POST', 'GET'])
def appointments():
  """Form for patient to add an appointment, they choose privacy level for their carer."""
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
  """Shows message to inform the user that the appointment has been deleted"""
  if request.method == 'GET':
    appid = request.args.get("appid")
    deleted = deleteAppointment(session['username'], appid)
    flash(deleted, 'success')
    return redirect(url_for('appointments'))

@app.route('/updateAppointment', methods=['POST', 'GET'])
def getUpdateAppointment_view():
  """Takes the appointment ID to put the existing appointment information in the form, ready to be updated"""
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
    """Shows carer page listing their connected patients, they can edit each patient's prescriptions and appointments from here"""
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

@app.route('/prescriptions')
def prescriptions():
    """Shows all the active prescriptions for the patient selected"""
    prescriptions = json.loads(getPrescriptions(session['username']))
    return render_template('prescriptions.html', prescriptions = prescriptions)

@app.route('/deletePrescription')
def deletePrescription_view():
    """Informs Carer that the prescription has been deleted from the selected patient"""
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
    """Informs Carer that the prescription has been added to the selected patient"""
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
    """Informs Carer that the prescription has been updated for the selected patient"""
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

@app.route('/carerAppointments', methods=['POST', 'GET'])
def carerappointments():
  """Form for carer to add a personal appointment, this is not shown to patients."""
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
  """Form for carer to add an appointment with a specific patient they are connected with, this will show on the patient's calendar."""
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

@app.route('/nhsSearch', methods=['POST', 'GET'])
def searchNHS():
  if request.method == 'POST':
    website = searchNHSDirect(request.form['searchterm'])
    webbrowser.open(website,new=2)
  return render_template('searchNHSDirect.html')


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
  return "Your request appears to be malformed", 400

@app.errorhandler(401)
def internal_error(error):
  return render_template('400RequestMalformed.html'), 401

#Admin Portal pages
@app.route('/adminPortal')
def adminPortal():
    allUsers = json.loads(getAllUsers())
    if request.method == 'POST':
        result = deactivateAccount(request.form)  
        return render_template('adminHome.html', reasons = Deactivatereason.select(), allUsers = allUsers)
    else: 
       return render_template('adminHome.html', reasons = Deactivatereason.select(), allUsers = allUsers)

@app.route('/addNewDeactivate', methods=['POST'])
def addNewDeactivate():
    if request.method == 'POST':
        result = addDeactivate(request.form)  
        if result == "True":
            return render_template('adminHome.html',type="success", message = 'Deactivate Reason Added')
        else: render_template('adminHome.html',type="warning", message = 'Update failed')
    else: 
       return render_template('adminHome.html')

@app.route('/addNewMedication', methods=['POST'])
def addNewMedication():
    if request.method == 'POST':
        result = newMedication(request.form)  
        if result == "True":
            return render_template('adminHome.html',type="success", message = 'Medication Added')
        else: render_template('adminHome.html',type="warning", message = 'Update failed')
    else:   
       return render_template('adminHome.html')

