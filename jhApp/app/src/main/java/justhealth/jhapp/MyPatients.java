package justhealth.jhapp;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class MyPatients extends Activity {

    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.my_patients);

        String username = getSharedPreferences("account", 0).getString("username", null);
        displayPatients(getPatients(username));
    }

    private JSONArray getPatients(String username) {
        HashMap<String, String> parameters = new HashMap<String, String>();
        parameters.put("username", username);

        String response = Request.post("getConnections", parameters, getApplicationContext());
        try {
            JSONObject allConnections = new JSONObject(response);
            String completed = allConnections.getString("completed");
            JSONArray completedConnections = new JSONArray(completed);
            return completedConnections;
        } catch (JSONException e) {
            System.out.println(e.getStackTrace());
        }
        return null;
    }

    private void displayPatients(JSONArray patients) {
        for (int x = 0; x < patients.length(); x++) {
            try {
                JSONObject patient = patients.getJSONObject(x);
                final String username = patient.getString("username");
                final String firstname = patient.getString("firstname");
                final String surname = patient.getString("surname");
                final String accounttype = patient.getString("accounttype");

                if (accounttype.equals("Patient")) {
                    //Create a button
                    Button patientButton = new Button(this);
                    String patientString = username + "\n" + firstname + " " + surname;
                    patientButton.setText(patientString);

                    //Add button to view
                    LinearLayout ll = (LinearLayout) findViewById(R.id.patientButtons);
                    ll.addView(patientButton, new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.MATCH_PARENT));

                    LinearLayout.LayoutParams center = (LinearLayout.LayoutParams) patientButton.getLayoutParams();
                    center.gravity = Gravity.CENTER;
                    patientButton.setLayoutParams(center);

                    patientButton.setOnClickListener(new View.OnClickListener() {
                        public void onClick(View v) {
                            AlertDialog.Builder alert = new AlertDialog.Builder(MyPatients.this);
                            alert.setTitle("Patient Options")
                                .setItems(R.array.patient_options, new DialogInterface.OnClickListener() {
                                    public void onClick(DialogInterface dialog, int which) {
                                        if (which == 0) {
                                            Intent intent = new Intent(getBaseContext(), CarerPrescriptions.class);
                                            intent.putExtra("targetUsername", username);
                                            intent.putExtra("firstName", firstname);
                                            intent.putExtra("surname", surname);
                                            startActivity(intent);
                                        }
                                        else if (which == 1) {
                                            Intent intent = new Intent(getBaseContext(), CarerAppointments.class);
                                            intent.putExtra("targetUsername", username);
                                            intent.putExtra("firstName", firstname);
                                            intent.putExtra("surname", surname);
                                            startActivity(intent);
                                        }
                                    }
                                });
                                alert.show();
                        }
                    });
                }
            } catch (JSONException e) {
                System.out.print(e.getStackTrace());
            }
        }
    }
}