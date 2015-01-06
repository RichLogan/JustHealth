package justhealth.jhapp;

import android.annotation.TargetApi;
import android.app.ActionBar;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.drawable.ColorDrawable;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.StrictMode;
import android.provider.CalendarContract;
import android.util.Base64;
import android.util.Log;
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
public class EditSelfAppointment extends Activity {

    //id of the appointment being edited
    private String appId;
    private String androidAppId;
    private String appType;


    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.create_self_appointment);
        // Set up your ActionBar
        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Update Appointment");
        // You customization
        final int actionBarColor = getResources().getColor(R.color.action_bar);
        actionBar.setBackgroundDrawable(new ColorDrawable(actionBarColor));

        Button createAppointment = (Button) findViewById(R.id.buttonAppointment);
        createAppointment.setText("Update");
        createAppointment.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        updateAppointment();
                    }
                }
        );


        setCurrentDetails(getIntent());
        populateSpinner();
    }

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
        //This isn't great, had to hard code it and if the options change then this will need to change.
        //Not sure about another way to do it
        for (int i = 0; i < populateSpinner.size(); i++) {
            if(populateSpinner.get(i).equals(appType)) {
                appointmentType.setSelection(i);
                return;
            }
        }
    }

    private void setCurrentDetails(Intent intent) {
        HashMap<String, String> appointment = (HashMap<String, String>) intent.getSerializableExtra("appointmentDetails");
        appId = appointment.get("appid");
        String name = appointment.get("name");
        appType = appointment.get("appType");
        String startDate = appointment.get("startDate");
        String startTime = appointment.get("startTime");
        String endDate = appointment.get("endDate");
        String endTime = appointment.get("endTime");
        String address = appointment.get("addressNameNumber");
        String postcode = appointment.get("postcode");
        String details = appointment.get("details");
        String isPrivate = appointment.get("private");
        androidAppId = appointment.get("androidId");

        EditText appName = (EditText) findViewById(R.id.name);
        appName.setText(name);

        EditText appBuildingNameNumber = (EditText) findViewById(R.id.buildingNameNumber);
        appBuildingNameNumber.setText(address);

        EditText appPostcode = (EditText) findViewById(R.id.postcode);
        appPostcode.setText(postcode);

        EditText appStartDate = (EditText) findViewById(R.id.startDate);
        appStartDate.setText(startDate);

        EditText appStartTime = (EditText) findViewById(R.id.startTime);
        appStartTime.setText(startTime);

        EditText appEndDate = (EditText) findViewById(R.id.endDate);
        appEndDate.setText(endDate);

        EditText appEndTime = (EditText) findViewById(R.id.endTime);
        appEndTime.setText(endTime);

        EditText appDetails = (EditText) findViewById(R.id.details);
        appDetails.setText(details);

        CheckBox appPrivate = (CheckBox) findViewById(R.id.appPrivate);
        System.out.println(isPrivate);
        if(isPrivate.equals("true")) {
            appPrivate.setChecked(true);
        }
        else {
            appPrivate.setChecked(false);
        }

    }

    private void updateAppointment() {

        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        String password = account.getString("password", null);

        HashMap<String, String> details = new HashMap<String, String>();

        //Text Boxes
        details.put("appid", appId);
        details.put("creator", username);
        details.put("name", ((EditText) findViewById(R.id.name)).getText().toString());
        details.put("addressnamenumber", ((EditText) findViewById(R.id.buildingNameNumber)).getText().toString());
        details.put("postcode", ((EditText) findViewById(R.id.postcode)).getText().toString());
        details.put("startdate", ((EditText) findViewById(R.id.startDate)).getText().toString());
        details.put("starttime", ((EditText) findViewById(R.id.startTime)).getText().toString());
        details.put("enddate", ((EditText) findViewById(R.id.endDate)).getText().toString());
        details.put("endtime", ((EditText) findViewById(R.id.endTime)).getText().toString());
        details.put("other", ((EditText) findViewById(R.id.details)).getText().toString());

        final Spinner appTypeSpinner = (Spinner) findViewById((R.id.type));
        final String appType = String.valueOf(appTypeSpinner.getSelectedItem());
        details.put("apptype", appType);

        if (((CheckBox) findViewById(R.id.appPrivate)).isChecked() == true) {
            details.put("private", "True");
        } else {
            details.put("private", "False");
        }

        String responseString = Request.post("updateAppointment", details, this);
        System.out.println(responseString);

        //Check if the Layout already exists
        LinearLayout alert = (LinearLayout) findViewById(R.id.successMessage);
        if (alert == null) {
            //Insert the alert message
            LinearLayout insertAlert = (LinearLayout) findViewById(R.id.insertAlert);
            View insertAlertView = getLayoutInflater().inflate(R.layout.success_message, insertAlert, false);
            insertAlert.addView(insertAlertView);
            TextView myTextView = (TextView) findViewById(R.id.successText);

            if (responseString.equals("Appointment Updated")) {
                myTextView.setText("Success! Appointment Updated.");
                updateNativeCalendarQuestion(details);
            }
            else {
                myTextView.setText("Oops something went wrong, try again.");
            }
        }
    }

    private void updateNativeCalendarQuestion(final HashMap<String, String> details) {
        AlertDialog.Builder alert = new AlertDialog.Builder(this);

        alert.setTitle("Update Native Calendar");
        alert.setMessage("Do you want to update this appointment in your phones calendar?");

        alert.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int whichButton) {
                updateCalendar(details);
            }
        });

        alert.setNegativeButton("No", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int whichButton) {
                // Cancelled.
            }
        });

        alert.show();
    }

    @TargetApi(Build.VERSION_CODES.ICE_CREAM_SANDWICH)
    private void updateCalendar(HashMap<String, String> details) {
        long appointmentID = Long.parseLong(androidAppId);

        String appName = details.get("name");
        String location = details.get("addressnamenumber") + ", " + details.get("postcode");
        String startDate = details.get("startdate");
        String startTime = details.get("starttime");
        String endDate = details.get("enddate");
        String endTime = details.get("endtime");
        String description = details.get("description");

        //get the correct format of the start date/time of the calendar appointment
        HashMap<String, Integer> appStart = getDateTimeFormat(startDate, startTime);
        Calendar start = Calendar.getInstance();
        start.set(appStart.get("year"), appStart.get("month"), appStart.get("day"), appStart.get("hour"), appStart.get("minute"));

        //get the correct format of the end date/time of the calendar appointment
        HashMap<String, Integer> appEnd = getDateTimeFormat(endDate, endTime);
        Calendar end = Calendar.getInstance();
        end.set(appEnd.get("year"), appEnd.get("month"), appEnd.get("day"), appEnd.get("hour"), appEnd.get("minute"));

        ContentResolver cr = getContentResolver();
        ContentValues values = new ContentValues();
        Uri updateUri = null;
        // The new title for the event
        values.put(CalendarContract.Events.DTSTART, start.getTimeInMillis());
        values.put(CalendarContract.Events.DTEND, end.getTimeInMillis());
        values.put(CalendarContract.Events.TITLE, appName);
        values.put(CalendarContract.Events.DESCRIPTION, description);
        values.put(CalendarContract.Events.EVENT_TIMEZONE, location);
        values.put(CalendarContract.Events.CALENDAR_ID, 1);
        updateUri = ContentUris.withAppendedId(CalendarContract.Events.CONTENT_URI, appointmentID);
        int rows = getContentResolver().update(updateUri, values, null, null);

        if (rows > 0) {
            //show the alert to say it is successful
            Context context = getApplicationContext();
            CharSequence text = "This appointment has been updated in your phone's calendar";
            //Length
            int duration = Toast.LENGTH_LONG;
            Toast toast = Toast.makeText(context, text, duration);
            //Position
            toast.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL, 0, 100);
            toast.show();
        }
        finish();
    }

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
