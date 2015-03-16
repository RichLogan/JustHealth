package justhealth.jhapp;

import android.annotation.TargetApi;
import android.app.ActionBar;
import android.app.Activity;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.TextView;

import java.util.HashMap;

/**
 * Created by Stephen on 16/03/15.
 */
public class ViewAppointment extends Activity {
    @TargetApi(Build.VERSION_CODES.HONEYCOMB)
    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.view_appointment);

        // Set up your ActionBar
        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Appointment Details");

        Button updateAppointment = (Button) findViewById(R.id.buttonAppointment);
        updateAppointment.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        //Edit appointment
                        Intent intent = new Intent(ViewAppointment.this, EditSelfAppointment.class);
                        intent.putExtra("appointmentDetails", getIntent().getSerializableExtra("appointmentDetails"));
                        startActivity(intent);
                    }
                }
        );

        display(getIntent());
    }

    private void display(Intent intent) {
        HashMap<String, String> appointment = (HashMap<String, String>) intent.getSerializableExtra("appointmentDetails");
        String appId = appointment.get("appid");
        String name = appointment.get("name");
        String appType = appointment.get("appType");
        String startDate = appointment.get("startDate");
        String startTime = appointment.get("startTime");
        String endDate = appointment.get("endDate");
        String endTime = appointment.get("endTime");
        String address = appointment.get("addressNameNumber");
        String postcode = appointment.get("postcode");
        String details = appointment.get("details");
        String isPrivate = appointment.get("private");
        String androidAppId = appointment.get("androidId");

        TextView appName = (TextView) findViewById(R.id.appointmentTitle);
        appName.setText(name);

        TextView appointmentType = (TextView) findViewById(R.id.type);
        appointmentType.setText(appType);

        TextView appBuildingNameNumber = (TextView) findViewById(R.id.buildingNameNumber);
        appBuildingNameNumber.setText(address);

        TextView appPostcode = (TextView) findViewById(R.id.postcode);
        appPostcode.setText(postcode);

        TextView appStartDate = (TextView) findViewById(R.id.startDate);
        appStartDate.setText(startDate);

        TextView appStartTime = (TextView) findViewById(R.id.startTime);
        appStartTime.setText(startTime);

        TextView appEndDate = (TextView) findViewById(R.id.endDate);
        appEndDate.setText(endDate);

        TextView appEndTime = (TextView) findViewById(R.id.endTime);
        appEndTime.setText(endTime);

        if (details.equals("")) {
            details = "No additional details provided";
        }
        TextView appDetails = (TextView) findViewById(R.id.details);
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
    }

