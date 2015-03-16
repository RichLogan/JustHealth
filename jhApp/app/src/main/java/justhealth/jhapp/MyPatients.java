package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class MyPatients extends Activity {

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.my_patients);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Patients");

        loadPatients();
    }

    private void loadPatients() {
        final HashMap<String, String> parameters = new HashMap<String, String>();
        parameters.put("username", getSharedPreferences("account", 0).getString("username", null));

        new AsyncTask<Void, Void, JSONArray>() {
            ProgressDialog progressDialog;

            @Override
            protected void onPreExecute() {
                progressDialog = ProgressDialog.show(MyPatients.this, "Loading...", "Loading your patients", true);
            }

            @Override
            protected JSONArray doInBackground(Void... params) {
                try {
                    String response = Request.post("getConnections", parameters, getApplicationContext());
                    return new JSONArray(new JSONObject(response).getString("completed"));
                } catch (JSONException e) {
                    return null;
                }
            }

            @Override
            protected void onPostExecute(JSONArray result) {
                try {
                    super.onPostExecute(result);
                    displayPatients(result);
                    progressDialog.dismiss();
                } catch (NullPointerException e) {
                    Feedback.toast("Could not load your patients", false, getApplicationContext());
                }
            }
        }.execute();
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
                    String patientString = firstname + " " + surname + "\n" + "(" + username + ")";
                    patientButton.setText(patientString);

                    // Can't set styles, so have to do it manually :( Deprecated method because min API: 11
                    Style.styleButton(
                            patientButton,
                            "primary",
                            (LinearLayout) findViewById(R.id.patientButtons),
                            getApplicationContext());

                    patientButton.setOnClickListener(new View.OnClickListener() {
                        public void onClick(View v) {
                            AlertDialog.Builder alert = new AlertDialog.Builder(MyPatients.this);
                            alert.setTitle("Patient Options");
                            alert.setItems(R.array.patient_options, new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int which) {
                                    if (which == 0) {
                                        Intent intent = new Intent(getBaseContext(), CarerPrescriptions.class);
                                        intent.putExtra("targetUsername", username);
                                        intent.putExtra("firstName", firstname);
                                        intent.putExtra("surname", surname);
                                        startActivity(intent);
                                    } else if (which == 1) {
                                        Intent intent = new Intent(MyPatients.this, CarerPatientAppointments.class);
                                        intent.putExtra("targetUsername", username);
                                        intent.putExtra("patientFirstName", firstname);
                                        intent.putExtra("patientSurname", surname);
                                        startActivity(intent);
                                    } else if (which == 2) {
                                        Intent intent = new Intent(MyPatients.this, CarerPatientCorrespondence.class);
                                        intent.putExtra("patientUsername", username);
                                        intent.putExtra("patientFirstName", firstname);
                                        intent.putExtra("patientSurname", surname);
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