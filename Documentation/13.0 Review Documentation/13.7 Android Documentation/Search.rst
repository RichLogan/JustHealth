.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.app AlertDialog

.. java:import:: android.content DialogInterface

.. java:import:: android.content Intent

.. java:import:: android.content SharedPreferences

.. java:import:: android.graphics Color

.. java:import:: android.os Bundle

.. java:import:: android.os StrictMode

.. java:import:: android.view View

.. java:import:: android.view ViewGroup

.. java:import:: android.widget Button

.. java:import:: android.widget EditText

.. java:import:: android.widget LinearLayout

.. java:import:: android.widget TableLayout

.. java:import:: android.widget TableRow

.. java:import:: android.widget TextView

.. java:import:: com.joanzapata.android.iconify Iconify

.. java:import:: org.json JSONArray

.. java:import:: org.json JSONException

.. java:import:: org.json JSONObject

.. java:import:: java.util HashMap

Search
======

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class Search extends Activity

Methods
-------
connectOnClick
^^^^^^^^^^^^^^

.. java:method::  View.OnClickListener connectOnClick(Button button, String targetUsername)
   :outertype: Search

   This method is the action listener that is applied to the Connect button to create a new connection after searching for a user. It runs the connect method, gives you the option to cancel or connect and changes the text on the button and stops the button being clicked again.

   :param button: the button that the onclick listener is applied too
   :param targetUsername: the username of the person that they want to remove as a connection

onCreate
^^^^^^^^

.. java:method:: protected void onCreate(Bundle savedInstanceState)
   :outertype: Search

   This method runs when the page is first loaded. Sets the correct xml layout and sets the correct action bar. Onclick listener for the search button.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

