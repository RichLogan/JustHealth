.. java:import:: android.app Activity

.. java:import:: android.app ProgressDialog

.. java:import:: android.content Context

.. java:import:: android.content Intent

.. java:import:: android.content SharedPreferences

.. java:import:: android.content.pm PackageInfo

.. java:import:: android.content.pm PackageManager

.. java:import:: android.os AsyncTask

.. java:import:: android.os Bundle

.. java:import:: com.google.android.gms.common ConnectionResult

.. java:import:: com.google.android.gms.common GooglePlayServicesUtil

.. java:import:: com.google.android.gms.gcm GoogleCloudMessaging

.. java:import:: java.io IOException

.. java:import:: java.util HashMap

Main
====

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class Main extends Activity

   JustHealth main application. The user will never see this, but it acts as the primary activity and mainly handles setup required for Google Cloud Messaging (Push notifications).

   It also checks whether a user is logged in and their account type in order to present them with the correct activity.

Fields
------
SENDER_ID
^^^^^^^^^

.. java:field::  String SENDER_ID
   :outertype: Main

account
^^^^^^^

.. java:field::  SharedPreferences account
   :outertype: Main

context
^^^^^^^

.. java:field::  Context context
   :outertype: Main

gcm
^^^

.. java:field::  GoogleCloudMessaging gcm
   :outertype: Main

regid
^^^^^

.. java:field::  String regid
   :outertype: Main

Methods
-------
onCreate
^^^^^^^^

.. java:method:: @Override public void onCreate(Bundle savedInstanceState)
   :outertype: Main

onResume
^^^^^^^^

.. java:method:: @Override protected void onResume()
   :outertype: Main

   Runs on reopen of application

