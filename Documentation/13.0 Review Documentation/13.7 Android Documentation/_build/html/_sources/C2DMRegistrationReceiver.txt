.. java:import:: android.content BroadcastReceiver

.. java:import:: android.content Context

.. java:import:: android.content Intent

C2DMRegistrationReceiver
========================

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class C2DMRegistrationReceiver extends BroadcastReceiver

   This class defines how the android device that is running the application is able to get its registration ID. RegistrationID of the device is subsequently used for push notifications.

Methods
-------
onReceive
^^^^^^^^^

.. java:method:: @Override public void onReceive(Context context, Intent intent)
   :outertype: C2DMRegistrationReceiver

