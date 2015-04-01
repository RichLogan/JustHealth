.. java:import:: android.annotation TargetApi

.. java:import:: android.app ActionBar

.. java:import:: android.app Activity

.. java:import:: android.app AlertDialog

.. java:import:: android.app ProgressDialog

.. java:import:: android.content ContentResolver

.. java:import:: android.content ContentValues

.. java:import:: android.content Context

.. java:import:: android.content DialogInterface

.. java:import:: android.content Intent

.. java:import:: android.content SharedPreferences

.. java:import:: android.graphics.drawable ColorDrawable

.. java:import:: android.net Uri

.. java:import:: android.os AsyncTask

.. java:import:: android.os Build

.. java:import:: android.os Bundle

.. java:import:: android.os StrictMode

.. java:import:: android.provider CalendarContract

.. java:import:: android.util Base64

.. java:import:: android.view Gravity

.. java:import:: android.view View

.. java:import:: android.widget ArrayAdapter

.. java:import:: android.widget Button

.. java:import:: android.widget CheckBox

.. java:import:: android.widget EditText

.. java:import:: android.widget Spinner

.. java:import:: android.widget TextView

.. java:import:: android.widget Toast

.. java:import:: org.apache.http HttpResponse

.. java:import:: org.apache.http.client HttpClient

.. java:import:: org.apache.http.client.methods HttpPost

.. java:import:: org.apache.http.impl.client DefaultHttpClient

.. java:import:: org.apache.http.util EntityUtils

.. java:import:: org.json JSONArray

.. java:import:: org.json JSONException

.. java:import:: java.io IOException

.. java:import:: java.util ArrayList

.. java:import:: java.util Calendar

.. java:import:: java.util HashMap

CreateCarerPatientAppointment
=============================

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class CreateCarerPatientAppointment extends Activity

   Created by Stephen on 06/01/15. Allows a carer to create an appointment between themselves and a patient

Methods
-------
onCreate
^^^^^^^^

.. java:method:: protected void onCreate(Bundle savedInstanceState)
   :outertype: CreateCarerPatientAppointment

   This method runs when the page is first loaded. Sets the correct xml layout to be displayed and loads the action bar. Sets the action bar of the page and has an onclickListener applied to the create appointment button.

   :param savedInstanceState: a bundle if the state of the application was to be saved.

