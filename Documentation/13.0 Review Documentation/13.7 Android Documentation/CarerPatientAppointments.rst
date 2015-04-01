.. java:import:: android.annotation TargetApi

.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.app AlertDialog

.. java:import:: android.app ProgressDialog

.. java:import:: android.content ContentResolver

.. java:import:: android.content ContentUris

.. java:import:: android.content ContentValues

.. java:import:: android.content DialogInterface

.. java:import:: android.content Intent

.. java:import:: android.content SharedPreferences

.. java:import:: android.graphics Color

.. java:import:: android.net Uri

.. java:import:: android.os AsyncTask

.. java:import:: android.os Build

.. java:import:: android.os Bundle

.. java:import:: android.provider CalendarContract

.. java:import:: android.view Menu

.. java:import:: android.view MenuInflater

.. java:import:: android.view MenuItem

.. java:import:: android.view View

.. java:import:: android.widget Button

.. java:import:: android.widget LinearLayout

.. java:import:: android.widget TextView

.. java:import:: com.joanzapata.android.iconify IconDrawable

.. java:import:: com.joanzapata.android.iconify Iconify

.. java:import:: org.json JSONArray

.. java:import:: org.json JSONException

.. java:import:: org.json JSONObject

.. java:import:: java.text DateFormat

.. java:import:: java.text ParseException

.. java:import:: java.text SimpleDateFormat

.. java:import:: java.util Calendar

.. java:import:: java.util Date

.. java:import:: java.util HashMap

.. java:import:: java.util Locale

CarerPatientAppointments
========================

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class CarerPatientAppointments extends Activity

Fields
------
appointmentHolder
^^^^^^^^^^^^^^^^^

.. java:field::  LinearLayout appointmentHolder
   :outertype: CarerPatientAppointments

Methods
-------
onCreate
^^^^^^^^

.. java:method:: protected void onCreate(Bundle savedInstanceState)
   :outertype: CarerPatientAppointments

   This runs when the page is first loaded. It also sets the correct xml layout to display. Following this, it sets the action bar, which uses the patients first name. It has an onClickListener to check when the filter button is pressed. When pressed the filter options method is run and this is used to bring up a menu option of the different filters.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

onCreateOptionsMenu
^^^^^^^^^^^^^^^^^^^

.. java:method:: @Override public boolean onCreateOptionsMenu(Menu menu)
   :outertype: CarerPatientAppointments

   Creates the action bar items for the CarerPatient Appointments page

   :param menu: The options menu in which the items are placed
   :return: True must be returned in order for the options menu to be displayed

onOptionsItemSelected
^^^^^^^^^^^^^^^^^^^^^

.. java:method:: @Override public boolean onOptionsItemSelected(MenuItem item)
   :outertype: CarerPatientAppointments

   This method is called when any action from the action bar is selected

   :param item: The menu item that was selected
   :return: in order for the method to work, true should be returned here

onResume
^^^^^^^^

.. java:method:: protected void onResume()
   :outertype: CarerPatientAppointments

   This runs when the page is reloaded, it ensures that the page is reloaded so that an appointment that has been added is retrieved from the database and displayed.

