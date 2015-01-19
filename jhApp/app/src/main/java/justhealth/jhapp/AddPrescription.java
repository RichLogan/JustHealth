package justhealth.jhapp;

import android.app.Activity;
import android.content.Context;
import android.graphics.Color;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.Gravity;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;

import java.util.ArrayList;
import java.util.HashMap;

public class AddPrescription extends Activity {

    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.carer_add_prescription);

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
        details.put("frequencyunit", ((EditText) findViewById(R.id.frequencyUnit)).getText().toString());
        details.put("dosageform", ((EditText) findViewById(R.id.type)).getText().toString());
        details.put("startdate", ((EditText) findViewById(R.id.startDate)).getText().toString());
        details.put("enddate", ((EditText) findViewById(R.id.endDate)).getText().toString());
        details.put("stockleft", ((EditText) findViewById(R.id.stockLeft)).getText().toString());
        details.put("prerequisite", ((EditText) findViewById(R.id.observations)).getText().toString());

        final CheckBox repeat = (CheckBox) findViewById(R.id.repeat);
        if (repeat.isChecked()) {
            details.put("repeat", "Yes");
        } else {
            details.put("repeat", "No");
        }

        String response = Request.post("addPrescription", details, getApplicationContext());
        System.out.println(response);
    }

    private boolean validateForm() {
        if (((EditText) findViewById(R.id.quantity)).getText().toString().trim().equals("")) {
            makeToast("Please give a quantity");
            return false;
        }
        return true;
    }

    private void makeToast(String value) {
        Context context = getApplicationContext();
        CharSequence text = value;
        int duration = Toast.LENGTH_LONG;
        Toast toast = Toast.makeText(context, text, duration);
        toast.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL, 0, 100);
        toast.getView().setBackgroundColor(Color.RED);
        toast.show();
    }
}
