.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.content Intent

.. java:import:: android.content SharedPreferences

.. java:import:: android.os AsyncTask

.. java:import:: android.os Bundle

.. java:import:: android.view View

.. java:import:: android.widget Button

.. java:import:: android.widget ImageView

.. java:import:: android.widget TextView

.. java:import:: org.json JSONException

.. java:import:: org.json JSONObject

.. java:import:: java.util HashMap

.. java:import:: java.util Map

Profile
=======

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class Profile extends Activity

Methods
-------
onActivityResult
^^^^^^^^^^^^^^^^

.. java:method:: @Override protected void onActivityResult(int requestCode, int resultCode, Intent data)
   :outertype: Profile

   Runs when the profile activity exits giving you the requestCode you started it with, the resultCode it returned, and any additional data from it. The resultCode will be RESULT_CANCELED if the activity explicitly returned that, didn't return any result, or crashed during its operation.

   :param requestCode: The integer request code originally supplied to startActivityForResult(), allowing you to identify who this result came from.
   :param resultCode: The integer result code returned by the child activity through its setResult().
   :param data: An Intent, which can return result data to the caller (various data can be attached to Intent "extras").

onCreate
^^^^^^^^

.. java:method:: @Override protected void onCreate(Bundle savedInstanceState)
   :outertype: Profile

   This sets the correct xml layout and displays the action bar. Sets profile username and account type in the relevant text views. Runs the load profile method.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

