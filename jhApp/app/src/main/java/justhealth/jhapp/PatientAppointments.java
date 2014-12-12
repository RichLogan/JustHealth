package justhealth.jhapp;

import android.annotation.TargetApi;
import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.Bundle;
import android.os.StrictMode;
import android.provider.CalendarContract;
import android.support.v7.app.ActionBarActivity;
import android.util.Base64;
import android.view.View;
import android.widget.Adapter;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Spinner;
import android.widget.TabHost;
import android.widget.TextView;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Created by Stephen on 09/12/14.
 */
public class PatientAppointments extends Activity {
    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.patient_appointments);

        TabHost tabHost = (TabHost) findViewById(R.id.tabHost);
        tabHost.setup();

        TabHost.TabSpec tabSpec = tabHost.newTabSpec("Upcoming");
        tabSpec.setContent(R.id.upcomingAppointmentView);
        tabSpec.setIndicator("Upcoming");
        tabHost.addTab(tabSpec);


        tabSpec = tabHost.newTabSpec("Create");
        tabSpec.setContent(R.id.createAppointmentView);
        tabSpec.setIndicator("Create");
        tabHost.addTab(tabSpec);

        Button createAppointment = (Button) findViewById(R.id.buttonAppointment);
        createAppointment.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        createApp();
                    }
                }
        );

        tabSpec = tabHost.newTabSpec("Archived");
        tabSpec.setContent(R.id.archiveAppointmentView);
        tabSpec.setIndicator("Archived");
        tabHost.addTab(tabSpec);

        populateSpinner();
        getUpcomingAppointments();

        //Trial and error with the calendar
        //new CalendarAppointments().addEvent(/*"title", "11", "SS17 9AY", "a description of this event", "20-12-2014", "09:00", "20-12-2014", "10:00"*/);
        //calendar();
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
    }


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

        if (((CheckBox) findViewById(R.id.appPrivate)).isChecked()) {
            details.put("private", "TRUE");
        } else {
            details.put("private", "FALSE");
        }

        HttpClient httpclient = new DefaultHttpClient();
        String authentication = username + ":" + password;
        String encodedAuthentication = Base64.encodeToString(authentication.getBytes(), Base64.NO_WRAP);

        HttpPost httppost = new HttpPost("http://raptor.kent.ac.uk:5000/api/addPatientAppointment");
        httppost.setHeader("Authorization", "Basic " + encodedAuthentication);
        try {
            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);

            Set<Map.Entry<String, String>> detailsSet = details.entrySet();
            for (Map.Entry<String, String> string : detailsSet) {
                nameValuePairs.add(new BasicNameValuePair(string.getKey(), string.getValue()));
                System.out.println(nameValuePairs);
            }

            //pass the list to the post request
            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
            System.out.println(httppost);
            HttpResponse response = httpclient.execute(httppost);
            String responseString = EntityUtils.toString(response.getEntity());

            System.out.println(responseString);

            //Check if the Layout already exists
            LinearLayout alert = (LinearLayout) findViewById(R.id.successMessage);
            if (alert == null) {
                //Insert the alert message
                LinearLayout insertAlert = (LinearLayout) findViewById(R.id.insertAlert);
                View insertAlertView = getLayoutInflater().inflate(R.layout.success_message, insertAlert, false);
                insertAlert.addView(insertAlertView);
            }

            TextView myTextView = (TextView) findViewById(R.id.successText);
            myTextView.setText(responseString);

        } catch (ClientProtocolException e) {
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    private void getUpcomingAppointments() {
        //this will not work when API authentication is put in place
        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        String password = account.getString("password", null);

        HashMap<String, String> details = new HashMap<String, String>();

        //Text Boxes
        details.put("loggedInUser", username);
        details.put("targetUser", username);
        String postRequest = PostRequest.post("getAllAppointments", details);

        JSONArray getApps = null;
        try {
            getApps = new JSONArray(postRequest);

        } catch (JSONException e) {
            e.printStackTrace();
        }

        assert getApps != null;
        for (int i = 0; i < 5; i++) {
            try {
                JSONObject obj = getApps.getJSONObject(i);
                String name = obj.getString("name");
                String startDate = obj.getString("startdate");
                String startTime = obj.getString("starttime");

                Button app = new Button(this);
                app.setText(name + " " + startDate + " " + startTime);
                LinearLayout layout = (LinearLayout) findViewById(R.id.upcomingAppointmentView);
                layout.addView(app);

            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }


    /* Calendar example

    @TargetApi(Build.VERSION_CODES.ICE_CREAM_SANDWICH)
    private void calendar() {
        Calendar beginTime = Calendar.getInstance();
        beginTime.set(2014, 12, 25, 9, 50);
        Calendar endTime = Calendar.getInstance();
        endTime.set(2014, 12, 25, 17, 30);

        Intent intent = new Intent(Intent.ACTION_INSERT)
                .setData(CalendarContract.Events.CONTENT_URI)
                .putExtra(CalendarContract.EXTRA_EVENT_BEGIN_TIME, beginTime.getTimeInMillis())
                .putExtra(CalendarContract.EXTRA_EVENT_END_TIME, endTime.getTimeInMillis())
                .putExtra(CalendarContract.Events.TITLE, "Christmas Day Shananigans")
                .putExtra(CalendarContract.Events.EVENT_LOCATION, "SS17 9AY");
        startActivity(intent);

        System.out.println("Event ID: " + CalendarContract.Events.CONTENT_URI);
    }*/



}
