.. java:import:: android.annotation TargetApi

.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.app AlertDialog

.. java:import:: android.content ContentResolver

.. java:import:: android.content ContentUris

.. java:import:: android.content ContentValues

.. java:import:: android.content Context

.. java:import:: android.content DialogInterface

.. java:import:: android.content Intent

.. java:import:: android.content SharedPreferences

.. java:import:: android.graphics Color

.. java:import:: android.graphics.drawable ColorDrawable

.. java:import:: android.net Uri

.. java:import:: android.os Build

.. java:import:: android.os Bundle

.. java:import:: android.os StrictMode

.. java:import:: android.provider CalendarContract

.. java:import:: android.view ContextThemeWrapper

.. java:import:: android.view Gravity

.. java:import:: android.view Menu

.. java:import:: android.view MenuInflater

.. java:import:: android.view MenuItem

.. java:import:: android.view View

.. java:import:: android.view ViewGroup

.. java:import:: android.widget Button

.. java:import:: android.widget LinearLayout

.. java:import:: android.widget Toast

.. java:import:: org.json JSONArray

.. java:import:: org.json JSONException

.. java:import:: org.json JSONObject

.. java:import:: java.text DateFormat

.. java:import:: java.text ParseException

.. java:import:: java.text SimpleDateFormat

.. java:import:: java.util Calendar

.. java:import:: java.util Date

.. java:import:: java.util HashMap

SelfArchivedAppointments
========================

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class SelfArchivedAppointments extends Activity

   Created by Stephen on 06/01/15.

Methods
-------
onCreate
^^^^^^^^

.. java:method:: @TargetApi protected void onCreate(Bundle savedInstanceState)
   :outertype: SelfArchivedAppointments

   This method runs when the page is first loaded. Sets the correct xml layout and sets the correct custom action bar. Runs the printArchivedAppointments method.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

onCreateOptionsMenu
^^^^^^^^^^^^^^^^^^^

.. java:method:: @Override public boolean onCreateOptionsMenu(Menu menu)
   :outertype: SelfArchivedAppointments

   Creates the action bar items for the SelfArchived Appointments page

   :param menu: The options menu in which the items are placed
   :return: True must be returned in order for the options menu to be displayed

onOptionsItemSelected
^^^^^^^^^^^^^^^^^^^^^

.. java:method:: @Override public boolean onOptionsItemSelected(MenuItem item)
   :outertype: SelfArchivedAppointments

   This method is called when any action from the action bar is selected

   :param item: The menu item that was selected
   :return: in order for the method to work, true should be returned here

