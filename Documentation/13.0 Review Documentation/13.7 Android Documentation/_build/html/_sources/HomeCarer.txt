.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.content Intent

.. java:import:: android.content SharedPreferences

.. java:import:: android.os Bundle

.. java:import:: android.view Menu

.. java:import:: android.view MenuInflater

.. java:import:: android.view MenuItem

.. java:import:: android.view View

.. java:import:: android.widget Button

.. java:import:: android.widget IconTextView

HomeCarer
=========

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class HomeCarer extends Activity

Methods
-------
onCreate
^^^^^^^^

.. java:method:: protected void onCreate(Bundle savedInstanceState)
   :outertype: HomeCarer

   Creates the action bar items for the home carer page

   :param savedInstanceState: The options menu in which the items are placed
   :return: True must be returned in order for the terms and conditions page to be displayed This page displays 6 buttons for a user to access all settings options

onCreateOptionsMenu
^^^^^^^^^^^^^^^^^^^

.. java:method:: @Override public boolean onCreateOptionsMenu(Menu menu)
   :outertype: HomeCarer

   Creates the action bar items for the Carer Home page

   :param menu: The options menu in which the items are placed
   :return: True must be returned in order for the options menu to be displayed

onOptionsItemSelected
^^^^^^^^^^^^^^^^^^^^^

.. java:method:: @Override public boolean onOptionsItemSelected(MenuItem item)
   :outertype: HomeCarer

   This method is called when any action from the action bar is selected

   :param item: The menu item that was selected
   :return: in order for the method to work, true should be returned here

onResume
^^^^^^^^

.. java:method:: @Override protected void onResume()
   :outertype: HomeCarer

   When the page is loaded after the first time this method is run.

