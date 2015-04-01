.. java:import:: android.annotation TargetApi

.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.app AlertDialog

.. java:import:: android.app PendingIntent

.. java:import:: android.app ProgressDialog

.. java:import:: android.content ContentUris

.. java:import:: android.content DialogInterface

.. java:import:: android.content Intent

.. java:import:: android.content SharedPreferences

.. java:import:: android.media MediaPlayer

.. java:import:: android.net Uri

.. java:import:: android.os AsyncTask

.. java:import:: android.os Build

.. java:import:: android.os Bundle

.. java:import:: android.os StrictMode

.. java:import:: android.provider CalendarContract

.. java:import:: android.util Log

.. java:import:: android.view Menu

.. java:import:: android.view MenuInflater

.. java:import:: android.view MenuItem

.. java:import:: android.view SurfaceHolder

.. java:import:: android.view SurfaceView

.. java:import:: android.view View

.. java:import:: android.widget Button

.. java:import:: android.widget EditText

.. java:import:: android.widget TextView

.. java:import:: org.json JSONException

.. java:import:: org.json JSONObject

.. java:import:: java.io IOException

.. java:import:: java.util Calendar

.. java:import:: java.util HashMap

Login
=====

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class Login extends Activity implements SurfaceHolder.Callback

Fields
------
surfaceHolder
^^^^^^^^^^^^^

.. java:field::  SurfaceHolder surfaceHolder
   :outertype: Login

surfaceView
^^^^^^^^^^^

.. java:field::  SurfaceView surfaceView
   :outertype: Login

Methods
-------
onCreate
^^^^^^^^

.. java:method:: @Override protected void onCreate(Bundle savedInstanceState)
   :outertype: Login

   Runs when the login page is first loaded. Attempts to load the video that is on the home page of the web. Please not that this does not yet work. Loads the action bar. Add onClickListeners for the login, register and forgot password buttons on the page.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

onCreateOptionsMenu
^^^^^^^^^^^^^^^^^^^

.. java:method:: @Override public boolean onCreateOptionsMenu(Menu menu)
   :outertype: Login

   Creates the action bar items for the Login page

   :param menu: The options menu in which the items are placed
   :return: True must be returned in order for the options menu to be displayed

onOptionsItemSelected
^^^^^^^^^^^^^^^^^^^^^

.. java:method:: @Override public boolean onOptionsItemSelected(MenuItem item)
   :outertype: Login

   This method is called when any action from the action bar is selected

   :param item: The menu item that was selected
   :return: in order for the method to work, true should be returned here

registerWithServer
^^^^^^^^^^^^^^^^^^

.. java:method:: public void registerWithServer()
   :outertype: Login

   This method is not used. Was trial and error with the android notifications!

surfaceChanged
^^^^^^^^^^^^^^

.. java:method:: @Override public void surfaceChanged(SurfaceHolder h, int a, int b, int c)
   :outertype: Login

surfaceCreated
^^^^^^^^^^^^^^

.. java:method:: @Override public void surfaceCreated(SurfaceHolder holder)
   :outertype: Login

   Attempt in order to display the video, this currently runs the exception

   :param holder: The placeholder for the video.

surfaceDestroyed
^^^^^^^^^^^^^^^^

.. java:method:: @Override public void surfaceDestroyed(SurfaceHolder h)
   :outertype: Login

