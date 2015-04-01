========================
Full API Listing
========================

Listed below is the complete list of possible API functionality provided by JustHealth, broken down by their general function.

All API calls require valid HTTP Basic Authentication using a registered username and encrypted password unless otherwise noted. When there is a single parameter, usually called 'details', it is a list of all post request data. The individual field will be noted in the description by [ ]. 

---------
Accounts
---------

.. autofunction:: justHealthServer.api.registerUser

.. autofunction:: justHealthServer.api.usernameCheck

.. autofunction:: justHealthServer.api.authenticate

.. autofunction:: justHealthServer.api.deactivateAccount

.. autofunction:: justHealthServer.api.resetPassword

.. autofunction:: justHealthServer.api.getProfilePictureAPI

.. autofunction:: justHealthServer.api.getAccountInfo

.. autofunction:: justHealthServer.api.getCarers

.. autofunction:: justHealthServer.api.setProfilePicture

.. autofunction:: justHealthServer.api.editProfile

.. autofunction:: justHealthServer.api.changePasswordAPI

.. autofunction:: justHealthServer.api.lockAccount

.. autofunction:: justHealthServer.api.passwordExpiration

.. autofunction:: justHealthServer.api.expiredResetPassword

----------------
Email Functions
----------------

.. autofunction:: justHealthServer.api.getSerializer

.. autofunction:: justHealthServer.api.sendVerificationEmail

.. autofunction:: justHealthServer.api.getUserFromEmail

.. autofunction:: justHealthServer.api.sendForgotPasswordEmail

.. autofunction:: justHealthServer.api.sendUnlockEmail

.. autofunction:: justHealthServer.api.sendPasswordResetEmail

.. autofunction:: justHealthServer.api.sendContactUs

-------------
Appointments
-------------

.. autofunction:: justHealthServer.api.addPatientAppointment

.. autofunction:: justHealthServer.api.addInviteeAppointment

.. autofunction:: justHealthServer.api.getAllAppointments

.. autofunction:: justHealthServer.api.deleteAppointment

.. autofunction:: justHealthServer.api.getUpdateAppointment

.. autofunction:: justHealthServer.api.updateAppointment

.. autofunction:: justHealthServer.api.getAppointment

.. autofunction:: justHealthServer.api.acceptDeclineAppointment

.. autofunction:: justHealthServer.api.addAndroidEventId

--------------
Connnections
--------------

.. autofunction:: justHealthServer.api.searchPatientCarer

.. autofunction:: justHealthServer.api.getConnectionStatus

.. autofunction:: justHealthServer.api.createConnection

.. autofunction:: justHealthServer.api.completeConnection

.. autofunction:: justHealthServer.api.cancelRequest

.. autofunction:: justHealthServer.api.deleteConnection

.. autofunction:: justHealthServer.api.getConnections

--------------
Prescriptions
--------------

.. autofunction:: justHealthServer.api.addPrescription

.. autofunction:: justHealthServer.api.editPrescription

.. autofunction:: justHealthServer.api.deletePrescription

.. autofunction:: justHealthServer.api.getPrescriptions

.. autofunction:: justHealthServer.api.getActivePrescriptions

.. autofunction:: justHealthServer.api.getUpcomingPrescriptions

.. autofunction:: justHealthServer.api.getExpiredPrescriptions

.. autofunction:: justHealthServer.api.getPrescription

.. autofunction:: justHealthServer.api.takePrescription

.. autofunction:: justHealthServer.api.checkStockLevel

.. autofunction:: justHealthServer.api.getPrescriptionCount

--------------
Notifications
--------------

.. autofunction:: justHealthServer.api.createNotificationRecord

.. autofunction:: justHealthServer.api.getNotifications

.. autofunction:: justHealthServer.api.getAllNotifications

.. autofunction:: justHealthServer.api.getDismissedNotifications

.. autofunction:: justHealthServer.api.getNotificationContent

.. autofunction:: justHealthServer.api.getNotificationLink

.. autofunction:: justHealthServer.api.getNotificationTypeClass

.. autofunction:: justHealthServer.api.dismissNotification

----------
Reminders
----------

.. autofunction:: justHealthServer.api.getMinutesDifference

.. autofunction:: justHealthServer.api.getAppointmentsDueIn30

.. autofunction:: justHealthServer.api.getAppointmentsDueNow

.. autofunction:: justHealthServer.api.getPrescriptionsDueToday

.. autofunction:: justHealthServer.api.checkMissedPrescriptions

.. autofunction:: justHealthServer.api.addReminders

.. autofunction:: justHealthServer.api.deleteReminders

.. autofunction:: justHealthServer.api.getReminders

----------------
Correspondence
----------------

.. autofunction:: justHealthServer.api.getCorrespondence

.. autofunction:: justHealthServer.api.getPatientNotes

.. autofunction:: justHealthServer.api.addCorrespondence

.. autofunction:: justHealthServer.api.deleteNote

------
Admin
------

.. autofunction:: justHealthServer.api.addMedication

.. autofunction:: justHealthServer.api.deleteMedication

.. autofunction:: justHealthServer.api.getMedications

.. autofunction:: justHealthServer.api.addDeactivate

.. autofunction:: justHealthServer.api.newMedication

.. autofunction:: justHealthServer.api.getReasons

.. autofunction:: justHealthServer.api.getAllUsers

.. autofunction:: justHealthServer.api.updateAccountSettings

.. autofunction:: justHealthServer.api.deleteAccount

---------
Security
---------
.. autofunction:: justHealthServer.api.verify_password

.. autofunction:: justHealthServer.api.getUsernameFromHeader

.. autofunction:: justHealthServer.api.verifyContentRequest

.. autofunction:: justHealthServer.api.verifySelf

.. autofunction:: justHealthServer.api.verifyCarer

.. autofunction:: justHealthServer.api.encryptPassword

.. autofunction:: justHealthServer.api.decryptPassword

-----------------
System Functions
-----------------

.. autofunction:: justHealthServer.api.searchNHSDirect

.. autofunction:: justHealthServer.api.getDeactivateReasons

.. autofunction:: justHealthServer.api.getAppointmentTypes

.. autofunction:: justHealthServer.api.createTakePrescriptionInstances

.. autofunction:: justHealthServer.api.pingServer

.. autofunction:: justHealthServer.api.generation