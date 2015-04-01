========================
Security Documentation
========================

------------------------
Introduction
------------------------

In order for JustHealth to be reputable, trusted and widely used it is necessary to ensure that patient confidentiality, data integrity and the availability of this data is exceptional. Therefore, JustHealth has implemented a strict security policy and implemented  security controls to ensure that the product meets customer expectation. 


------------------------
HTTPS
------------------------

JustHealth set out to implement HTTPS on the webserver that was hosting the application. This would have ensured that all of the communication between a client's browser and/or any Android device that they may be running the JustHealth mobile application would have been encrypted via SSL. JustHealth made the decision to utilise this protocol rather than standard HTTP as it ensures that user data is encrypted when being transmitted across the internet. This would have helped to ensure that the confidentiality of patient data is maintained.  
 
If the application had been hosted on our own server, this would have been implemented successfully. However, due to it being run on the University webserver (raptor) we were unable to use signed certificates. Despite using self-signed certificates, we found this was not supported with Android without implementing several exceptions. Therefore, the decision was made to not implement this. Although, below are the certificates that we have generated in order to prove that we the security could have been implemented on the web application providing we had deployed on our own server. 

**The Key:**
::

    -----BEGIN RSA PRIVATE KEY-----
    MIIEpAIBAAKCAQEAxyi4TLCJZwd9CmOZGDTYeo+bE/oyfMeeJUzzL9JH1xuezNr9
    vFHbPlsToHN1xDYjuf7en7GXVAr8sEaTJGo4zkfIWR8gMNvahIx9DvRsiVDtk32f
    qZyiDXYJK0nX6nH5r2bBN1jIAOswJ9rv068oCW5PEweUTUjEPxM1UoJMetChchke
    /rNGlRyt5SKB0XKqsqHXWGpHO6GNlycYH/cRF8D/ygPOlmnD+dbiLhkovLFkzuOf
    uXkpT/bfxrX0Zd/8zINvjEzCyiarOoRnGSlxj9MpXj6FdYL02haO56zhPZW7Sl91
    y+PezSOyHmgzATvQ8PdDBf88KSH3SLlWMoeP/QIDAQABAoIBAQC1cHmHFIX5YS8f
    meFN1kcqUU5dAuGgIFQJc3NSK+bbKASiaRgkywZMZrkYwleV7CTcPEAhiK9vF5ti
    FMnUsRkThP4Xg23WVVVc0IjWaQPAjgQDDL26zkIstU5hK6MTqcZpb9mzTKTZgWqb
    xLAdUEPPY7mSgqMvTY3MUPmRM7ftYi1fBhf1jsCIk2h5VVwwZKMd9IhF5Ar6fkZl
    T+5hMauf6ec7kucCl14wZGmCjw+bKxGi9xmdPXkZJUNbS7mIjo4aJeFL9JX2ZB+I
    iQoTefNokd6wV2DBldpFUL0h1OAoprgN84SI+q1U6RqgcrzV/ygh1uPAhKipi5Fx
    GwvnxCRBAoGBAOSbwsmLkP+3onjOBEPodn02xzfWV8x5q0F4vRxuHPFGYSQUvZxR
    KvIEvcDaCbnuSJY9l60FKjn/hGxEoqJmvju5Fb0Eae9loQWD4fWglBAMGkUJBQe5
    smoHGEJq7jEhWpSplSYrNwFOId4y2sXtaUKOAmcofIReMYBa8vXh1yyJAoGBAN8F
    pCRvPNWUPEwjPpB7tK/i+5GQENiyx0H51rYeOiXHjsTh/EqeOu6iaXtOLNZGh7Ee
    oenaZTiAkgYD/vnboSfHpe/allV+ZL53tvhTJujQcMArdCi0dFCiqrrkexsJ0xgz
    k5BcYD48h3Wi0936NTtzNgHvDdSw1/GCtaQxtvLVAoGABQ0L+LgEtCGyjUi//2Ab
    fhi/vhQWTIZDqmaohwBH02ziqJFsvw9sC3zfVGt824bQQ8GIoGIE1NM4ccvya/Qp
    L9ifClYWoRt1u1F2pJ6vpssdqXjRi6ImtwEBIDaMnLlH7xDwIq/Bv12ike49tzHP
    qZDJrM3QMnyCS3u28ofS4UECgYBj+SFle7/ndfW5o6ruFaYfmj5vOAd1PF76Akbv
    iIlEWjpzo2H3CQsd4gwqzBZpT2CQU0z9iXsKYwgSTkREOOH69RI7fN8bH/eFMiEB
    HDU69AU2/8OoY4wogWLLOJS+wB6yoJwrgF1cSMHoR791qC2oorK5FzI5/7QtfQxz
    uB1sqQKBgQCZ/y482vPfXZ8tKdNHgG5BJehlHbhxzmeW9If2NoF+9ybXcDvKXkvz
    mHffRaWFgtX6zgSUh9TQqocRZERiLydU+3Mp1RDObE7kftE3OhhZxhzIlDwDDVnB
    npUQPK4YxK7hv27XbApfmWIU6MEAmxIhb8rhbyxoVXu6Ba7am3DoPg==
    -----END RSA PRIVATE KEY-----

 
**The Certificate:** 
::

    -----BEGIN CERTIFICATE-----
    MIIDXTCCAkWgAwIBAgIJAMuJH8m+dN+jMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
    BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
    aWRnaXRzIFB0eSBMdGQwHhcNMTUwMTI0MTYxNzExWhcNMTYwMTI0MTYxNzExWjBF
    MQswCQYDVQQGEwJBVTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50
    ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
    CgKCAQEAxyi4TLCJZwd9CmOZGDTYeo+bE/oyfMeeJUzzL9JH1xuezNr9vFHbPlsT
    oHN1xDYjuf7en7GXVAr8sEaTJGo4zkfIWR8gMNvahIx9DvRsiVDtk32fqZyiDXYJ
    K0nX6nH5r2bBN1jIAOswJ9rv068oCW5PEweUTUjEPxM1UoJMetChchke/rNGlRyt
    5SKB0XKqsqHXWGpHO6GNlycYH/cRF8D/ygPOlmnD+dbiLhkovLFkzuOfuXkpT/bf
    xrX0Zd/8zINvjEzCyiarOoRnGSlxj9MpXj6FdYL02haO56zhPZW7Sl91y+PezSOy
    HmgzATvQ8PdDBf88KSH3SLlWMoeP/QIDAQABo1AwTjAdBgNVHQ4EFgQUbYQVxLIs
    i0i5Tk4KBxyUFldOLxcwHwYDVR0jBBgwFoAUbYQVxLIsi0i5Tk4KBxyUFldOLxcw
    DAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEAP6HN+3+w9eqi6prF5u5d
    mDpA4kUft1Zdowg+m4QhTMYGcyyt/jY+MAxltqF3wwtTWX1nrLiELEK+HD8Zcn8n
    frh38Fy/WvX1qfMeCwVzWWfSY/LCfDyxq5b/YmZTUN7Jc7aYqLJKMuNnYoLaFCb8
    BzXUuyp2oU8oGVSMj0Lf5/66Tyx4YWOcLUA4pbLqKUSeT+LeHsL7SR+fvRH6RXTA
    kmoBhJARajvUvNo6bSM8fIXAD53IS0pLpAo7mSBWuAvHYnJ/AhNRxl+UuEM28LtL
    If+kh/uGxhfF0NfDuFJLa8ntJTfg8Ef7+KdMfLoF/o0nPH17nIMSmfcknRokwpj3
    nA==
    -----END CERTIFICATE-----


We would have implemented Transport Layer Security 1.2 (TLS 1.2), which is currently viewed as being the most secure application layer security protocol that is able to be implemented on the web. It is not vulnerable to the recently publicised and discovered POODLE vulnerability. 


------------------------
Password Security
------------------------

Password Security has been extremely important to JustHealth and therefore, all user passwords are hashed in the database. This ensures that even administrators would not be able to convert the password to plaintext. This is important as although it is not advised users of JustHealth are likely to use their JustHealth login credentials on other accounts that they have. Although, very unlikely, if the JustHealth database was to be compromised it would not be feasible for a hacker to be able to convert passwords to plaintext. 
 
The hashing algorithm that JustHealth have adopted is the same one that is utilised by the Linux Operating System. This is a python algorithm named: SHA-256 Crypt. Currently, there are no known weaknesses or vulnerabilities. JustHealth make a conscious effort to review this regularly and if there are any vulnerabilities that come to light JustHealth will address this.  
 
Example of the implementation code: 
python:type::

    # Encrypt password with SHA 256
    profile['password'] = sha256_crypt.encrypt(profile['password'])

Example of the password "hello", stored as a hash: ::

	$5$rounds=110000$u.CYQ7BoQbYoEyCi$hzbrZqkoKPdHeVaWvCuZnastY17W/oenJudbcdcOwj2

 
When a user logs into the JustHealth web or mobile application the password that they enter into the field is also Hashed in the same way and compared to their hashed password that is stored in JustHealths database.  
 
Example of the code used to authenticate a user at login:
python:type::

	hashedPassword = uq8LnAWi7D.get((uq8LnAWi7D.username == attempted.username) & (uq8LnAWi7D.iscurrent==True)).password.strip()
        attemptedPassword = request.form['password']
        # This checks that the password that they have entered is the same as the password that is stored in the database.
        if sha256_crypt.verify(attemptedPassword, hashedPassword):
        	#other checks that check that the account is verified etc. 
 
Additionally, to avoid plaintext passwords being stored within the android application on login, the password is encrypted by a method in the API and then this is stored in the Android Application's Shared Preferences. This is required to be stored by the application so that it is able to authenticate with the API through HTTP Basic. The encryption and decryption method are able to be seen below.

**Encryption Method**
python:type::

    @app.route("/api/encryptPassword", methods=["POST"])
    def encryptPassword():
        """
        Encrypts the users password and returns it to them

        :param request.form: POST request containing plaintext [password].
        :type request.form: dict.

        :returns: str -- Encrypted password.
        """
        # Used so that we are able to store the encrypted users password in android SharedPreferences
        plaintext = request.form['password']
        cipherText = encrypt(app.secret_key, plaintext)
        stringCipher = binascii.hexlify(cipherText)
        return stringCipher

**Decryption Method** ::
python:type::

    def decryptPassword(cipherText):
    """
    Decrypts the users password and returns it so that we are able to authenticate them.

    :param cipherText: Encrypted password.
    :type cipherText: str.

    :returns: str -- Plaintext password.
    """
    #used so that we are able to store the encrypted users password in android SharedPreferences
    bytesCipher = binascii.unhexlify(cipherText)
    plaintext = decrypt(app.secret_key, bytesCipher)
    return plaintext


--------------------------------
API Authentication
--------------------------------

HTTP Basic
--------------------------------

JustHealth acknowledge that both the web and the mobile application that they have developed use the API that was  simultaneously developed in the  Python programming language. This is achieved through the use of POST and GET requests, which without authentication makes user data vulnerable.  
 
For example, using the POSTMAN add-on that is available for the Google Chrome browser anyone would have been able to send a POST Request to JustHealth’s API. This would effectively enable them to read, modify and delete data from JustHealths database subsequently, impacting dramatically user’s data confidentiality, integrity and availability.  
 
In order to mitigate this threat, JustHealth have adopted HTTP Basic Authentication. This requires the person querying the API to be authenticated. This is achieved by setting the Headers of a POST/GET request to the username or password  of a legitimate user. In order for this to be able to work across both the web and mobile applications,  there is a method that contains the logic and a method that is able to be externally addressed and runs the corresponding method which contains the logic. This is required as from the web application authentication isn’t required as the method is able to be called internally from views.py. However, the android application is calling the method from an external source and therefore requires authentication to be encoded in the headers of the POST/GET request. Examples of the authentication methods are able to be seen below.  
 
The method that is used to check verify the person that is querying the API:
python:type::

	auth = HTTPBasicAuth()

	@auth.verify_password
	def verify_password(username,password):
	    """Checks if the password entered is the current password for that account"""
	    try:
	        hashedPassword = uq8LnAWi7D.get((uq8LnAWi7D.username == username) & (uq8LnAWi7D.iscurrent==True)).password
	        return sha256_crypt.verify(password, hashedPassword)
	    except:
	        return False

 
Examples of internally and externally addressable methods in the API.
Externally Addressable Method: 
python:type::

	@app.route('/api/deactivateaccount', methods=['POST'])
	@auth.login_required
	def deactivateAccount():
	    return deactivateAccount(request.form)

Internally Addressable Method: 
python:type::

	def deactivateAccount(details):
        #Method contents removed

Example of internal call from views.py (The Web Application itself): 
python:type::

	@app.route('/deactivate', methods=['POST', 'GET'])
	@needLogin
	def deactivate():
	    """Handles account deactivation form"""
	    if request.method == 'POST':
	    #Where the call to the API method deactivateAccount() is made
	        result = deactivateAccount(request.form)
 
Example of the external method call (POST Request) from android: 
java:type::

	public static String post(String url, HashMap<String, String> parameters, Context context) {
        HttpClient httpClient = new DefaultHttpClient();
        HttpPost httppost = new HttpPost("http://raptor.kent.ac.uk:5000/api/" + url);

        //Authentication for HTTP Basic
        SharedPreferences account = context.getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        String password = account.getString("password", null);
        String authentication = username + ":" + password;
        String encodedAuthentication = Base64.encodeToString(authentication.getBytes(), Base64.NO_WRAP);
        httppost.setHeader("Authorization", "Basic " + encodedAuthentication);

        try {
            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);
            Set<Map.Entry<String, String>> detailsSet = parameters.entrySet();
            for (Map.Entry<String, String> string : detailsSet) {
                nameValuePairs.add(new BasicNameValuePair(string.getKey(), string.getValue()));
            }
            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
            HttpResponse response = httpClient.execute(httppost);

            return EntityUtils.toString(response.getEntity());
        }
        catch (ClientProtocolException e) {
            //TODO Auto-generated catch block
        } catch (IOException e) {
            //TODO Auto-generated catch block
        } catch (NullPointerException e) {
            //TODO Auto-generated catch block
        }
        Feedback.toast("Cannot connect to Server", false, context);
        return null;
    }


 

 
It should also be noted that the following methods do not require any API authentication. These are methods that do not require a user to be logged in to run and none of them pose a direct threat to existing user data. 



Manual Authentication
--------------------------------

As well HTTP Basic authentication to ensure that someone querying the API has a legitimate JustHealth user account, JustHealth have also ensured that users querying the API are only allowed to retrieve the information that they have permission to see. Permissions on the user accounts are as follows: 

================  =================================================================================================================
Account Type      Permissions
================  =================================================================================================================
Patient              * They are entitled to read/write information to and from their profile.
                     * They are entitled to read/write 'self' appointments.
                     * They are entitled to read and accept/decline appointments that are created with them.
                     * They are entitled to read their own prescriptions.
                     * They are entitled to read their notes/correspondence.
                     * They are entitled to read and request to connect with other carers.

Carer                * They are entitled to read/write information about themselves.
                     * They are entitled to read/write prescriptions of only patients they are connected too.
                     * They are entitled to read/write appointments that they have created with a patient that they are connected.
                     * They are entitled to read/write correspondence with patients that they are connected too.
                     * They are entitled to read when a patient that they are connected to has taken/missed medication.
                     * They are entitled to read appointments that the patient they have connected too has not marked as private.
                     * They are entitled to read and request to connect with other patient's.

Administrator        * Methods are currently not accessible from the public API.
================  =================================================================================================================

This authentication has been implemented using several methods that check that the user who has authenticated through HTTP Basic has the permission to read and/or write for a given method. For example: 

1. If a user is asking to read/write information about themselves, we check that the username that is sent and authenticated in the header of the request is the same user that is being read from or written too. 

2. If a user (Currently, account type: Carer) is asking to read/write information about a patient, we check that the carer is connected to the patient. 

If either of the above scenarios return False then the API will throw a HTTP 401 status code, not authenticated. 

**The Code**

The method below is the first that JustHealth wrote. This allows us to get the username from the HTTP request headers and this is what we are able to compare permissions too. 
python:type::

    def getUsernameFromHeader():
        """Method gets the HTTP Basic header, decodes it and gets the username"""
        authHeader = str(request.headers.get('Authorization'))
        authHeader = authHeader.replace("Basic ", "")
        decodedAuthHeader = base64.b64decode(authHeader)
        authUsername = decodedAuthHeader.split(':')[0]
        return authUsername


The following method co-ordinates what we should check for. If the method is to update something for themselves then the second parameter is passed as a blank string and therefore, we just need to check that the person authorised, through HTTP Basic is the same as the username that is going to be edited. These checks are done through the two methods below this co-ordinating method.
python:type::

    def verifyContentRequest(username, targetUsername):
    """This co-ordinated the running of the other methods, depending on the parameters that are passed"""
    """This method can be called from anywhere and if the method is retrieving records for the same person that is authenticated targetUsername should be sent accross as an empty string"""
        authUsername = getUsernameFromHeader()
        if targetUsername == "":
            return verifySelf(authUsername, username)
        elif verifySelf(authUsername, username):
            return verifyCarer(username, targetUsername)
        else:
            return abort(401)


This verifies that the record to be read/written of a particular user is the same user that has been authenticated through HTTP Basic.
python:type::

    def verifySelf(authUsername, methodUsername):
    """Checks that the user authenticated by HTTP Basic is the same as user that is associated with the records being read/written"""
        if authUsername == methodUsername:
            return True
        else:
            return abort(401)


This verifies that the record to be read/written for a particular user is a user that is connected to the user that has been authenticated through HTTP Basic.
python:type::

    def verifyCarer(username, targetUsername):
    """Checks that the user authenticated by HTTP Basic is connected to the user that is associated with the records being read/written"""
        accountInfo = json.loads(getAccountInfo(username))
        if accountInfo['accounttype'] == "Carer":
            if getConnectionStatus(username, targetUsername) == "Already Connected":
                return True
            else:
                return abort(401)
        else:
            return abort(401)


All of the methods above are called in the publically accessible API function. The first method shows the call for a method that is retrieving records associated with the authenticated user. 
python:type::

    @app.route('/api/getAppointment', methods=['POST'])
    @auth.login_required
    def getAppointment():
        if verifyContentRequest(request.form['user'], ""):
            return getAppointment(request.form['user'], request.form['appid'])


The second method shows a call where the user making the request is different from the user associated with the records that are being requested.
python:type::

    @app.route('/api/addCorrespondence', methods=['POST'])
    def addCorrespondence():
        if verifyContentRequest(request.form['carer'], request.form['patient']):
            return addCorrespondence(request.form)


Below shows a method where in order to get the associated user of the records that are being requested, the database has to be queried. This occurs when the target username is not sent in the post request.
python:type::

    @app.route('/api/updateAppointment', methods=['POST'])
    @auth.login_required
    def updateAppointment():
        #username isn't sent with the request, so here we need to get the creator of the appointment from the database.
        appointment = Appointments.select().where(Appointments.appid == request.form['appid']).get()
        user = appointment.creator.username
        if verifyContentRequest(user, ""):
            return updateAppointment(request.form['appid'], request.form['name'], request.form['apptype'], request.form['addressnamenumber'], request.form['postcode'], request.form['startdate'], request.form['starttime'], request.form['enddate'], request.form['endtime'], request.form['other'], request.form['private'])



**Why is this necessary?**

Without this manual security API implementation, anyone with valid credentials for the application would be able to query the API and read/write any information from or to the database. 


------------------------
SQL Injection
------------------------

JustHealth have adopted the use of an Object Relational Mapper (ORM) called **peewee**. All of the interactions that happen with JustHealth’s PostgreSQL database happen through the ORM. Not only is this quicker but it provides JustHealth with additional security enhancements; the biggest being the inability to inject SQL into the application. This is because of no direct SQL being run on the database and therefore, input data is placed into already waiting placeholders. If data is not in the correct format, it will simply be rejected by the ORM. 
