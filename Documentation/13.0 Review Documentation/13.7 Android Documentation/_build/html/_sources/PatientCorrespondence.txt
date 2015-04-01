.. java:import:: android.annotation TargetApi

.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.app ProgressDialog

.. java:import:: android.content SharedPreferences

.. java:import:: android.graphics Color

.. java:import:: android.graphics Typeface

.. java:import:: android.os AsyncTask

.. java:import:: android.os Build

.. java:import:: android.os Bundle

.. java:import:: android.os StrictMode

.. java:import:: android.view ContextThemeWrapper

.. java:import:: android.view Gravity

.. java:import:: android.view View

.. java:import:: android.view ViewGroup

.. java:import:: android.widget Button

.. java:import:: android.widget LinearLayout

.. java:import:: android.widget RelativeLayout

.. java:import:: android.widget TableRow

.. java:import:: android.widget TextView

.. java:import:: org.json JSONArray

.. java:import:: org.json JSONException

.. java:import:: org.json JSONObject

.. java:import:: java.util HashMap

PatientCorrespondence
=====================

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class PatientCorrespondence extends Activity

Fields
------
notes
^^^^^

.. java:field::  JSONArray notes
   :outertype: PatientCorrespondence

Methods
-------
onCreate
^^^^^^^^

.. java:method:: @TargetApi protected void onCreate(Bundle savedInstanceState)
   :outertype: PatientCorrespondence

   This method is initiated when the page is first loaded. It sets the correct xml layout and displays the action bar. Invokes the method, getNotes.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

