.. java:import:: android.annotation TargetApi

.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.os Build

.. java:import:: android.os Bundle

.. java:import:: android.os StrictMode

.. java:import:: android.view View

.. java:import:: android.widget Button

.. java:import:: android.widget EditText

.. java:import:: java.util HashMap

CarerAddPatientCorrespondence
=============================

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class CarerAddPatientCorrespondence extends Activity

Fields
------
patientFirstName
^^^^^^^^^^^^^^^^

.. java:field::  String patientFirstName
   :outertype: CarerAddPatientCorrespondence

patientUsername
^^^^^^^^^^^^^^^

.. java:field::  String patientUsername
   :outertype: CarerAddPatientCorrespondence

Methods
-------
onCreate
^^^^^^^^

.. java:method:: @TargetApi protected void onCreate(Bundle savedInstanceState)
   :outertype: CarerAddPatientCorrespondence

   This runs when the page is first loaded. It also sets the correct xml layout to display. Following this, it sets the action bar, which uses the patients first name. It has an onClickListener to check when the add note button has been pressed. When pressed it runs the add note method.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

