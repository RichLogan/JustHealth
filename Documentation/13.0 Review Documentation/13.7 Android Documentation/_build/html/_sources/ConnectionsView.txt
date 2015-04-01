.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.app AlertDialog

.. java:import:: android.content DialogInterface

.. java:import:: android.content Intent

.. java:import:: android.content SharedPreferences

.. java:import:: android.graphics Color

.. java:import:: android.os Bundle

.. java:import:: android.os StrictMode

.. java:import:: android.support.v7.widget CardView

.. java:import:: android.text Editable

.. java:import:: android.text InputFilter

.. java:import:: android.text InputType

.. java:import:: android.view Gravity

.. java:import:: android.view View

.. java:import:: android.view ViewGroup

.. java:import:: android.widget ArrayAdapter

.. java:import:: android.widget EditText

.. java:import:: android.widget FrameLayout

.. java:import:: android.widget ImageView

.. java:import:: android.widget LinearLayout

.. java:import:: android.widget SpinnerAdapter

.. java:import:: android.widget TextView

.. java:import:: com.joanzapata.android.iconify Iconify

.. java:import:: org.json JSONArray

.. java:import:: org.json JSONException

.. java:import:: org.json JSONObject

.. java:import:: java.util HashMap

ConnectionsView
===============

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class ConnectionsView extends Activity

   Lists of Connections of the given category (Incoming, Outgoing, Completed) as given by ConnectionsMain

Fields
------
ignoreChange
^^^^^^^^^^^^

.. java:field::  Boolean ignoreChange
   :outertype: ConnectionsView

type
^^^^

.. java:field::  String type
   :outertype: ConnectionsView

Methods
-------
onCreate
^^^^^^^^

.. java:method:: protected void onCreate(Bundle savedInstanceState)
   :outertype: ConnectionsView

   This method runs when the page is first loaded. Sets the correct xml layout to be displayed and loads the action bar. The print connections method is also run.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

