.. java:import:: android.content Context

.. java:import:: android.graphics Color

.. java:import:: android.view Gravity

.. java:import:: android.widget Toast

Feedback
========

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class Feedback

Methods
-------
toast
^^^^^

.. java:method:: public static void toast(String value, Boolean success, Context context)
   :outertype: Feedback

   This creates a toast so that JustHealth are able to provide feedback to the user easily.

   :param value: The text that should be displayed to the user
   :param success: Boolean, determines whether the toast should be Red or not.
   :param context: The current application activity. (e.g. getApplicationContext())

