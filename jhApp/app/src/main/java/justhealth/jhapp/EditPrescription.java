package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
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

public class EditPrescription extends Activity {

    String prescriptionid;
    String targetUsername;

    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.carer_edit_prescription);

        final Bundle extras = getIntent().getExtras();
        if (extras != null) {
            prescriptionid = extras.getString("prescriptionid");
            targetUsername = extras.getString("targetUsername");
        }

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle(targetUsername + "'s Prescriptions");

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
            System.out.println(e.getStackTrace());
        }

        Spinner medication = (Spinner)findViewById(R.id.medication);
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_dropdown_item, populateSpinner);
        medication.setAdapter(adapter);

        if (!target.equals(null)) {
            int position = adapter.getPosition(target);
            medication.setSelection(position);
        }
    }

    private JSONArray displayPrescription() {
        HashMap<String, String> parameters = new HashMap<String, String>();
        parameters.put("prescriptionid", prescriptionid);
        String response = Request.post("getPrescription", parameters, getApplicationContext());
        try {
            JSONObject prescription = new JSONObject(response);

            populateSpinner(prescription.getString("medication"));
            ((EditText)findViewById(R.id.quantity)).setText(prescription.getString("quantity"), TextView.BufferType.EDITABLE);
            ((EditText)findViewById(R.id.dosageValue)).setText(prescription.getString("dosage"), TextView.BufferType.EDITABLE);
            ((EditText)findViewById(R.id.dosageUnit)).setText(prescription.getString("dosageunit"), TextView.BufferType.EDITABLE);
            ((EditText)findViewById(R.id.frequency)).setText(prescription.getString("frequency"), TextView.BufferType.EDITABLE);
            ((EditText)findViewById(R.id.frequencyUnit)).setText(prescription.getString("frequencyunit"), TextView.BufferType.EDITABLE);
            ((EditText)findViewById(R.id.type)).setText(prescription.getString("dosageform"), TextView.BufferType.EDITABLE);
            ((EditText)findViewById(R.id.startDate)).setText(prescription.getString("startdate"), TextView.BufferType.EDITABLE);
            ((EditText)findViewById(R.id.endDate)).setText(prescription.getString("enddate"), TextView.BufferType.EDITABLE);
            ((EditText)findViewById(R.id.stockLeft)).setText(prescription.getString("stockleft"), TextView.BufferType.EDITABLE);
            ((EditText)findViewById(R.id.observations)).setText(prescription.getString("prerequisite"), TextView.BufferType.EDITABLE);

            if (prescription.getString("repeat").equals("Yes")) {
                ((CheckBox) findViewById(R.id.repeat)).setChecked(true);
            }
            else {
                ((CheckBox) findViewById(R.id.repeat)).setChecked(true);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
        return null;
    }

    private void editPrescription() {

        HashMap<String, String> parameters = new HashMap<String, String>();

        parameters.put("username", targetUsername);
        parameters.put("prescriptionid", prescriptionid);
        parameters.put("medication", ((Spinner)findViewById(R.id.medication)).getSelectedItem().toString());
        parameters.put("quantity", ((EditText)findViewById(R.id.quantity)).getText().toString());
        parameters.put("dosage", ((EditText)findViewById(R.id.dosageValue)).getText().toString());
        parameters.put("dosageunit", ((EditText)findViewById(R.id.dosageUnit)).getText().toString());
        parameters.put("frequency", ((EditText)findViewById(R.id.frequency)).getText().toString());
        parameters.put("frequencyunit", ((EditText)findViewById(R.id.frequencyUnit)).getText().toString());
        parameters.put("dosageform", ((EditText) findViewById(R.id.type)).getText().toString());
        parameters.put("startdate", ((EditText)findViewById(R.id.startDate)).getText().toString());
        parameters.put("enddate", ((EditText)findViewById(R.id.endDate)).getText().toString());
        parameters.put("stockleft", ((EditText) findViewById(R.id.stockLeft)).getText().toString());
        parameters.put("prerequisite", ((EditText)findViewById(R.id.observations)).getText().toString());
        if (((CheckBox) findViewById(R.id.repeat)).isChecked()) {
            parameters.put("repeat", "Yes");
        }
        else {
            parameters.put("repeat", "No");
        }

        //Post
        String response = Request.post("editPrescription", parameters, getApplicationContext());

        //Back to view all with response
        Intent i = getIntent();
        i.putExtra("response", response);
        if (!response.equals("Failed")) {
            setResult(1, i);
        } else {
            setResult(0, i);
        }
        finish();
    }
}
