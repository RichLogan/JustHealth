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

def needAdmin(f):
    @wraps(f)
    def needAdmin(*args, **kwargs):
        if session['accounttype'] != "Admin":
            # If the URL for admin portal is attempted, check for authorisation.
            return render_template('401Unauthorised.html'), 401
        return f(*args, **kwargs)
    return needAdmin

@app.route('/images/<filename>')
@needLogin
def getProfilePicture(filename):
    """Gets the user's profile picture from the JustHealth images folder on the server"""
    return send_from_directory(app.config['PROFILE_PICTURE'], filename)

@app.route('/')
def frontPage():
    # Checks if a user session is set, if not kick to the front page, instead of dashboard
    try:
        session['username']
        return redirect(url_for('index'))
    except KeyError, e:
        return render_template('frontPage.html')

@app.route('/home')
@needLogin
def index():
    """Sends user to a dashboard according to account type if session is active, it shows their profile and connections. A patient will be able to see their notifications, prescriptions and appointments. A carer will be able to see their notifications, the patients that they are connected to (with prescriptions and appointments) and their own appointments"""
    ## set common functionality for all account types
    accountInfo = json.loads(getAccountInfo(session['username']))

    if accountInfo['accounttype'] == "Admin":
        # direct user to the admin portal
        return redirect(url_for('adminPortal'))

    # common functionality for patient and carer
    connections = json.loads(getConnections(session['username']))
    appointments = json.loads(getAllAppointments(session['username'], session['username']))
    outgoingConnections = json.loads(connections['outgoing'])
    incomingConnections = json.loads(connections['incoming'])
    completedConnections = json.loads(connections['completed'])

    if accountInfo['accounttype'] == "Patient":
        # Patient Functionality
        notifications = json.loads(getNotifications(session['username']))
        prescriptions = json.loads(getActivePrescriptions(session['username']))
        reminders = json.loads(getReminders(session['username']))
        return render_template(
            'dashboard.html',
            accountInfo=accountInfo,
            notifications=notifications,
            connections=connections,
            appType=Appointmenttype.select(),
            appointments=appointments,
            prescriptions = prescriptions,
            outgoing=outgoingConnections,
            incoming=incomingConnections,
            completed=completedConnections,
            reminders = reminders)
    elif accountInfo['accounttype'] == "Carer":
        # Carer Functionality
        
        # Get Carer's Patients
        if json.loads(api.getAccountInfo(session['username']))['accounttype'] == 'Carer':
            # Get all patients connected to this user
            connections = json.loads(getConnections(session['username']))
            completedConnections = json.loads(connections['completed'])

            patients = []
            for connection in completedConnections:
                if connection['accounttype'] == "Patient":
                    patients.append(connection)
        
        appointmentsMapping = {}
        activePrescriptions = {}
        upcomingPrescriptions = {}
        expiredPrescriptions = {}
        for patient in patients:
            appointmentsMapping[patient['username']] = json.loads(getAllAppointments(session['username'], patient['username']))
            activePrescriptions[patient['username']] = json.loads(getActivePrescriptions(patient['username']))
            upcomingPrescriptions[patient['username']] = json.loads(getUpcomingPrescriptions(patient['username']))
            expiredPrescriptions[patient['username']] = json.loads(getExpiredPrescriptions(patient['username']))
            # checkPrescriptionLevel(session['username'], activePrescriptions[patient['username']])

        # Notifications relies on some of the methods above and therefore needs to be run at the end of this block.
        # Otherwise the notification won't be displayed until the refresh after it is created.
        notifications = json.loads(getNotifications(session['username']))
        reminders = json.loads(getReminders(session['username']))
        return render_template(
            'dashboardCarer.html',
            accountInfo=accountInfo,
            notifications=notifications,
            reminders=reminders,
            connections=connections,
            appointments=appointments,
            outgoing=outgoingConnections,
            incoming=incomingConnections,
            completed=completedConnections,
            patients = patients,
            appointmentsMapping = appointmentsMapping,
            activePrescriptions = activePrescriptions,
            upcomingPrescriptions = upcomingPrescriptions,
            expiredPrescriptions = expiredPrescriptions,
            appType=Appointmenttype.select(),
            medicationList = Medication.select())

@app.route('/profile')
@needLogin
def profile():
    # Redundant function as the profile page is no longer in use 
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
@needLogin
def getEditDetails_view():
    if request.method == 'GET':
        username = request.args.get('username')
        getUpdate = json.loads(getAccountInfo(session['username']))
    return render_template('editProfile.html', request=getUpdate)
   
@app.route('/updateProfile', methods=['POST'])
@needLogin
def editDetails_view():
    updated = editProfile(request.form, request.files)
    if updated == "Failed":
        flash(updated, 'danger')
    else:
        # sets the profile picture in the session variable so that it updates on submit
        nameresult = json.loads(getAccountInfo(session['username']))
        session['profilepicture'] = nameresult['profilepicture']

        flash(updated, 'success')
    return redirect('/')

@app.route('/termsandconditions')
def terms():
    # Redundant page: content is now in a modal
    """JustHealth terms and conditions reference page for all users"""
    return render_template('termsandconditions.html')

@app.route('/corpusindex')
def corpus():
    return render_template('indexCorpus.html')

@app.route('/legal')
def legal():
    # Redundant page: content is now in a modal
    """This page hold 4 tiles each a link onto the respective legal page"""
    return render_template('legal.html')

@app.route('/privacypolicy')
def privacy():
    # Redundant page: content is now in a modal
    """JustHealth privacy policy and data protection reference page"""
    return render_template('privacypolicy.html')

@app.route('/references')
def references():
    # Redundant page: content is now in a modal
    return render_template('references.html')

@app.route('/faq')
@needLogin
def faq():
    return render_template('faq.html')

@app.route('/sitemap')
@needLogin
def sitemap():
    # Redundant page: content is now in a modal
    return render_template('sitemap.html')

@app.route('/contactUs', methods=['POST', 'GET'])
@needLogin
def contactUs():
    """Shows a form to allow the user to contact JustHealth, it sends an email from the address associated with their account"""
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
    """Search to find a different user, potentially so a connection can then be requested"""
    if request.method =='POST':
        result = searchPatientCarer(request.form['username'], request.form['searchterm'])
        if result == "No users found":
            flash(result, 'danger')
        else:
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
            # if the checkbox is ticked, we delete their data and their account is completely deleted
            session.pop('username', None)
            return render_template('login.html', type="success", message = "Your account has been deleted")
        elif result == "Kept":
            # if the checkbox is left unchecked, we keep their data but mark their account as deactivated
            session.pop('username', None)
            return render_template('login.html', type="success", message = "Your account has been deactivated")
        else:
            # deactive attempt failed
            return render_template('deactivate.html', reasons = Deactivatereason.select(), user = session['username'], type="danger", message = result)
    return render_template('deactivate.html', reasons = Deactivatereason.select(), user = session['username'])

# Account Pages
@app.route('/register', methods=['POST', 'GET'])
def registration():
    """Handles user registration form"""
    if request.method == 'POST':
        result = registerUser()
        if result == "True":
            flash("Thanks for registering! Please check your email for a verification link", "success")
            return redirect('/login')
        else:
            flash(result, "danger")
    return render_template('register.html')

@app.route('/logout')
@needLogin
def logout():
    """Terminates user session and redirects to the front page"""
    session.pop('username', None)
    return redirect('/')

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

@app.route('/password', methods=['POST', 'GET'])
@needLogin
def changePassword():
    """Opens a change password form (for when user knows their current password)"""
    if request.method == 'POST':
        result = changePasswordAPI(request.form)
        if result == "Password changed successfully":
            flash(result, "success")
        else:
            flash(result, "danger")
        return redirect(url_for('changePassword'))
    return render_template('changePassword.html')

@app.route('/users/activate/<payload>')
def passwordReset(payload):
    # forced password reset, if password is expiring etc.
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
    """Gets the username from login in order to authenticate session, log the user in and redirects to index function"""
    if request.method == 'POST':
        result = authenticate()
        if result == "Authenticated":
            # Valid user, set SESSION
            session["username"] = request.form['username']
            nameresult = json.loads(getAccountInfo(session['username']))
            session['firstname'] = nameresult['firstname']
            session['surname'] = nameresult['surname']
            session['accounttype'] = nameresult['accounttype']
            session['profilepicture'] = nameresult['profilepicture']
            fullname = session['firstname'] + session['surname']

            return redirect(url_for('index'))
        # Expired password here
        elif result == "Reset":
            return render_template('expiredpassword.html', user=request.form['username'], message="Your password has expired and needs to be reset before you will be able to log in.", submessage="JustHealth enforce this from time-to-time to ensure that your privacy and security are maximised whilst using the website.")
        elif result == "<11":
            session["username"] = request.form['username']
            nameresult = json.loads(getAccountInfo(session['username']))
            session['firstname'] = nameresult['firstname']
            session['surname'] = nameresult['surname']
            fullname = session['firstname'] + " " + session['surname']

            return render_template('resetpasswordnowquestion.html')
        else:
            return render_template('login.html', type="danger", message = result)
    try:
      session['username']
    except KeyError, e:
      return render_template('login.html')
    return redirect(url_for('index'))

@app.route('/expiredpassword', methods=['POST', 'GET'])
def expiredpassword():
    """This forces the user to the expired password page, and checks the password reset"""
    if request.method == 'POST':
        reset = expiredResetPassword(request.form)
        if reset == "True":
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        # does not work, see API comments for details
        # elif reset == "Exists":
        #      return render_template('expiredpassword.html', user=session['username'], error="The password that you have tried to use has already been used as one of your last five passwords. Please try again.", errortype="danger")
        
        elif reset == "Unmatched":
            # handles the attempted password reset
            return render_template('expiredpassword.html', user=request.form['username'], error="The two passwords you entered did not match, please try again.", errortype="danger")
        else: 
            return render_template('expiredpassword.html', user=session['username'], error="Oops, something went wrong. Please try again.", errortype="danger")

    return render_template('expiredpassword.html', user=session['username'])
    

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
        return render_template('resetpassword.html', type="danger", message="The details that you entered are incorrect. Please try again.", user=result)
    return render_template('resetpassword.html')


@app.route('/createConnectionWeb', methods=['POST', 'GET'])
def createConnectionWeb():
    """Shows user a notification if a connection is attempted to tell them of the current connection state with that user"""
    result = createConnection(request.form)
    if result != "Connection already established":
        flash(result, 'success')
    else:
        flash(result, 'danger')
    return redirect('/home?go=connections')

@app.route('/completeConnectionWeb', methods=['POST', 'GET'])
def completeConnectionWeb():
    """Shows user a notification of whether their attempt to verify a connection was successful, the user has to put in the correct 4 digit code to complete the connection"""
    result = completeConnection(request.form)
    if result == "Incorrect code":
        flash(result, 'danger')
    else:
        flash(result, 'success')
    return redirect('/home?go=connections')

@app.route('/deleteConnectionWeb', methods=['POST', 'GET'])
def deleteConnectionWeb():
    """Shows user a notification if their attempt to delete a connection was successful or not"""
    result = deleteConnection(request.form)
    if result == "True":
        flash("Delete successful", 'success')
    else:
        flash("Delete failed. Please try again or contact an administrator", 'danger')
    return redirect('/home?go=connections')

@app.route('/cancelConnectionWeb', methods=['POST', 'GET'])
def cancelConnectionWeb():
    """Shows user a notification if their attempt to cancel their request for a connection was successful or not"""
    result = cancelRequest(request.form)
    if result == "True":
        flash("Cancellation successful", 'success')
    else:
        flash("Cancellation failed. Please try again or contact an administrator", 'danger')
    return redirect('/home?go=connections')

@app.route('/appointments', methods=['POST', 'GET'])
@needLogin
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
@needLogin
def deleteAppointment_view():
    """Shows message to inform the user that the appointment has been deleted"""
    if request.method == 'GET':
        appid = request.args.get("appid")
        deleted = deleteAppointment(session['username'], appid)
        flash(deleted, 'success')
        return redirect(url_for('appointments'))

@app.route('/updateAppointment', methods=['POST', 'GET'])
@needLogin
def getUpdateAppointment_view():
    """Takes the appointment ID to put the existing appointment information in the form, ready to be updated"""
    if request.method == 'GET':
        appid = request.args.get('appid')
        whereFrom = request.args.get('whereFrom')
        getUpdate = json.loads(getUpdateAppointment(session['username'], appid))
        return render_template('patientUpdateAppointment.html', appType=Appointmenttype.select(), request=getUpdate, previousLocation=whereFrom)

@app.route('/patientUpdateAppointment', methods=['POST'])
@needLogin
def updateAppointment_view():
    """If the privacy option isn't selected, the field isn't sent with the form, so it is caught and handled in this function"""
    if request.method == 'POST':
        #The tick box is not sent if it isn't ticked, so we have to catch it here.
        try:
            private = request.form['private']
        except KeyError, e:
            private = "False"

    updated = updateAppointment(request.form['appid'], request.form['name'], request.form['type'], request.form['nameNumber'], request.form['postcode'], request.form['dateFrom'], request.form['startTime'], request.form['dateTo'], request.form['endTime'], request.form['other'], private)
    flash(updated, 'success')
    if request.form['whereFrom'] == "myPatients":
        return redirect(url_for('myPatients'))
        
    return redirect(url_for('appointments'))

@app.route('/appointmentDetails', methods=['GET', 'POST'])
@needLogin
def appointmentAcceptDecline_view():
    """Gets the correct appointment to show the patient, handles the accept or decline option on appointments that they have been invited to by their carer"""
    if request.method == 'GET':
        appid = request.args.get('id')
        getApp = json.loads(getAppointment(session['username'], appid))
        return render_template('appointmentAcceptDecline.html', appointment=getApp)
    if request.method == 'POST':
        action = acceptDeclineAppointment(session['username'], request.form['action'], request.form['appid'])
        
        if request.form['action'] == "Accept":
            messageType = 'success'
        else: 
            messageType = 'danger'

        if action == "Failed": 
            messageType = 'danger'
        if action == "You have not been invited to this appointment.": 
            messageType = 'danger'

        getApp = json.loads(getAppointment(session['username'], request.form['appid']))
        return render_template('appointmentAcceptDecline.html', appointment=getApp, message=action, type=messageType)


@app.route('/myPatients')
@needLogin
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

    return render_template('myPatients.html', patients = patients, appointmentsMapping = appointmentsMapping, activePrescriptions = activePrescriptions, upcomingPrescriptions = upcomingPrescriptions, expiredPrescriptions = expiredPrescriptions, medicationList = Medication.select())

@app.route('/prescriptions')
@needLogin
def prescriptions():
    """Shows all the active prescriptions for the patient selected"""
    prescriptions = json.loads(getPrescriptions(session['username']))
    return render_template('prescriptions.html', prescriptions = prescriptions)

@app.route('/deletePrescription')
@needLogin
def deletePrescription_view():
    """Informs Carer that the prescription has been deleted from the selected patient"""
    prescriptionid = request.args.get('id')
    prescription = Prescription.select().where(Prescription.prescriptionid == prescriptionid).get()
    username = request.args.get('username')
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
@needLogin
def addPrescription_view():
    """Informs Carer that the prescription has been added to the selected patient"""
    result = addPrescription(request.form)
    username = request.form['username']
    if result != "Failed":
        flash(result, 'result')
        flash('success', 'class')
        flash(username, 'user')
        flash('prescription', 'type')
        return redirect(url_for('myPatients'))
    elif result == "Data is in the wrong format":
        flash('prescription', 'type')
        flash('danger', 'class')
        flash(result, 'result')
        flash(username, 'user')
        return redirect(url_for('myPatients'))
    else:
        flash('prescription', 'type')
        flash('danger', 'class')
        flash(result, 'result')
        flash(username, 'user')
        return redirect(url_for('myPatients'))

@app.route('/updatePrescription', methods=['POST'])
@needLogin
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

@app.route('/takePrescriptionWeb', methods=['POST'])
@needLogin
def takePrescriptionWeb():
    return takePrescription(request.form)

@app.route('/getPrescriptionCountWeb', methods=['POST'])
@needLogin
def getPrescriptionCountWeb():
    return getPrescriptionCount(request.form)

@app.route('/carerAppointments', methods=['POST', 'GET'])
@needLogin
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
@needLogin
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
      
        if added > 0: 
            flash("Appointment Added", 'success')
            return redirect(url_for('appointments'))        
    return render_template('myPatients.html', appType=Appointmenttype.select(), appointments=appointments, request=None)


@app.route('/nhsSearch', methods=['POST', 'GET'])
@needLogin
def searchNHS():
    """The POST request is no longer needed as this is done with Javascript"""
    # if request.method == 'POST':
    #     website = searchNHSDirect(request.form['searchterm'])
    #     webbrowser.open(website,new=2)
    return render_template('searchNHSDirect.html')

@app.route('/dismissNotification', methods=['POST', 'GET'])
@needLogin
def dismissNotifications():
    """Dismiss the notification by running a method from the API"""
    if request.method == 'POST':
        notificationDismiss = dismissNotification(request.form['notificationid'])
        return notificationDismiss 


@app.route('/notes',methods=['POST', 'GET'])
def notes():
    """JustHealth correspondence, shows notes between a patient and their carer"""
    connections = json.loads(getConnections(session['username']))    
    if request.method == "GET":
        try:
            # Get the notes for the patient and carer that are connected
            patient = request.args.get('user', '')
            Patientcarer.select().where((Patientcarer.carer == session['username']) & (Patientcarer.patient == patient)).get()
            correspondence = json.loads(getCorrespondence(session['username'], patient))
            return render_template('correspondence.html', notes=correspondence, patient=patient)
        except Patientcarer.DoesNotExist:
            # Patient/Carer relationship that's requested does not exist
            return redirect(url_for('index'))

@app.route('/addNote',methods=['POST', 'GET'])
def addNote():
    """Correspondence page, handles the form POST request to store a note between patient and carer"""
    patient = request.form['patient']
    if request.method == "POST":
        result = addCorrespondence(request.form)
        if result == "True":
            flash("Note successfully added", 'success')
        else:
            flash("Note could not be added", 'danger')
        return redirect("/notes?user=" + patient)

@app.route('/deleteNote', methods=['POST'])
def deleteNote_view():
    """Correspondence page, handles the POST request from the delete button to remove the correct note from the database"""
    patient = request.form['patient']
    noteid = request.form['noteid']
    deleted = deleteNote(noteid)
    if deleted == "Deleted":
        flash("Note successfully deleted", 'success')
    else:
        flash("Note could not be deleted", 'danger')
    return redirect("/notes?user=" + patient)

@app.route('/patientNotes',methods=['POST', 'GET'])
def patientNotes():
    if request.method == "GET":
        try:
            notes = json.loads(getPatientNotes(session))
            return render_template('patientNotes.html', notes=notes)
        except Patientcarer.DoesNotExist:
            return render_template('patientNotes.html')

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
  return "Unauthorised", 401

#Admin Portal pages
@app.route('/adminPortal')
@needLogin
@needAdmin
def adminPortal():
    """Loads the pages related to the tablist on the IM portal home page, this includes a list of active users, current medication list and deactivation options"""
    allUsers = json.loads(getAllUsers())
    deactivateReasons = json.loads(getReasons())
    carers = json.loads(str(Carer.select(Carer.username).count()))
    patients = json.loads(str(Patient.select(Patient.username).count()))     
    if request.method == 'POST':
        result = deactivateAccount(request.form)
        if allUsers['accounttype'] == "Patient":
            return render_template('adminHome.html', reasons = Deactivatereason.select(), reasonStats = deactivateReasons, allUsers = allUsers, printaccounttype = 'Patient', medicationList = Medication.select(), carers = carers, patients = patients)
    else: 
       return render_template('adminHome.html', reasons = Deactivatereason.select(), reasonStats = deactivateReasons, allUsers = allUsers, printaccounttype = 'Carer', medicationList = Medication.select(), carers = carers, patients = patients)

@app.route('/updateAccountSettings_view', methods=['POST'])
@needLogin
@needAdmin
def updateAccountSettings_view():
    if request.method == 'POST':
        #The tick boxes are not sent if they aren't ticked, so we have to catch them here.
        try:
            accountdeactivated = request.form['accountdeactivated']
            accountdeactivated = True
        except KeyError, e:
            accountdeactivated = False

        try:
            accountlocked = request.form['accountlocked']
            accountlocked = True
        except KeyError, e:
            accountlocked = False

        try:       
            verified = request.form['verified']
            verified = True
        except KeyError, e:
            verified = False

        result = updateAccountSettings(request.form, accountlocked, accountdeactivated, verified)

        if result == "True":
            flash('Account Settings Updated', 'success')
            return redirect(url_for('adminPortal'))
        else:
            flash('Update failed', 'danger')
            return redirect(url_for('adminPortal'))

@app.route('/deleteAccount', methods=['POST'])
@needLogin
@needAdmin
def deleteAccount_view():
    """Submits the form for an administrator to delete a user account from the management portal"""
    username = request.form['username']
    deleted = deleteAccount(username)
    if deleted == "Deleted":
        flash("User successfully deleted", 'success')
    else:
        flash("User could not be deleted", 'danger')
    return redirect("/adminPortal")

@app.route('/addNewDeactivate', methods=['POST'])
@needLogin
@needAdmin
def addNewDeactivate():
    """Submits the form to add a new deactivation reason to the database"""
    if request.method == 'POST':
        result = addDeactivate(request.form)  
        if result == "True":
            return render_template('adminHome.html',type="success", message = 'Deactivate Reason Added')
        else: render_template('adminHome.html',type="warning", message = 'Update failed')
    else: 
       return render_template('adminHome.html')

@app.route('/addNewMedication', methods=['POST'])
@needLogin
@needAdmin
def addNewMedication():
    """Submits the form to add a new medication name to the database"""
    if request.method == 'POST':
        result = newMedication(request.form)  
        if result == "True":
            return render_template('adminHome.html',type="success", message = 'Medication Added')
        else: render_template('adminHome.html',type="warning", message = 'Update failed')
    else:   
       return render_template('adminHome.html')

import datetime
@app.route('/test', methods=['POST', 'GET'])
def test():
    return str(addReminders('sophie15', datetime.datetime.now()))
