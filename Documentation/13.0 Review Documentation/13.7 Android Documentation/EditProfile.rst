.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.app AlertDialog

.. java:import:: android.content DialogInterface

.. java:import:: android.content Intent

.. java:import:: android.os Bundle

.. java:import:: android.view View

.. java:import:: android.widget AdapterView

.. java:import:: android.widget Button

.. java:import:: android.widget EditText

.. java:import:: android.widget IconTextView

.. java:import:: android.widget RadioButton

.. java:import:: android.widget RadioGroup

.. java:import:: android.widget Spinner

.. java:import:: android.widget TextView

.. java:import:: org.json JSONException

.. java:import:: org.json JSONObject

.. java:import:: java.util HashMap

EditProfile
===========

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class EditProfile extends Activity

Methods
-------
onCreate
^^^^^^^^

.. java:method:: protected void onCreate(Bundle savedInstanceState)
   :outertype: EditProfile

   Sets the correct xml layout for the page and loads the action bar. Sets an onClickListener on the update button and runs the method to load the existing profile information.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

