package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.LinearLayout.LayoutParams;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;


public class PatientMedication extends Activity {

    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.patient_medication);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Medication");

        displayPrescriptions(getPrescriptions());
    }

    private JSONArray getPrescriptions() {
        HashMap<String, String> parameters = new HashMap<String, String>();
        String username = getSharedPreferences("account", 0).getString("username", null);
        parameters.put("username", username);

        String response = Request.post("getPrescriptions", parameters, getApplicationContext());
            try {
                JSONArray result = new JSONArray(response);
                return result;

            } catch (JSONException e) {
                e.printStackTrace();
            }
        return null;
    }

    private void displayPrescriptions(JSONArray prescriptionList) {
        for(int x=0;x<prescriptionList.length();x++) {
            try {
                JSONObject prescription = prescriptionList.getJSONObject(x);
                final String username = prescription.getString("username");
                final String medication = prescription.getString("medication");
                final String dosage = prescription.getString("dosage");
                final String frequency = prescription.getString("frequency");
                final String quantity = prescription.getString("quantity");
                final String dosageunit = prescription.getString("dosageunit");
                final String frequencyunit = prescription.getString("frequencyunit");
                final String startdate = prescription.getString("startdate");
                final String enddate = prescription.getString("enddate");
                final String repeat = prescription.getString("repeat");
                final String stockleft = prescription.getString("stockleft");
                final String prerequisite = prescription.getString("prerequisite");
                final String dosageform = prescription.getString("dosageform");

                //Create a button
                Button prescriptionButton = new Button(this);
                String prescriptionString = medication + ":\n" + "Take " + quantity + " x " + dosage + " " + dosageunit + " " + dosageform + "(s)\n" + frequency + " x " + "a " + frequencyunit;
                prescriptionButton.setText(prescriptionString);

                //Add button to view
                LinearLayout ll = (LinearLayout)findViewById(R.id.prescriptionButtons);
                ll.addView(prescriptionButton,new LayoutParams(LayoutParams.MATCH_PARENT,LayoutParams.MATCH_PARENT));

                LinearLayout.LayoutParams center = (LinearLayout.LayoutParams)prescriptionButton.getLayoutParams();
                center.gravity = Gravity.CENTER;
                prescriptionButton.setLayoutParams(center);

                prescriptionButton.setOnClickListener(new View.OnClickListener() {
                    public void onClick(View v) {
                        AlertDialog.Builder alert = new AlertDialog.Builder(PatientMedication.this);
                        alert.setTitle(medication + " (" + dosage + dosageunit + ")");
                        alert.setMessage("Start Date: " + startdate + "\nEnd Date: " + enddate + "\nExtra Info: " + prerequisite + "\nRepeat: " + repeat);
                        alert.setNegativeButton("Got it!", new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int whichButton) {
                                // Cancelled.
                            }
                        });
                    alert.show();
                    }
                });
            }
            catch (JSONException e) {
                System.out.print(e.getStackTrace());
            }
        }
    }
}