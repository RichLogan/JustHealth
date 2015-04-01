.. java:import:: android.app Activity

.. java:import:: android.app ActionBar

.. java:import:: android.app AlertDialog

.. java:import:: android.app ProgressDialog

.. java:import:: android.content DialogInterface

.. java:import:: android.content Intent

.. java:import:: android.graphics.drawable Drawable

.. java:import:: android.os AsyncTask

.. java:import:: android.os Bundle

.. java:import:: android.util TypedValue

.. java:import:: android.view Gravity

.. java:import:: android.view Menu

.. java:import:: android.view MenuItem

.. java:import:: android.view MenuInflater

.. java:import:: android.view View

.. java:import:: android.widget Button

.. java:import:: android.widget LinearLayout

.. java:import:: android.widget ProgressBar

.. java:import:: com.joanzapata.android.iconify IconDrawable

.. java:import:: com.joanzapata.android.iconify Iconify

.. java:import:: org.json JSONArray

.. java:import:: org.json JSONException

.. java:import:: org.json JSONObject

.. java:import:: java.util HashMap

CarerPrescriptions
==================

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class CarerPrescriptions extends Activity

   Functionality to allow a carer to view all Prescriptions for any patient that they are connected to.

Methods
-------
onActivityResult
^^^^^^^^^^^^^^^^

.. java:method:: @Override protected void onActivityResult(int requestCode, int resultCode, Intent data)
   :outertype: CarerPrescriptions

   Informs the calling activity whether the action was successful for not.

   :param requestCode: Internally used, autopopulated
   :param resultCode: 1 for success, 0 for failure
   :param data: Internally used, autopopulated

onCreate
^^^^^^^^

.. java:method:: protected void onCreate(Bundle savedInstanceState)
   :outertype: CarerPrescriptions

   This method runs when the page is first loaded. Sets the correct xml layout to be displayed and loads the custom action bar. Because of the use of a custom action bar the action listeners have to be applied manually here too. The loadPrescriptions method is then run from here.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

