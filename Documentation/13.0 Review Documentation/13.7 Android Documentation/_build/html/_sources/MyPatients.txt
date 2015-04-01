.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.app AlertDialog

.. java:import:: android.app ProgressDialog

.. java:import:: android.content DialogInterface

.. java:import:: android.content Intent

.. java:import:: android.os AsyncTask

.. java:import:: android.os Bundle

.. java:import:: android.view View

.. java:import:: android.widget Button

.. java:import:: android.widget LinearLayout

.. java:import:: org.json JSONArray

.. java:import:: org.json JSONException

.. java:import:: org.json JSONObject

.. java:import:: java.util HashMap

MyPatients
==========

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class MyPatients extends Activity

Methods
-------
onCreate
^^^^^^^^

.. java:method:: protected void onCreate(Bundle savedInstanceState)
   :outertype: MyPatients

   Run when the page first loads, assigns the correct xml layout and displays the action bar. Invokes loadPatients()

   :param savedInstanceState: a bundle if the state of the application was to be saved.

