.. java:import:: android.annotation TargetApi

.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.app ProgressDialog

.. java:import:: android.content Intent

.. java:import:: android.content SharedPreferences

.. java:import:: android.graphics Color

.. java:import:: android.graphics Typeface

.. java:import:: android.os AsyncTask

.. java:import:: android.os Build

.. java:import:: android.os Bundle

.. java:import:: android.os StrictMode

.. java:import:: android.view Menu

.. java:import:: android.view MenuInflater

.. java:import:: android.view MenuItem

.. java:import:: android.view View

.. java:import:: android.widget LinearLayout

.. java:import:: android.widget TableRow

.. java:import:: android.widget TextView

.. java:import:: org.json JSONArray

.. java:import:: org.json JSONException

.. java:import:: org.json JSONObject

.. java:import:: java.util HashMap

CarerPatientCorrespondence
==========================

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class CarerPatientCorrespondence extends Activity

   Created by Stephen on 06/03/15.

Fields
------
notes
^^^^^

.. java:field::  JSONArray notes
   :outertype: CarerPatientCorrespondence

patientFirstName
^^^^^^^^^^^^^^^^

.. java:field::  String patientFirstName
   :outertype: CarerPatientCorrespondence

patientSurname
^^^^^^^^^^^^^^

.. java:field::  String patientSurname
   :outertype: CarerPatientCorrespondence

patientUsername
^^^^^^^^^^^^^^^

.. java:field::  String patientUsername
   :outertype: CarerPatientCorrespondence

Methods
-------
onCreate
^^^^^^^^

.. java:method:: @TargetApi protected void onCreate(Bundle savedInstanceState)
   :outertype: CarerPatientCorrespondence

   Runs when the page is first loaded. This sets the correct XML layout for the page and sets the action bar. Runs the method to retrieve the notes from the JustHealth API.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

onCreateOptionsMenu
^^^^^^^^^^^^^^^^^^^

.. java:method:: @Override public boolean onCreateOptionsMenu(Menu menu)
   :outertype: CarerPatientCorrespondence

   This creates the action bar menu items

   :param menu: The options menu in which you place your items.
   :return: You must return true for the menu to be displayed; if you return false it will not be shown.

onOptionsItemSelected
^^^^^^^^^^^^^^^^^^^^^

.. java:method:: @Override public boolean onOptionsItemSelected(MenuItem item)
   :outertype: CarerPatientCorrespondence

   This method defines the actions when the menu items are pressed

   :param item: The item that has been pressed
   :return: returns true if the action has been executed.

