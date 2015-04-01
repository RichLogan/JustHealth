.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.app AlertDialog

.. java:import:: android.app ProgressDialog

.. java:import:: android.content DialogInterface

.. java:import:: android.content Intent

.. java:import:: android.os AsyncTask

.. java:import:: android.os Bundle

.. java:import:: android.os StrictMode

.. java:import:: android.view View

.. java:import:: android.widget Button

.. java:import:: android.widget LinearLayout

.. java:import:: org.json JSONArray

.. java:import:: org.json JSONException

.. java:import:: org.json JSONObject

.. java:import:: java.util HashMap

PatientPrescription
===================

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class PatientPrescription extends Activity

Methods
-------
onCreate
^^^^^^^^

.. java:method:: protected void onCreate(Bundle savedInstanceState)
   :outertype: PatientPrescription

   The onCreate method is run when the page is first loaded. The correct xml layout is set and the action bar is loaded. The getPrescriptions method is invoked.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

