.. java:import:: android.app IntentService

.. java:import:: android.app NotificationManager

.. java:import:: android.app PendingIntent

.. java:import:: android.content Context

.. java:import:: android.content Intent

.. java:import:: android.media RingtoneManager

.. java:import:: android.net Uri

.. java:import:: android.opengl Visibility

.. java:import:: android.os Bundle

.. java:import:: android.os SystemClock

.. java:import:: android.support.v4.app NotificationCompat

.. java:import:: android.widget Toast

.. java:import:: com.google.android.gms.gcm GoogleCloudMessaging

GcmIntentService
================

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class GcmIntentService extends IntentService

   Created by Stephen on 26/02/15.

Fields
------
NOTIFICATION_ID
^^^^^^^^^^^^^^^

.. java:field:: public static int NOTIFICATION_ID
   :outertype: GcmIntentService

builder
^^^^^^^

.. java:field::  NotificationCompat.Builder builder
   :outertype: GcmIntentService

Constructors
------------
GcmIntentService
^^^^^^^^^^^^^^^^

.. java:constructor:: public GcmIntentService()
   :outertype: GcmIntentService

Methods
-------
onHandleIntent
^^^^^^^^^^^^^^

.. java:method:: @Override protected void onHandleIntent(Intent intent)
   :outertype: GcmIntentService

