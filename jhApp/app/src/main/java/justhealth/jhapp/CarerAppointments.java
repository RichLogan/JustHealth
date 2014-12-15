package justhealth.jhapp;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class CarerAppointments extends Activity {
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.carer_appointments);

        //Get data passed from MyPatients
        String username = "";
        String firstname = "";
        String surname = "";
        Bundle extras = getIntent().getExtras();
        if (extras != null) {
            username = extras.getString("targetUsername");
            firstname = extras.getString("firstName");
            surname = extras.getString("surname");
        }

        //Set text of patientName to username
        TextView title = (TextView) findViewById(R.id.patientName);
        title.setText("Appointments: " + firstname + " " + surname + " (" + username + ")");

        //Display Prescriptions
        displayAppointments(getAllAppointments(username));



    }

//    private void getUpcomingAppointments() {
//        //this will not work when API authentication is put in place
//        SharedPreferences account = getSharedPreferences("account", 0);
//        String username = account.getString("username", null);
//
//        HashMap<String, String> details = new HashMap<String, String>();
//
//        //Text Boxes
//        details.put("loggedInUser", username);
//        details.put("targetUser", username);
//        String postRequest = PostRequest.post("getAllAppointments", details);
//
//        JSONArray getApps = null;
//        try {
//            getApps = new JSONArray(postRequest);
//
//        } catch (JSONException e) {
//            e.printStackTrace();
//        }
//
//        assert getApps != null;
//        for (int i = 0; i < 5; i++) {
//            try {
//                JSONObject obj = getApps.getJSONObject(i);
//                String name = obj.getString("name");
//                String startDate = obj.getString("startdate");
//                String startTime = obj.getString("starttime");
//
//                Button app = new Button(this);
//                app.setText(name + " " + startDate + " " + startTime);
//
//            } catch (JSONException e) {
//                e.printStackTrace();
//            }
//        }
//
//      ;
//
//    }


    private JSONArray getAllAppointments(String targetUser) {
        HashMap<String, String> parameters = new HashMap<String, String>();
        String loggedInUser = getSharedPreferences("account", 0).getString("username", null);
        parameters.put("loggedInUser", loggedInUser);
        parameters.put("targetUser", targetUser);

        String response = PostRequest.post("getAllAppointments", parameters);
        try {
            JSONArray result = new JSONArray(response);
            System.out.println("Result IS:");
            System.out.println(result);
            return result;

        } catch (JSONException e) {
            e.printStackTrace();
        }
        return null;
    }


    private void displayAppointments(JSONArray appointmentList) {
        for(int x=0;x<appointmentList.length();x++) {
            try {
                JSONObject prescription = appointmentList.getJSONObject(x);

                final String creator = prescription.getString("creator");
                final String name = prescription.getString("name");
                final String addressnamenumber = prescription.getString("addressnamenumber");
                final String postcode = prescription.getString("postcode");
                final String startdate = prescription.getString("startdate");
                final String enddate = prescription.getString("enddate");
                final String description = prescription.getString("description");
                final String starttime = prescription.getString("starttime");

                System.out.println("Details:");
                System.out.println(prescription);



                //Create a button
                Button appointmentButtons = new Button(this);
                String appointmentString = name + " " + startdate + " " + starttime  ;
                appointmentButtons.setText(appointmentString);

                //Add button to view
                LinearLayout ll = (LinearLayout)findViewById(R.id.appointmentButtons);
                ll.addView(appointmentButtons,new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.MATCH_PARENT));

                LinearLayout.LayoutParams center = (LinearLayout.LayoutParams)appointmentButtons.getLayoutParams();
                center.gravity = Gravity.CENTER;
                appointmentButtons.setLayoutParams(center);
            }
            catch (JSONException e) {
                System.out.print(e.getStackTrace());
            }
        }
    }





}
