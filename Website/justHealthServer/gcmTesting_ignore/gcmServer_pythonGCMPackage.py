# from gcm import GCM

# gcm = GCM('AIzaSyCLEJR4te1Y6i2hJa7mOhkeFkTzBbWfZ9Y')
# data = {'variable': 'Hello', 'variable2': 'World'}

# # Plaintext request
# reg_id = 'APA91bFSdGrImn8cmDmRxmp5cdxlj9cACubPJzZlOCbZPDEa5k3gOW6T1tKbATFRR3L6F62W22X8c-TBKBbiV1sSdGrr78cx4gkyKwtGUT6UL7U5KSQ4d1h35kSOrE5AYFo5QXN_dyKTNqBg87SspZeh1vCEFLKrhw'
# response = gcm.plaintext_request(registration_id=reg_id, data=data)
# print response

# # JSON request
# reg_ids = ['12', '34', '69']
# response = gcm.json_request(registration_ids=reg_ids, data=data)

# # Extra arguments
# res = gcm.json_request(
#     registration_ids=reg_ids, data=data,
#     collapse_key='uptoyou', delay_while_idle=True, time_to_live=3600
# )

# import requests, json
# json_data = {
# 	"collapse_key": "JustHealth",
#  	"data" : {
#  		"message": "ciao",
# 	}, 
# 	"registration_ids": ['APA91bHrGv8mDeXasNNtzEozM4650yjFZEv_SJVZw7oQy_PgJRqb0v_bLBnSm4Vr5crDMkDv2AmgXFtmPPf6Avf7Kaa7umbpgSttK8jjYqq0kg-s8EEJ7v4ozIvHu-PZEziUsQFKhCvG6tElF_7wjCM9Hx0Ht127qnKgAgu9VzAqEPwHRgsMDhU'],
# }
# url = 'https://android/googleapis.com/gcm/send'
# myKey = "AIzaSyCLEJR4te1Y6i2hJa7mOhkeFkTzBbWfZ9Y"
# data = json.dumps(json_data)
# headers = {'Content-Type': 'application/json', 'Authorization': 'key=%s' % myKey}
# req = urllib2.Request(url, data, headers)
# f = urllib2.urlopen(req)
# response = json.loads(f.read())
# print response

# import requests, json
# headers = {
# 	'content-type' : 'application/json',
# 	'Authorization' : "key=AIzaSyCLEJR4te1Y6i2hJa7mOhkeFkTzBbWfZ9Y"

# payload = {
# 	"collapse_key" : "JustHealth",
# 	"data" : {
# 		"message" : "ciao"
# 	},
# 	"registration_ids": ['APA91bFSdGrImn8cmDmRxmp5cdxlj9cACubPJzZlOCbZPDEa5k3gOW6T1tKbATFRR3L6F62W22X8c-TBKBbiV1sSdGrr78cx4gkyKwtGUT6UL7U5KSQ4d1h35kSOrE5AYFo5QXN_dyKTNqBg87SspZeh1vCEFLKrhw']
# }
# r = requests.post('https://android.googleapis.com/gcm/send', data=json.dumps(payload), headers=headers)
# print r.text