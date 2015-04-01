.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.os AsyncTask

.. java:import:: android.os Bundle

.. java:import:: android.view Gravity

.. java:import:: android.view View

.. java:import:: android.widget CheckBox

.. java:import:: android.widget LinearLayout

.. java:import:: android.widget TextView

.. java:import:: org.json JSONException

.. java:import:: org.json JSONObject

.. java:import:: java.text DateFormatSymbols

.. java:import:: java.util Calendar

.. java:import:: java.util HashMap

.. java:import:: java.util Locale

TakePrescription
================

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class TakePrescription extends Activity

Fields
------
prescription
^^^^^^^^^^^^

.. java:field::  JSONObject prescription
   :outertype: TakePrescription

Methods
-------
onCreate
^^^^^^^^

.. java:method:: @Override public void onCreate(Bundle savedInstanceState)
   :outertype: TakePrescription

   This runs when the page is first loaded and all of the prescription taking is controlled from here. The correct xml layout is set and the action bar is loaded. All of the parameters of the prescription are already passed with the intent. Firstly, the display is set correctly and dynamically depending on what is set in the prescription JSONObject. After this any boxes that are ticked a post request is made asynchronously to the JustHealth API to ensure that the taking of the medication is recorded on the backend too.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

