import requests, json
headers = {
	'content-type' : 'application/json',
	'Authorization' : "key=AIzaSyCLEJR4te1Y6i2hJa7mOhkeFkTzBbWfZ9Y"

payload = {
	"collapse_key" : "JustHealth",
	"data" : {
		"message" : "ciao"
	},
	"registration_ids": ['APA91bFSdGrImn8cmDmRxmp5cdxlj9cACubPJzZlOCbZPDEa5k3gOW6T1tKbATFRR3L6F62W22X8c-TBKBbiV1sSdGrr78cx4gkyKwtGUT6UL7U5KSQ4d1h35kSOrE5AYFo5QXN_dyKTNqBg87SspZeh1vCEFLKrhw']
}
r = requests.post('https://android.googleapis.com/gcm/send', data=json.dumps(payload), headers=headers)
print r.text