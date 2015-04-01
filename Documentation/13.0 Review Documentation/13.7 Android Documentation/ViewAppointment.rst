.. java:import:: android.annotation TargetApi

.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.content Intent

.. java:import:: android.os Build

.. java:import:: android.os Bundle

.. java:import:: android.os StrictMode

.. java:import:: android.view View

.. java:import:: android.view ViewGroup

.. java:import:: android.widget Button

.. java:import:: android.widget CheckBox

.. java:import:: android.widget EditText

.. java:import:: android.widget TextView

.. java:import:: java.util HashMap

ViewAppointment
===============

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class ViewAppointment extends Activity

   Created by Stephen on 16/03/15.

Methods
-------
onCreate
^^^^^^^^

.. java:method:: @TargetApi protected void onCreate(Bundle savedInstanceState)
   :outertype: ViewAppointment

   This runs when the page is first loaded, it sets the correct xml layout and loads the action bar. Has a number of onClickListeners for the update button on the page, when this is pressed the user is redirected to the edit page. The display method is also run to display the appointment and all details.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

