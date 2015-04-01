.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.content Intent

.. java:import:: android.os Bundle

.. java:import:: android.view View

.. java:import:: android.widget Button

Settings
========

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class Settings extends Activity

   This page displays 4 buttons for a user to access all settings options

Methods
-------
onCreate
^^^^^^^^

.. java:method:: protected void onCreate(Bundle savedInstanceState)
   :outertype: Settings

   This runs when the page is first loaded, it sets the correct xml layout and loads the action bar. Has a number of onClickListeners for each of the buttons on the page.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

