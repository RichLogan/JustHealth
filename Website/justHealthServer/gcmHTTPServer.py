from justHealthServer import *
from api import *
import json
import requests

def sendPushNotification(username, title, message):
  """Sends a push notification to the users Android device with the specified title and message"""
  # Get Registration ID
  registrationid = Androidregistration.select().where(Androidregistration.username == username).get().registrationid

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
    return True
  return False