========================
Security Documentation
========================

------------------------
Introduction
------------------------

In order for JustHealth to be reputable, trusted and widely used it is necessary to ensure that patient confidentiality, data integrity and the availability of this data is exceptional. Therefore, JustHealth have adopted a strict security policy and implemented  security controls to ensure that JustHealth are able to meet customer expectation. 


------------------------
HTTPS
------------------------

All of the communication between a clients browser and/or any android device  that they may be running JustHealth’s  Mobile application to the JustHealth server will be encrypted via SSL. JustHealth made the decision to utilise this protocol rather than standard HTTP as it ensures that user data is encrypted when being transmitted across the internet. This will help to ensure that the confidentiality of patient data is maintained.  
 
JustHealth have been able to implement HTTPS on all application traffic by configuring it on the server where JustHealth is located. It was able to be completed using the following: 
 
<<Show the code here, TBC>> 
 
This implements Transport Layer Security 1.2 (TLS 1.2), which is currently viewed as being the most secure application layer security protocol that is able to be implemented on the web. It is not vulnerable to the recently publicised and discovered POODLE vulnerability. 


------------------------
Password Security
------------------------

Password Security has been extremely important to JustHealth and therefore, all user passwords are hashed in the database. This ensures that even administrators would not be able to convert the password to plaintext. This is important as although it is not advised users of JustHealth are likely to use their JustHealth login credentials on other accounts that they have. Although, very unlikely, if the JustHealth database was to be compromised it would not be feasible for a hacker to be able to convert passwords to plaintext. 
 
The hashing algorithm that JustHealth have adopted is the same one that is utilised by the Linux Operating System. This is a python algorithm named: SHA-256 Crypt. Currently, there are no known weaknesses or vulnerabilities. JustHealth make a conscious effort to review this regularly and if there are any vulnerabilities that come to light JustHealth will address this.  
 
Example of the implementation code: ::

    # Encrypt password with SHA 256
    profile['password'] = sha256_crypt.encrypt(profile['password'])

Example of the password "hello", stored as a hash:
	$5$rounds=110000$u.CYQ7BoQbYoEyCi$hzbrZqkoKPdHeVaWvCuZnastY17W/oenJudbcdcOwj2

 
When a user logs into the JustHealth web or mobile application the password that they enter into the field is also Hashed in the same way and compared to their hashed password that is stored in JustHealths database.  
 
Example of the code used to authenticate a user at login: ::
	hashedPassword = uq8LnAWi7D.get((uq8LnAWi7D.username == attempted.username) & (uq8LnAWi7D.iscurrent==True)).password.strip()
    attemptedPassword = request.form['password']
    #This checks that the password that they have entered is the same as the password that is stored in the database.
    if sha256_crypt.verify(attemptedPassword, hashedPassword):
    	#other checks that check that the account is verified etc. 
 
<<Android Password storage- this needs to be written how it is encrypted in the shared-preferences- when completed.>>


--------------------------------
API Authentication - HTTP Basic
--------------------------------

JustHealth acknowledge that both the web and the mobile application that they have developed use the API that was  simultaneously developed in the  Python programming language. This is achieved through the use of POST and GET requests, which without authentication makes user data vulnerable.  
 
For example, using the POSTMAN add-on that is available for the Google Chrome browser anyone would have been able to send a POST Request to JustHealth’s API. This would effectively enable them to read, modify and delete data from JustHealths database subsequently, impacting dramatically user’s data confidentiality, integrity and availability.  
 
In order to mitigate this threat, JustHealth have adopted HTTP Basic Authentication. This requires the person querying the API to be authenticated. This is achieved by setting the Headers of a POST/GET request to the username or password  of a legitimate user. In order for this to be able to work across both the web and mobile applications,  there is a method that contains the logic and a method that is able to be externally addressed and runs the corresponding method which contains the logic. This is required as from the web application authentication isn’t required as the method is able to be called internally from views.py. However, the android application is calling the method from an external source and therefore requires authentication to be encoded in the headers of the POST/GET request. Examples of the authentication methods are able to be seen below.  
 
The method that is used to check verify the person that is querying the API: ::

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
Externally Addressable Method: :: 

	@app.route('/api/deactivateaccount', methods=['POST'])
	@auth.login_required
	def deactivateAccount():
	    return deactivateAccount(request.form)

Internally Addressable Method: ::

	def deactivateAccount(details):
    #Method contents removed

Example of internal call from views.py (The Web Application itself): :: 

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


------------------------
SQL Injection
------------------------

JustHealth have adopted the use of an Object Relational Mapper (ORM) called peewee. All of the interactions that happen with JustHealth’s PostgreSQL database happen through the ORM. Not only is this quicker but it provides JustHealth with additional security enhancements; the biggest being the inability to inject SQL into the application. This is because of no direct SQL being run on the database and therefore, input data is placed into already waiting placeholders. If data is not in the correct format, it will simply be rejected by the ORM. 
