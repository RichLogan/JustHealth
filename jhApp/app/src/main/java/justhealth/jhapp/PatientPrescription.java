package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class PatientPrescription extends Activity {

    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.patient_prescription);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Your Prescriptions");

        getPrescriptions();
    }

    private void getPrescriptions() {
        final HashMap<String, String> parameters = new HashMap<String, String>();
        String username = getSharedPreferences("account", 0).getString("username", null);
        parameters.put("username", username);

        new AsyncTask<Void, Void, JSONArray>() {
            ProgressDialog progressDialog;

            @Override
            protected void onPreExecute() {
                progressDialog = ProgressDialog.show(PatientPrescription.this, "Loading...", "Loading your prescriptions", true);
            }

            @Override
            protected JSONArray doInBackground(Void... params) {
                try {
                    String response = Request.post("getPrescriptions", parameters, getApplicationContext());
                    return new JSONArray(response);
                } catch (Exception e) {
                    return null;
                }
            }

            @Override
            protected void onPostExecute(JSONArray response) {
                try {
                    super.onPostExecute(response);
                    JSONArray prescriptionList = response;
                    displayPrescriptions(prescriptionList);
                    progressDialog.dismiss();

                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }.execute();

    }

    private void displayPrescriptions(JSONArray prescriptionList) {
        for (int x = 0; x < prescriptionList.length(); x++) {
            try {
                final JSONObject prescription = prescriptionList.getJSONObject(x);
                final String username = prescription.getString("username");
                final String medication = prescription.getString("medication");
                final String dosage = prescription.getString("dosage");
                final String frequency = prescription.getString("frequency");
                final String quantity = prescription.getString("quantity");
                final String dosageunit = prescription.getString("dosageunit");
                final String startdate = prescription.getString("startdate");
                final String enddate = prescription.getString("enddate");
                final String stockleft = prescription.getString("stockleft");
                final String prerequisite = prescription.getString("prerequisite");
                final String dosageform = prescription.getString("dosageform");

                //Create a button
                Button prescriptionButton = new Button(this);
                String prescriptionString = medication + ":\n"
                        + "Take " + quantity + " x " + dosage + " " + dosageunit + " "
                        + dosageform + "(s)\n" + frequency + " times " + "a day";
                prescriptionButton.setText(prescriptionString);

                // Can't set styles, so have to do it manually
                Style.styleButton(
                        prescriptionButton,
                        "primary",
                        (LinearLayout) findViewById(R.id.prescriptionButtons),
                        getApplicationContext());

                prescriptionButton.setOnClickListener(new View.OnClickListener() {
                    public void onClick(View v) {
                        AlertDialog.Builder alert = new AlertDialog.Builder(PatientPrescription.this);
                        alert.setTitle(medication + " (" + dosage + dosageunit + ")");
                        alert.setMessage(
                            "Stock Left: " + stockleft + "\n"
                            + "Start Date: " + startdate + "\n"
                            + "End Date: " + enddate + "\n"
                            + "Extra Info: " + prerequisite);
                        alert.setPositiveButton("Take this prescription", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                Intent intent = new Intent(PatientPrescription.this, TakePrescription.class);
                                intent.putExtra("prescription", prescription.toString());
                                startActivity(intent);
                            }
                        });
                        alert.setNegativeButton("Got it!", null);
                        alert.show();
                    }
                });
            } catch (JSONException e) {
                System.out.print(e.getStackTrace());
            }
        }
    }
}