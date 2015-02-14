========================
Full Views Listing
========================

Listed below is the complete list of views for the JustHealth web application, broken down by their general function.

Each method will show its:

- URL
- Primary function
- Method type (POST or GET)
- POST / GET parameters
- Possible return values

------------------------
User Login
------------------------

.. autofunction:: justHealthServer.views.login

  :URL: /login
  :HTTP_METHOD: POST, GET

  :param username: Checks username is valid, posts to authenticate() API

Return values:
    - Redirects to appropriate home page for user
    - Fields not filled in/Input not valid

Home
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: justHealthServer.views.index

  :URL: /

  :param accounttype: Checks the type of account user has registered with

Return values:
  patienthome.html
    - Sends the user to a home page designed specifically for a patient's needs.
  carerhome.html
    - Sends the user to a home page designed specifically for a carer's needs, simplifying the administrative work involved with care.

------------------------
Profile
------------------------

.. autofunction:: justHealthServer.views.profile

  :URL: /profile

  :param username: Gets user's details assigned to their username

Return values:
  profile.html
    - Shows user details and existing connections.

Edit Profile
^^^^^^^^^^^^^^^^^^^^^^^^

(Show source here when edit profile is complete)

------------------------
Register
------------------------

.. autofunction:: justHealthServer.views.registration

  :URL: /register
  :HTTP_METHOD: POST, GET

Return values:
  login.html
    - Success: "Thanks for registering! Please check your email for a verification link"
  register.html
    - Failed: Fields not filled in/Input not valid

------------------------
Search
------------------------

.. autofunction:: justHealthServer.views.search

  :URL: /search
  :HTTP_METHOD: POST, GET

  :param username: Finds user assigned by their username

Return values:
  search.html
    - Shows any users found that match the search term.

------------------------
Deactivate
------------------------

.. autofunction:: justHealthServer.views.deactivate

  :URL: /deactivate
  :HTTP_METHOD: POST, GET

  :param username: Finds account by username

Return values:
  "Your account has been deleted"
    - User account is deleted and all information is removed from the database.
  "Your account has been deactivated"
    - User account is deactivated and their information remains in the database.
  Deactivation failed
    - Fields not filled in/Input not valid

------------------------
Legal
------------------------

.. autofunction:: justHealthServer.views.legal

  :URL: /legal

Return values:
  legal.html
    - Links to each of the JustHealth legal documents.

Terms and Conditions
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: justHealthServer.views.terms

  :URL: /termsandconditions

Return values:
  termsandconditions.html
    - Shows JustHealth terms and conditions.

Privacy Policy
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: justHealthServer.views.privacy

  :URL: /privacypolicy

Return values:
  privacypolicy.html
    - Shows JustHealth privacy policy.

------------------------
User Logout
------------------------

.. autofunction:: justHealthServer.views.logout

  :URL: /logout

Return values:
  Redirect to JustHealth home

------------------------
User Verification
------------------------

.. autofunction:: justHealthServer.views.verifyUser

  :URL: /users/activate/<payload>

Return values:
  "Thank you for verifying your account."
    - Link directs user to login.html

------------------------
Forgot Password
------------------------

.. autofunction:: justHealthServer.views.forgotPassword

  :URL: /forgotPassword
  :HTTP_METHOD: POST, GET

  :param email: Finds user account from valid email

Return values:
  "An account with this email address does not exist."
    - Message shown if email address is not found in the database.
  "An email has been sent to you containing a link, which will allow you to reset your password."
    - Message informs the user that they can successfully reset their password.

------------------------
Password Reset
------------------------

.. autofunction:: justHealthServer.views.resetPasswordRedirect

  :URL: /resetpassword
  :HTTP_METHOD: POST, GET

  :param resetPassword(): Allows user to reset password if ``"True"``

Return values:
  "Your password has been reset, please check your email and click the link to verify."
    - Successful password reset, user has to click the link in their email to prove the reset was them.
  Failed
    - Fields not filled in/Input not valid

------------------------
Appointments
------------------------
Patient Appointments
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: justHealthServer.views.appointments

  :URL: /appointments
  :HTTP_METHOD: POST, GET

  :param details: All appointment details must be filled in for the database entry

Return values:
  "Appointment Added"
    - Successfully added appointment.
  Failed
    - patientAppointments.html form is shown for user to try again.

Carer Appointments
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: justHealthServer.views.carerappointments

  :URL: /carerAppointments
  :HTTP_METHOD: POST, GET

  :param details: All appointment details must be filled in for the database entry

Return values:
  "Appointment Added"
    - Successfully added appointment.
  Failed
    - carerAppointments.html form is shown for user to try again.

Invitee Appointments
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: justHealthServer.views.inviteeappointments

  :URL: /inviteeappointments
  :HTTP_METHOD: POST, GET

  :param details: All appointment details must be filled in for the database entry

Return values:
  Success
    - Successfully added appointment to individual patient.
  Failed
    - My Patients page with appointment form is shown for user to try again.

Update Appointment
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: justHealthServer.views.getUpdateAppointment_view

  :URL: /updateAppointment
  :HTTP_METHOD: POST, GET

  :param appid: Uses the appointment ID to show the existing data in the form
  :param updateAppointment: All appointment details must be filled in for the database entry

Return values:
  Success/Updated
    - Successfully updated the appointment information.
  Failed
    - Appointment page with form is shown for user to try again.

Delete Appointment
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: justHealthServer.views.deleteAppointment_view

  :URL: /deleteAppointment
  :HTTP_METHOD: POST, GET

  :param appid: Uses the appointment ID to delete a specific appointment

Return values:
  Success/Deleted
    - Successfully deleted appointment to individual patient.
  Failed
    - Appointment page with form is shown for user to try again.

------------------------
My Patients
------------------------

.. autofunction:: justHealthServer.views.myPatients

  :URL: /myPatients

  :param username, accounttype: The carer's username is needed to pull the list of connected patients from the database

Return values:
  myPatients.html
    - Page is shown listing all the carer's connected patients, with their active prescriptions and appointments listed.

------------------------
Prescriptions
------------------------

.. autofunction:: justHealthServer.views.prescriptions

  :URL: /prescriptions

  :param username: Patient's medication is stored in the database associated with their username

Return values:
  prescriptions.html
    - Page is shown listing current medication prescribed to the patient.

Add Prescription
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: justHealthServer.views.addPrescription_view

  :URL: /addPrescription
  :HTTP_METHOD: POST

  :param username: Patient's medication is stored in the database associated with their username

Return values:
  Success/Added
    - myPatients.html, new prescription is shown for individual patient
  Failed
    - "Could not add prescription"

Delete Prescription
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: justHealthServer.views.deletePrescription_view

  :URL: /deletePrescription

  :param username: Patient's medication is stored in the database associated with their username
  :param prescriptionid: Uses the prescription ID to delete a specific prescription

Return values:
  Success/Deleted
    - ``"Deleted " + prescription.medication.name + " (" + str(prescription.quantity) + "x" + str(prescription.dosage) + ") " + prescription.dosageunit + " for " + username``
  Failed
    - myPatients.html, shows the prescription still exists
  

Update Prescription
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: justHealthServer.views.updatePrescription_view

  :URL: /updatePrescription
  :HTTP_METHOD: POST

  :param username: Patient's medication is stored in the database associated with their username
  :param prescriptionid: Uses the prescription ID to update a specific prescription

Return values:
  Success/Updated
    - myPatients.html, shows the updated prescription for the selected patient
  Failed
    - myPatients.html, shows the prescription with no changes

------------------------
Error Handling
------------------------

.. autofunction:: justHealthServer.views.internal_error

Return Values
  The following errors are handled with appropriate images:
    - 500
    - 408
    - 404
    - 400
    - 401

------------------------
JustHealth Admin Portal
------------------------

Admin Portal Home
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: justHealthServer.views.adminPortal

  :URL: /adminPortal
  :HTTP_METHOD: POST

  :param accounttype: Needed to display the user's accounttype in user statistics

Return values:
  adminHome.html
    - Shows the page with all tabs and content loaded for user accounts

New Deactivation Reason
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: justHealthServer.views.addNewDeactivate

  :URL: /addNewDeactivate
  :HTTP_METHOD: POST

Return values:
  adminHome.html, "Success"
    - "Deactivate Reason Added"
  adminHome.html, "Warning"
    - "Update failed"

New Medication Name
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: justHealthServer.views.addNewMedication

  :URL: /addNewMedication
  :HTTP_METHOD: POST

Return values:
  adminHome.html, "Success"
    - "Medication Added"
  adminHome.html, "Warning"
    - "Update failed"