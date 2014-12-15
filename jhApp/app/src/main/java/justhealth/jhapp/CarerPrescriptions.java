package justhealth.jhapp;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class CarerPrescriptions extends Activity{
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.carer_prescriptions);

        //Get data passed from MyPatients
        String username = "";
        String firstname = "";
        String surname= "";
        final Bundle extras = getIntent().getExtras();
        if (extras != null) {
            username = extras.getString("targetUsername");
            firstname = extras.getString("firstName");
            surname = extras.getString("surname");
        }

        Button addNewPrescription = (Button)findViewById(R.id.addNewPrescription);
        addNewPrescription.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    Intent intent = new Intent(getBaseContext(), AddPrescription.class);
                    String username =  extras.getString("targetUsername");
                    intent.putExtra("username", username);
                    startActivity(intent);
                }
            }
        );

        //Set text of patientName to username
        TextView title=(TextView)findViewById(R.id.patientName);
        title.setText("Prescriptions: " + firstname + " " + surname + " (" + username + ")");

        //Display Prescriptions
        displayPrescriptions(getPrescriptions(username));
    }

    private JSONArray getPrescriptions(String username) {
        HashMap<String, String> parameters = new HashMap<String, String>();
        parameters.put("username", username);

        String response = PostRequest.post("getPrescriptions", parameters);
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
                final JSONObject prescription = prescriptionList.getJSONObject(x);
                final String prescriptionid = prescription.getString("prescriptionid");
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
                ll.addView(prescriptionButton,new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.MATCH_PARENT));

                LinearLayout.LayoutParams center = (LinearLayout.LayoutParams)prescriptionButton.getLayoutParams();
                center.gravity = Gravity.CENTER;
                prescriptionButton.setLayoutParams(center);

                prescriptionButton.setOnClickListener(new View.OnClickListener() {
                    public void onClick(View v) {
                        AlertDialog.Builder alert = new AlertDialog.Builder(CarerPrescriptions.this);
                        alert.setTitle(medication + " (" + dosage + dosageunit + ")");
                        alert.setMessage("Start Date: " + startdate + "\nEnd Date: " + enddate + "\nExtra Info: " + prerequisite + "\nRepeat: " + repeat);
                        alert.setNegativeButton("Edit", new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int whichButton) {
                                Intent intent = new Intent(getBaseContext(), EditPrescription.class);
                                intent.putExtra("prescriptionid", prescriptionid);
                                intent.putExtra("targetUsername", username);
                                startActivityForResult(intent, 1);
                            }
                        });
                        alert.setPositiveButton("Got It!", new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int whichButton) {
                            //Cancelled
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

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        // TODO Auto-generated method stub
        super.onActivityResult(requestCode, resultCode, data);
        if(data.getExtras().containsKey("response")){
            Boolean success = (resultCode == 1);
            Feedback.toast(data.getStringExtra("response"), success, getApplicationContext());
            finish();
            startActivity(getIntent());
        }
    }
}