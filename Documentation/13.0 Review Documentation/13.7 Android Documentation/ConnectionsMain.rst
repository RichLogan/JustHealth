.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.content Intent

.. java:import:: android.content SharedPreferences

.. java:import:: android.os AsyncTask

.. java:import:: android.os Bundle

.. java:import:: android.view View

.. java:import:: android.widget Button

.. java:import:: android.widget RelativeLayout

.. java:import:: android.widget TextView

.. java:import:: org.json JSONArray

.. java:import:: org.json JSONException

.. java:import:: org.json JSONObject

.. java:import:: java.util HashMap

ConnectionsMain
===============

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class ConnectionsMain extends Activity

   Allows a user access to their incoming, outgoing and completed connections through the creation of ConnectionsView.

Fields
------
completed
^^^^^^^^^

.. java:field::  JSONArray completed
   :outertype: ConnectionsMain

incoming
^^^^^^^^

.. java:field::  JSONArray incoming
   :outertype: ConnectionsMain

outgoing
^^^^^^^^

.. java:field::  JSONArray outgoing
   :outertype: ConnectionsMain

Methods
-------
onCreate
^^^^^^^^

.. java:method:: protected void onCreate(Bundle savedInstanceState)
   :outertype: ConnectionsMain

   This method runs when the page is first loaded. Sets the correct xml layout to be displayed and loads the action bar. It has action listeners for the incoming/outgoing and completed buttons (the type of connections). The getConnections method is also run.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

