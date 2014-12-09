package justhealth.jhapp;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.StrictMode;
import android.support.v7.app.ActionBarActivity;
import android.util.Base64;
import android.view.View;
import android.widget.Adapter;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TabHost;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

/**
 * Created by Stephen on 09/12/14.
 */
public class PatientAppointments extends ActionBarActivity {
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

        HttpPost httppost = new HttpPost("http://127.0.0.1:9999/api/getAppointmentTypes");
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
                    JSONObject jsonobject = appointmentTypes.getJSONObject(i);
                    System.out.println(jsonobject.toString());
                    populateSpinner.add(jsonobject.optString("type"));
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }

        } catch (IOException e) {
            e.printStackTrace();
        }

        Spinner appointmentType = (Spinner) findViewById(R.id.type);
        appointmentType.setAdapter(new ArrayAdapter<String>(this,
                android.R.layout.simple_spinner_dropdown_item,
                populateSpinner));
    }


    private void createApp() {

        HashMap<String, String> details = new HashMap<String, String>();

        //Text Boxes
        details.put("name", ((EditText) findViewById(R.id.name)).getText().toString());
        details.put("apptype", ((Spinner) findViewById(R.id.type)).toString());
    }

}
