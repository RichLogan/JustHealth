from justHealthServer import app
from database import *
from flask import request
import api
import json
import requests


@app.route('/api/saveAndroidRegistrationID', methods=['POST'])
#need to add decorator here
def saveAndroidRegistrationID():
    username = request.form['username']
    registrationID = request.form['registrationid']

    try: 
        checkExisting = Androidregistration.select().where(Androidregistration.username == username).get()
    except Androidregistration.DoesNotExist:
        checkExisting = None

    if checkExisting != None:
        update = Androidregistration.update(
            registrationid = registrationID
            ).where(Androidregistration.username == username)

        with database.transaction():
            update.execute()
            return "True"
        return "Failed"
    else:
        insert = Androidregistration.insert(
            username = username,
            registrationid = registrationID
            )

        with database.transaction():
            insert.execute()
            return "True"
        return "Failed"

def createPushNotification(notificationid):
  """Creates a push notification, that can be sent to the users android device"""
  notification = Notification.select().dicts().where(Notification.notificationid == notificationid).get()
  username = notification['username']
  title = notification['notificationtype']
  content = getAndroidNotificationContent(notification)
  if content == "DoesNotExist":
    return None
  else:
    sendPushNotification(username, title, content)

def sendPushNotification(username, title, message):
  """Sends a push notification to the users Android device with the specified title and message"""
  # Get Registration ID
  try:
    registrationid = Androidregistration.select().where(Androidregistration.username == username).get().registrationid
  except Androidregistration.DoesNotExist:
    return "False"

  # Build Message
  headers = {
  'content-type' : 'application/json',
  'Authorization' : "key=" + app.config['GCM_API_KEY']
  }
  payload = {
    "data" : {
      "title" : title,
      "message" : message
    },
    "registration_ids": [registrationid]
  }
  
  # Post to google
  r = requests.post('https://android.googleapis.com/gcm/send', data=json.dumps(payload), headers=headers)

  # Check result
  result = json.loads(r.text)
  if (result['success'] == 1) and (result['failure'] == 0):
    return "True"
  return "False"

@app.route('/api/deleteAndroidRegistrationID', methods=['POST'])
#Need to add decorator here
def deleteAndroidRegID():
  username = request.form['username']
  regId = request.form['registrationid']
  registration = Androidregistration.select().where((Androidregistration.username == username) and (Androidregistration.registrationid == regId)).get()

  with database.transaction():
    registration.delete_instance()
    return "True"
  return "False"

def getAndroidNotificationContent(notification):
    """gets the body/content of the notification"""
    if notification['notificationtype'] == "Connection Request":
        try: 
            requestor = Relationship.select().where(Relationship.connectionid == notification['relatedObject']).get()
        except Relationship.DoesNotExist:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = "You have a new connection request from " + requestor.requestor.username
    
    if notification['notificationtype'] == "New Connection":
        content = "You have a new connection, click above to view."
    
    if notification['notificationtype'] == "Prescription Added":
        try:
            prescription = Prescription.select().where(Prescription.prescriptionid == notification['relatedObject']).get()
        except Prescription.DoesNotExist:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = "A new prescription for " + prescription.medication.name + " has been added to your profile."

    if notification['notificationtype'] == "Prescription Updated":
        try:
            prescription = Prescription.select().where(Prescription.prescriptionid == notification['relatedObject']).get()
        except Prescription.DoesNotExist:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = "Your prescription for " + prescription.medication.name + " has been updated."
    
    if notification['notificationtype'] == "Appointment Invite":
        try:
            appointment = Appointments.select().where(Appointments.appid == notification['relatedObject']).get()
        except Appointments.DoesNotExist:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = appointment.creator.username + " has added an appointment with you on " + str(appointment.startdate) + "."

    if notification['notificationtype'] == "Appointment Updated":
        try:
            appointment = Appointments.select().where(Appointments.appid == notification['relatedObject']).get()
        except Appointments.DoesNotExist:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = appointment.creator.username + " has updated the following appointment with you: " + str(appointment.name) + "."

    if notification['notificationtype'] == "Appointment Cancelled":
        content = "One of your appointments has been cancelled, click above to view your updated calendar."

    if notification['notificationtype'] == "Password Reset":
        content = "Your password has been changed successfully."

    if notification['notificationtype'] == "Medication Low":
        try:
            prescription = Prescription.select().where(Prescription.prescriptionid == notification['relatedObject']).get()
        except Prescription.DoesNotExist:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = prescription.username.username + "'s prescription for " + prescription.medication.name + " is running low."

    if notification['notificationtype'] == "Appointment Accepted":
        try:
            appointment = Appointments.select().where(Appointments.appid == notification['relatedObject']).get()
        except Appointments.DoesNotExist:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = appointment.invitee.username + " has accepted the appointment with you on " + str(appointment.startdate) + "."

    if notification['notificationtype'] == "Appointment Declined":
        try:
            appointment = Appointments.select().where(Appointments.appid == notification['relatedObject']).get()
        except Appointments.DoesNotExist:
            doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
            with database.transaction():
                doesNotExist.delete_instance()
                return "DoesNotExist"
        content = appointment.invitee.username + " has declined the appointment with you on " + str(appointment.startdate) + "."

    if notification['notificationtype'] == "Medication Low":
      try:
        prescription = Prescription.select().where(Prescription.prescriptionid == notification['relatedObject']).get()
      except Prescription.DoesNotExist:
        doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
        with database.transaction():
          doesNotExist.delete_instance()
          return "DoesNotExist"
      content = "You have less than 3 days stock of " + prescription.medication.name + " left."

    if notification['notificationtype'] == "Patient Medication Low":
      try:
        prescription = Prescription.select().where(Prescription.prescriptionid == notification['relatedObject']).get()
      except Prescription.DoesNotExist:
        doesNotExist = Notification.get(Notification.notificationid == notification['notificationid'])
        with database.transaction():
          doesNotExist.delete_instance()
          return "DoesNotExist"
      content = prescription.username.username + " has less than 3 days stock of " + prescription.medication.name + " left."

    if notification['notificationtype'] == "Missed Prescription":
      try:
        takeInstance = TakePrescription.select().where(TakePrescription.takeid == notification['relatedObject']).get()
        prescription = Prescription.select().where(Prescription.prescriptionid == takeInstance.prescriptionid).get()
      except Prescription.DoesNotExist:
        doesNotExist = Notification.get(Notification.notificationid == prescriptionid)
        with database.transaction():
          doesNotExist.delete_instance()
          return "DoesNotExist"
    content = "You only took " + str(takeInstance.currentcount) + " out of " + str(prescription.frequency) + " on " + str(takeInstance.currentdate)

    if notification['notificationtype'] == "Carer Missed Prescription":
      try:
        takeInstance = TakePrescription.select().where(TakePrescription.takeid == notification['relatedObject']).get()
        prescription = Prescription.select().where(Prescription.prescriptionid == takeInstance.prescriptionid).get()
      except Prescription.DoesNotExist:
        doesNotExist = Notification.get(Notification.notificationid == prescriptionid)
        with database.transaction():
          doesNotExist.delete_instance()
          return "DoesNotExist"
    content = "Your patient " + str(prescription.username) + " only took " + str(takeInstance.currentcount) + " out of " + str(prescription.frequency) + " on " + str(takeInstance.currentdate)
    
    return content
