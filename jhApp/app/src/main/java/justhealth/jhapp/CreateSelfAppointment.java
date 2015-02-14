package justhealth.jhapp;

import android.annotation.TargetApi;
import android.app.ActionBar;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Context;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.graphics.drawable.ColorDrawable;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.StrictMode;
import android.provider.CalendarContract;
import android.util.Base64;
import android.view.Gravity;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;

/**
 * Created by Stephen on 05/01/15.
 */
public class CreateSelfAppointment extends Activity {

    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.create_self_appointment);
        // Set up your ActionBar
        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Create Appointment");
        // You customization
        final int actionBarColor = getResources().getColor(R.color.action_bar);
        actionBar.setBackgroundDrawable(new ColorDrawable(actionBarColor));

        Button createAppointment = (Button) findViewById(R.id.buttonAppointment);
        createAppointment.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        createApp();
                    }
                }
        );


        populateSpinner();
    }

    /**
     * This makes a post request to the database to get the appointment types and populates the
     * spinner with these.
     */
    private void populateSpinner() {
        System.out.println("populateSpinner");
        ArrayList populateSpinner = new ArrayList<String>();

        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        String password = account.getString("password", null);

        //Create new HttpClient and Post Header
        HttpClient httpclient = new DefaultHttpClient();
        String authentication = username + ":" + password;
        String encodedAuthentication = Base64.encodeToString(authentication.getBytes(), Base64.NO_WRAP);

        HttpPost httppost = new HttpPost("http://raptor.kent.ac.uk:5000/api/getAppointmentTypes");
        httppost.setHeader("Authorization", "Basic " + encodedAuthentication);
        try {
            //pass the list to the post request
            HttpResponse response = httpclient.execute(httppost);
            System.out.println("post request executed");

            String responseString = EntityUtils.toString(response.getEntity());
            System.out.println("this is the array: " + responseString);

            JSONArray appointmentTypes = null;


            try {
                appointmentTypes = new JSONArray(responseString);
                for (int i = 0; i < appointmentTypes.length(); i++) {
                    String app = appointmentTypes.getString(i);
                    populateSpinner.add(app);
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }

        } catch (IOException e) {
            e.printStackTrace();
        }

        Spinner appointmentType = (Spinner) findViewById(R.id.type);
        appointmentType.setAdapter(new ArrayAdapter<String>(this, android.R.layout.simple_spinner_dropdown_item, populateSpinner));
    }


    /**
     * This method is called to create the appointment. It grabs all of the text etc from the text
     * boxes and adds these to a HashMap.
     * Following this, a POST request is made to the API sending the HashMap of the appointment details.
     * It then will display Appointment added/something went wrong.
     * If appointment is added the method to produce the pop up asking if the user wants to add the appointment
     * to their calendar is called.
     */
    private void createApp() {

        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        String password = account.getString("password", null);

        HashMap<String, String> details = new HashMap<String, String>();

        //Text Boxes
        details.put("creator", username);
        details.put("name", ((EditText) findViewById(R.id.name)).getText().toString());
        details.put("addressnamenumber", ((EditText) findViewById(R.id.buildingNameNumber)).getText().toString());
        details.put("postcode", ((EditText) findViewById(R.id.postcode)).getText().toString());
        details.put("startdate", ((EditText) findViewById(R.id.startDate)).getText().toString());
        details.put("starttime", ((EditText) findViewById(R.id.startTime)).getText().toString());
        details.put("enddate", ((EditText) findViewById(R.id.endDate)).getText().toString());
        details.put("endtime", ((EditText) findViewById(R.id.endTime)).getText().toString());
        details.put("description", ((EditText) findViewById(R.id.details)).getText().toString());

        final Spinner appTypeSpinner = (Spinner) findViewById((R.id.type));
        final String appType = String.valueOf(appTypeSpinner.getSelectedItem());
        details.put("apptype", appType);

        if (((CheckBox) findViewById(R.id.appPrivate)).isChecked() == true) {
            details.put("private", "True");
        } else {
            details.put("private", "False");
        }

        String responseString = Request.post("addPatientAppointment", details, this);
        int id = Integer.parseInt(responseString);
        System.out.println(responseString);

        if (id > 0) {
            //show the alert to say it is successful
            Context context = getApplicationContext();
            CharSequence text = "Appointment Added.";
            //Length
            int duration = Toast.LENGTH_LONG;
            Toast toast = Toast.makeText(context, text, duration);
            //Position
            toast.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL, 0, 100);
            toast.show();
            addToCalendarQuestion(details, id);
        }
        else {
            Context context = getApplicationContext();
            CharSequence text = "Oops, something went wrong. Please try again.";
            //Length
            int duration = Toast.LENGTH_LONG;
            Toast toast = Toast.makeText(context, text, duration);
            //Position
            toast.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL, 0, 100);
            toast.show();
        }
    }


    /**
     * This displays a pop up that asks the user whether they want to add the appointment to their
     * native android calendar. If yes, another method is invoked to do this.
     * @param details all of the details about the appointment
     * @param id the id of the appointment in the database
     */
    private void addToCalendarQuestion(final HashMap<String, String> details, final int id) {
        AlertDialog.Builder alert = new AlertDialog.Builder(this);

        alert.setTitle("Add To Calendar");
        alert.setMessage("Do you want to add this appointment to your phones calendar?");

        alert.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int whichButton) {
                addToCalendar(details, id);
            }
        });

        alert.setNegativeButton("No", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int whichButton) {
                finish();
                getIntent();
            }
        });

        alert.show();
    }

    //Calendar example
    @TargetApi(Build.VERSION_CODES.ICE_CREAM_SANDWICH)
    private void addToCalendar(HashMap<String, String> details, int id) {
        String appName = details.get("name");
        String location = details.get("addressnamenumber") + ", " + details.get("postcode");
        String startDate = details.get("startdate");
        String startTime = details.get("starttime");
        String endDate = details.get("enddate");
        String endTime = details.get("endtime");
        String description = details.get("description");

        //get the correct format of the start date/time of the calendar appointment
        HashMap<String, Integer> appStart = getDateTimeFormat(startDate, startTime);
        System.out.println(appStart);

        //get the correct format of the end date/time of the calendar appointment
        HashMap<String, Integer> appEnd = getDateTimeFormat(endDate, endTime);
        System.out.println(appEnd);

        Calendar start = Calendar.getInstance();
        start.set(appStart.get("year"), appStart.get("month"), appStart.get("day"), appStart.get("hour"), appStart.get("minute"));
        Calendar end = Calendar.getInstance();
        end.set(appEnd.get("year"), appEnd.get("month"), appEnd.get("day"), appEnd.get("hour"), appEnd.get("minute"));

        /*Intent intent = new Intent(Intent.ACTION_INSERT)
                .setData(CalendarContract.Events.CONTENT_URI)
                .putExtra(CalendarContract.EXTRA_EVENT_BEGIN_TIME, start.getTimeInMillis())
                .putExtra(CalendarContract.EXTRA_EVENT_END_TIME, end.getTimeInMillis())
                .putExtra(CalendarContract.Events.TITLE, appName)
                .putExtra(CalendarContract.Events.EVENT_LOCATION,location)
                .putExtra(CalendarContract.Events._ID, "JustHealth001");
        startActivity(intent);

        Intent intent1 = getIntent();
        System.out.println(intent1.getStringExtra(CalendarContract.Events.CONTENT_URI.toString()));*/

        ContentResolver cr = getContentResolver();
        ContentValues values = new ContentValues();
        values.put(CalendarContract.Events.DTSTART, start.getTimeInMillis());
        values.put(CalendarContract.Events.DTEND, end.getTimeInMillis());
        values.put(CalendarContract.Events.TITLE, appName);
        values.put(CalendarContract.Events.DESCRIPTION, description);
        values.put(CalendarContract.Events.EVENT_TIMEZONE, location);
        values.put(CalendarContract.Events.CALENDAR_ID, 1);
        Uri uri = cr.insert(CalendarContract.Events.CONTENT_URI, values);

        // get the event ID that is the last element in the Uri
        int eventID = Integer.parseInt(uri.getLastPathSegment());
        System.out.println(eventID);

        //show the alert to say it is successful
        Context context = getApplicationContext();
        CharSequence text = "This appointment has been added to your phone's calendar";
        //Length
        int duration = Toast.LENGTH_LONG;
        Toast toast = Toast.makeText(context, text, duration);
        //Position
        toast.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL, 0, 100);
        toast.show();


        //add the android event ID to the database
        HashMap<String, String> infoToUpdate = new HashMap<String, String>();
        infoToUpdate.put("dbid", Integer.toString(id));
        infoToUpdate.put("androidid", Integer.toString(eventID));
        System.out.println(infoToUpdate);
        String responseString = Request.post("addAndroidEventId", infoToUpdate, this);
        System.out.println(responseString);
        finish();
        getIntent();

    }

    /**
     * This method takes the date and time of the appointment and adds each part to a HashMap.
     * This is needed when adding the appointment to the native android calendar.
     * @param date the date of the appointment to be added to the android calendar
     * @param time the time of the appointment to be added to the android calendar
     * @return a HashMap of the date and time of the appointment
     */
    private HashMap<String, Integer> getDateTimeFormat(String date, String time) {
        HashMap<String, Integer> formattedDateTime = new HashMap<>();

        System.out.println(date);
        System.out.println(time);
        Integer year = Integer.parseInt(date.substring(0,4));
        Integer month = Integer.parseInt(date.substring(5,7));
        month -= 1;  //because January = 0... December = 11
        Integer day = Integer.parseInt(date.substring(8,10));
        Integer hour = Integer.parseInt(time.substring(0,2));
        Integer minute = Integer.parseInt(time.substring(3,5));

        formattedDateTime.put("year", year);
        formattedDateTime.put("month", month);
        formattedDateTime.put("day", day);
        formattedDateTime.put("hour", hour);
        formattedDateTime.put("minute", minute);
        return formattedDateTime;
    }
}
