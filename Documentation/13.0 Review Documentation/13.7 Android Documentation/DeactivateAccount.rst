.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.app AlertDialog

.. java:import:: android.app ProgressDialog

.. java:import:: android.content Context

.. java:import:: android.content DialogInterface

.. java:import:: android.content Intent

.. java:import:: android.content SharedPreferences

.. java:import:: android.os AsyncTask

.. java:import:: android.os Bundle

.. java:import:: android.os StrictMode

.. java:import:: android.util Base64

.. java:import:: android.util Log

.. java:import:: android.view Gravity

.. java:import:: android.view View

.. java:import:: android.widget ArrayAdapter

.. java:import:: android.widget Button

.. java:import:: android.widget CheckBox

.. java:import:: android.widget EditText

.. java:import:: android.widget Spinner

.. java:import:: android.widget TextView

.. java:import:: android.widget Toast

.. java:import:: org.apache.http HttpResponse

.. java:import:: org.apache.http NameValuePair

.. java:import:: org.apache.http.client HttpClient

.. java:import:: org.apache.http.client.entity UrlEncodedFormEntity

.. java:import:: org.apache.http.client.methods HttpPost

.. java:import:: org.apache.http.impl.client DefaultHttpClient

.. java:import:: org.apache.http.message BasicNameValuePair

.. java:import:: org.apache.http.util EntityUtils

.. java:import:: org.json JSONArray

.. java:import:: org.json JSONException

.. java:import:: org.json JSONObject

.. java:import:: java.io IOException

.. java:import:: java.util ArrayList

.. java:import:: java.util HashMap

.. java:import:: java.util List

.. java:import:: java.util Map

.. java:import:: java.util Set

DeactivateAccount
=================

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class DeactivateAccount extends Activity

   Created by stephentate on 04/11/14.

Methods
-------
onCreate
^^^^^^^^

.. java:method:: protected void onCreate(Bundle savedInstanceState)
   :outertype: DeactivateAccount

   This runs when the page is first loaded. This shows the action bar and runs the populate spinner method. There are then two action listeners for the deactivate button and the link to show the reasons why we should keep the data.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

