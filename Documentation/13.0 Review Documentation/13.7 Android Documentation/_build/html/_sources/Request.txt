.. java:import:: android.content Context

.. java:import:: android.content SharedPreferences

.. java:import:: android.os AsyncTask

.. java:import:: android.util Base64

.. java:import:: org.apache.http HttpResponse

.. java:import:: org.apache.http NameValuePair

.. java:import:: org.apache.http.client ClientProtocolException

.. java:import:: org.apache.http.client HttpClient

.. java:import:: org.apache.http.client.entity UrlEncodedFormEntity

.. java:import:: org.apache.http.client.methods HttpGet

.. java:import:: org.apache.http.client.methods HttpPost

.. java:import:: org.apache.http.impl.client DefaultHttpClient

.. java:import:: org.apache.http.message BasicNameValuePair

.. java:import:: org.apache.http.util EntityUtils

.. java:import:: java.io IOException

.. java:import:: java.net InetAddress

.. java:import:: java.net URI

.. java:import:: java.net UnknownHostException

.. java:import:: java.util ArrayList

.. java:import:: java.util HashMap

.. java:import:: java.util List

.. java:import:: java.util Map

.. java:import:: java.util Set

Request
=======

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class Request

   Helper class containing static methods for communication with the JustHealth server. Primarily provides access to POST and GET requests.

Methods
-------
get
^^^

.. java:method:: public static String get(String url, Context context)
   :outertype: Request

   Provides GET request communication to JustHealth's public facing API located at /api when no parameters need to be passed

   :param url: The API function url for the request, not the full URL. e.g http://server/api/{THIS_URL_HERE}
   :param context: The current application context, usually provided by getApplicationContext(). Allows access to SharedPreferences.
   :return: The result of the API call as a String. This is most often JSON but should be decoded by the calling functionality.

getServerURL
^^^^^^^^^^^^

.. java:method:: public static String getServerURL()
   :outertype: Request

   Method to get the active server's URL (protocol, host, port)

   :return: Full URL as String

post
^^^^

.. java:method:: public static String post(String url, HashMap<String, String> parameters, Context context)
   :outertype: Request

   Provides POST request communication to JustHealth's public facing API located at /api Takes credentials for the server from the logged in user's details

   :param url: The API function url for the request, not the full URL. e.g http://server/api/{THIS_URL_HERE}
   :param parameters: The parameters for the post request in the form of a HashMap corresponding to the key/value pairs the API function expects.
   :param context: The current application context, usually provided by getApplicationContext(). Allows access to SharedPreferences.
   :return: The result of the API call as a String. This is most often JSON but should be decoded by the calling functionality.

serverCheck
^^^^^^^^^^^

.. java:method:: public static void serverCheck(Context c)
   :outertype: Request

   Checks to see if the JustHealthServer is reachable -

   :param c: Application Context

