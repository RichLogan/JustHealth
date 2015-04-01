.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.content Context

.. java:import:: android.content Intent

.. java:import:: android.graphics Color

.. java:import:: android.graphics.drawable ColorDrawable

.. java:import:: android.os Bundle

.. java:import:: android.os StrictMode

.. java:import:: android.view Gravity

.. java:import:: android.view View

.. java:import:: android.view Menu

.. java:import:: android.widget ArrayAdapter

.. java:import:: android.widget Button

.. java:import:: android.widget CheckBox

.. java:import:: android.widget EditText

.. java:import:: android.widget Spinner

.. java:import:: android.widget Toast

.. java:import:: com.joanzapata.android.iconify Iconify

.. java:import:: org.json JSONArray

.. java:import:: org.json JSONException

.. java:import:: java.util ArrayList

.. java:import:: java.util HashMap

AddPrescription
===============

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class AddPrescription extends Activity

Methods
-------
onCreate
^^^^^^^^

.. java:method:: protected void onCreate(Bundle savedInstanceState)
   :outertype: AddPrescription

   This runs when the page is first loaded. It also sets the correct xml layout to display. Following this, it sets the action bar and runs the function to populate the spinner containing the medication names. Has an onClickListener to check when the add prescription button has been pressed. When pressed it first validates the form and then runs the add prescription method.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

