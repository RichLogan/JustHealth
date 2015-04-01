.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.app ProgressDialog

.. java:import:: android.content Intent

.. java:import:: android.content SharedPreferences

.. java:import:: android.os AsyncTask

.. java:import:: android.os Bundle

.. java:import:: android.view View

.. java:import:: android.widget Button

.. java:import:: android.widget EditText

.. java:import:: android.widget TextView

.. java:import:: android.widget Toast

.. java:import:: org.json JSONException

.. java:import:: org.json JSONObject

.. java:import:: java.util HashMap

ExpiredPassword
===============

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class ExpiredPassword extends Activity

   Created by Stephen on 15/02/15.

Methods
-------
onCreate
^^^^^^^^

.. java:method:: @Override protected void onCreate(Bundle savedInstanceState)
   :outertype: ExpiredPassword

   This method is invoked when the page is first loaded. Sets the correct xml layout and shows the action bar. Assigns the class variables from what is passed with the intent. OnclickListener for the password reset button.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

