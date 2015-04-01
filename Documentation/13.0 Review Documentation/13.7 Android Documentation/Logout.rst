.. java:import:: android.app Activity

.. java:import:: android.content Context

.. java:import:: android.content Intent

.. java:import:: android.content SharedPreferences

.. java:import:: android.view Gravity

.. java:import:: android.widget Toast

.. java:import:: java.util HashMap

Logout
======

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class Logout extends Activity

Methods
-------
logout
^^^^^^

.. java:method:: public static void logout(Context context)
   :outertype: Logout

   This is run when the user selects to logout the application. It checks whether the appointment has been added to the users calendar. If so this is deleted. A post request is also made to the API deleteAndroidRegistrationID which subsequently removes the users android ID details from the database.

   :param context: A HashMap of the users username and registration id to logout

