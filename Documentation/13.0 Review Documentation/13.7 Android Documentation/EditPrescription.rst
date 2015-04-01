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

.. java:import:: android.widget ArrayAdapter

.. java:import:: android.widget Button

.. java:import:: android.widget CheckBox

.. java:import:: android.widget EditText

.. java:import:: android.widget Spinner

.. java:import:: android.widget TextView

.. java:import:: org.json JSONArray

.. java:import:: org.json JSONException

.. java:import:: org.json JSONObject

.. java:import:: java.util ArrayList

.. java:import:: java.util HashMap

.. java:import:: java.util.zip CheckedOutputStream

EditPrescription
================

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class EditPrescription extends Activity

Fields
------
prescription
^^^^^^^^^^^^

.. java:field::  JSONObject prescription
   :outertype: EditPrescription

Methods
-------
onCreate
^^^^^^^^

.. java:method:: protected void onCreate(Bundle savedInstanceState)
   :outertype: EditPrescription

   This sets the correct xml layout. It gets the prescription JSON object that was passed with the intent and assigns it to the class variable. OnClickListener for the update button, displays an are you sure... dialog.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

