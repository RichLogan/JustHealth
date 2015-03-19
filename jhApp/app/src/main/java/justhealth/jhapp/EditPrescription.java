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
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.zip.CheckedOutputStream;

public class EditPrescription extends Activity {

    JSONObject prescription;

    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.carer_edit_prescription);

        try {
            final Bundle extras = getIntent().getExtras();
            if (extras != null) {
                prescription = new JSONObject(extras.getString("prescription"));
            }

            final ActionBar actionBar = getActionBar();
            actionBar.setDisplayShowHomeEnabled(true);
            actionBar.setTitle(prescription.getString("username") + "'s Prescriptions");

            displayPrescription();

            //OnClick of Edit
            Button update = (Button) findViewById(R.id.updatePrescription);
            update.setOnClickListener(
                    new Button.OnClickListener() {
                        public void onClick(View view) {
                            AlertDialog.Builder alert = new AlertDialog.Builder(EditPrescription.this);
                            alert.setTitle("Confirm Update");
                            alert.setMessage("Are you sure you want to update this prescription?");
                            alert.setNegativeButton("Cancel", null);
                            alert.setPositiveButton("Update", new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int whichButton) {
                                    editPrescription();
                                }
                            });
                            alert.show();
                        }
                    }
            );
        } catch (JSONException e) {
            exit(false, "Prescription is malformed, please try again");
        }
    }

    private void populateSpinner(String target) {
        ArrayList<String> populateSpinner = new ArrayList<String>();
        String getMedications = Request.get("getMedications", getApplicationContext());

        try {
            JSONArray medications = new JSONArray(getMedications);
            for (int i = 0; i < medications.length(); i++) {
                String app = medications.getString(i);
                populateSpinner.add(app);
            }
        } catch (JSONException e) {
            exit(false, "Prescription is malformed, please try again");
        }

        Spinner medication = (Spinner) findViewById(R.id.medication);
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_dropdown_item, populateSpinner);
        medication.setAdapter(adapter);

        if (!target.equals(null)) {
            int position = adapter.getPosition(target);
            medication.setSelection(position);
        }
    }

    private void displayPrescription() {
        try {
            populateSpinner(prescription.getString("medication"));
            ((EditText) findViewById(R.id.quantity)).setText(prescription.getString("quantity"), TextView.BufferType.EDITABLE);
            ((EditText) findViewById(R.id.dosageValue)).setText(prescription.getString("dosage"), TextView.BufferType.EDITABLE);
            ((EditText) findViewById(R.id.dosageUnit)).setText(prescription.getString("dosageunit"), TextView.BufferType.EDITABLE);
            ((EditText) findViewById(R.id.frequency)).setText(prescription.getString("frequency"), TextView.BufferType.EDITABLE);
            ((EditText) findViewById(R.id.type)).setText(prescription.getString("dosageform"), TextView.BufferType.EDITABLE);
            ((EditText) findViewById(R.id.startDate)).setText(prescription.getString("startdate"), TextView.BufferType.EDITABLE);
            ((EditText) findViewById(R.id.endDate)).setText(prescription.getString("enddate"), TextView.BufferType.EDITABLE);
            ((EditText) findViewById(R.id.stockLeft)).setText(prescription.getString("stockleft"), TextView.BufferType.EDITABLE);
            ((EditText) findViewById(R.id.observations)).setText(prescription.getString("prerequisite"), TextView.BufferType.EDITABLE);
            ((CheckBox) findViewById(R.id.monday)).setChecked(prescription.getBoolean("Monday"));
            ((CheckBox) findViewById(R.id.tuesday)).setChecked(prescription.getBoolean("Tuesday"));
            ((CheckBox) findViewById(R.id.wednesday)).setChecked(prescription.getBoolean("Wednesday"));
            ((CheckBox) findViewById(R.id.thursday)).setChecked(prescription.getBoolean("Thursday"));
            ((CheckBox) findViewById(R.id.friday)).setChecked(prescription.getBoolean("Friday"));
            ((CheckBox) findViewById(R.id.saturday)).setChecked(prescription.getBoolean("Saturday"));
            ((CheckBox) findViewById(R.id.sunday)).setChecked(prescription.getBoolean("Sunday"));
        } catch (JSONException e) {
            exit(false, "Prescription is malformed, please try again");
        }
    }

    private void editPrescription() {
        final HashMap<String, String> parameters = new HashMap<String, String>();

        try {
            parameters.put("username", prescription.getString("username"));
            parameters.put("prescriptionid", prescription.getString("prescriptionid"));
        } catch (JSONException e) {
            exit(false, "Prescription is malformed, please try again");
        }

        parameters.put("medication", ((Spinner) findViewById(R.id.medication)).getSelectedItem().toString());
        parameters.put("quantity", ((EditText) findViewById(R.id.quantity)).getText().toString());
        parameters.put("dosage", ((EditText) findViewById(R.id.dosageValue)).getText().toString());
        parameters.put("dosageunit", ((EditText) findViewById(R.id.dosageUnit)).getText().toString());
        parameters.put("frequency", ((EditText) findViewById(R.id.frequency)).getText().toString());
        parameters.put("dosageform", ((EditText) findViewById(R.id.type)).getText().toString());
        parameters.put("startdate", ((EditText) findViewById(R.id.startDate)).getText().toString());
        parameters.put("enddate", ((EditText) findViewById(R.id.endDate)).getText().toString());
        parameters.put("stockleft", ((EditText) findViewById(R.id.stockLeft)).getText().toString());
        parameters.put("prerequisite", ((EditText) findViewById(R.id.observations)).getText().toString());
        parameters.put("Monday", String.valueOf(((CheckBox) findViewById(R.id.monday)).isChecked()));
        parameters.put("Tuesday", String.valueOf(((CheckBox) findViewById(R.id.tuesday)).isChecked()));
        parameters.put("Wednesday", String.valueOf(((CheckBox) findViewById(R.id.wednesday)).isChecked()));
        parameters.put("Thursday", String.valueOf(((CheckBox) findViewById(R.id.thursday)).isChecked()));
        parameters.put("Friday", String.valueOf(((CheckBox) findViewById(R.id.friday)).isChecked()));
        parameters.put("Saturday", String.valueOf(((CheckBox) findViewById(R.id.saturday)).isChecked()));
        parameters.put("Sunday", String.valueOf(((CheckBox) findViewById(R.id.sunday)).isChecked()));

        System.out.print(parameters);

        new AsyncTask<Void, Void, String>() {
            ProgressDialog progressDialog;

            @Override
            protected void onPreExecute() {
                progressDialog = ProgressDialog.show(
                    EditPrescription.this,
                    "Loading...",
                    "Updating " + parameters.get("medication") + " (" + parameters.get("quantity") + " x " + parameters.get("dosage") + parameters.get("dosageunit") + ")",
                    true);
            }

            @Override
            protected String doInBackground(Void... params) {
                String r = Request.post("editPrescription", parameters, getApplicationContext());
                System.out.println(r);
                return r;
            }

            @Override
            protected void onPostExecute(String result) {
                super.onPostExecute(result);
                progressDialog.dismiss();
                if (result.equals("Failed")) {
                    exit(false, "Failed to update prescription");
                } else {
                    exit(true, result);
                }
            }
        }.execute();
    }

    private void exit(Boolean success, String response) {
        Intent i = getIntent();
        i.putExtra("response", response);
        if (success) {
            setResult(1, i);
        } else {
            setResult(0, i);
        }
        finish();
    }
}
