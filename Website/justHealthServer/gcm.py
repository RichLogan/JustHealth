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
	username = notification['username'	]
	title = notification['notificationtype']
	content = api.getNotificationContent(notification)

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
