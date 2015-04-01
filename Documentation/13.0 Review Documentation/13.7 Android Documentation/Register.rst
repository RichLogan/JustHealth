.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.app AlertDialog

.. java:import:: android.content ActivityNotFoundException

.. java:import:: android.content DialogInterface

.. java:import:: android.content Intent

.. java:import:: android.os Bundle

.. java:import:: android.view View

.. java:import:: android.widget AdapterView

.. java:import:: android.widget AdapterView.OnItemSelectedListener

.. java:import:: android.widget Button

.. java:import:: android.widget CheckBox

.. java:import:: android.widget EditText

.. java:import:: android.widget IconTextView

.. java:import:: android.widget Spinner

.. java:import:: java.util HashMap

Register
========

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class Register extends Activity

Methods
-------
isPasswordValid
^^^^^^^^^^^^^^^

.. java:method:: public boolean isPasswordValid(String password, String confirmPassword)
   :outertype: Register

   THIS METHOD IS NOT IN USE validation on password and confirm

   :param password: the password
   :param confirmPassword: the password in the confirm password field
   :return: Boolean whether the two passwords match.

onCreate
^^^^^^^^

.. java:method:: @Override protected void onCreate(Bundle savedInstanceState)
   :outertype: Register

   This method runs when the page is first loaded. Sets the correct xml layout and sets the correct action bar. Onclick listener for the register button. runs the method that checks for a change of the spinners.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

post
^^^^

.. java:method:: public void post(HashMap<String, String> details)
   :outertype: Register

   Makes the post request to the JustHealth API to register the user. If successful, alerts the user, and redirects them to the login page.

   :param details: HashMap of the details of the user to be registered.

