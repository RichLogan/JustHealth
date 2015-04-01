.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.app ProgressDialog

.. java:import:: android.content Intent

.. java:import:: android.os AsyncTask

.. java:import:: android.os Bundle

.. java:import:: android.os StrictMode

.. java:import:: android.view View

.. java:import:: android.widget Button

.. java:import:: android.widget EditText

.. java:import:: java.util HashMap

ForgotPassword
==============

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class ForgotPassword extends Activity

Methods
-------
onCreate
^^^^^^^^

.. java:method:: @Override protected void onCreate(Bundle savedInstanceState)
   :outertype: ForgotPassword

   This method runs when the page is first loaded. Sets the correct xml layout and sets the action bar. OnClickListener on the submit button of the page, runs the getDetails method.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

post
^^^^

.. java:method:: public void post(HashMap<String, String> details)
   :outertype: ForgotPassword

