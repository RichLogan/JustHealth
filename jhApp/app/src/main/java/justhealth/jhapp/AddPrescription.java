package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Context;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.Gravity;
import android.view.View;
import android.view.Menu;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import com.joanzapata.android.iconify.Iconify;

import org.json.JSONArray;
import org.json.JSONException;

import java.util.ArrayList;
import java.util.HashMap;

/*
Provides functionality to add a prescription to a patient's account
 */
public class AddPrescription extends Activity {

    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.carer_add_prescription);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Add Prescription");

        initMedicationSpinner();

        Button submit = (Button) findViewById(R.id.addPrescription);
        submit.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    if (validateForm()) {
                        addPrescription();
                    }
                }
            }
        );
    }

    /**
     * Populates the medication spinner with a list of medications given by the JustHealth server
     */
    private void initMedicationSpinner() {
        //Populate Spinner
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

        Spinner medication = (Spinner) findViewById(R.id.medication);
        medication.setAdapter(new ArrayAdapter<String>(this, android.R.layout.simple_spinner_dropdown_item, populateSpinner));
    }

    /**
     * Handles the input from the addPrescription form, add inserts into the database via the addPrescription API function.
     */
    private void addPrescription() {
        HashMap<String, String> details = new HashMap<String, String>();

        String username = null;
        final Bundle extras = getIntent().getExtras();
        if (extras != null) {
            username = extras.getString("username");
        }

        //Text Boxes
        details.put("username", username);
        details.put("medication", ((Spinner) findViewById(R.id.medication)).getSelectedItem().toString());
        details.put("quantity", ((EditText) findViewById(R.id.quantity)).getText().toString());
        details.put("dosage", ((EditText) findViewById(R.id.dosageValue)).getText().toString());
        details.put("dosageunit", ((EditText) findViewById(R.id.dosageUnit)).getText().toString());
        details.put("frequency", ((EditText) findViewById(R.id.frequency)).getText().toString());
        details.put("dosageform", ((EditText) findViewById(R.id.type)).getText().toString());
        details.put("startdate", ((EditText) findViewById(R.id.startDate)).getText().toString());
        details.put("enddate", ((EditText) findViewById(R.id.endDate)).getText().toString());
        details.put("stockleft", ((EditText) findViewById(R.id.stockLeft)).getText().toString());
        details.put("prerequisite", ((EditText) findViewById(R.id.observations)).getText().toString());

        String response = Request.post("addPrescription", details, getApplicationContext());
        System.out.println(response);
    }

    /**
     * Form to validate all user input on the addPrescription form.
     * @return Boolean to show whether the form successfully validated or not.
     */
    private boolean validateForm() {
        if (((EditText) findViewById(R.id.quantity)).getText().toString().trim().equals("")) {
            Feedback.toast("Please give a quantity", false, getApplicationContext());
            return false;
        }
        return true;
    }
}
