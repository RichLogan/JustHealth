package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.CheckBox;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.text.DateFormatSymbols;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Locale;

public class TakePrescription extends Activity {

    JSONObject prescription;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.take_prescription);

        // Get Prescription
        try {
            prescription = new JSONObject(getIntent().getStringExtra("prescription"));
            final ActionBar actionBar = getActionBar();
            actionBar.setDisplayShowHomeEnabled(true);
            actionBar.setTitle(
                    prescription.getString("medication")
                            + " "
                            + prescription.getString("quantity")
                            + " x "
                            + prescription.getString("dosage")
                            + prescription.getString("dosageunit")
            );

            // Days of the Week
            ((CheckBox) findViewById(R.id.monday)).setChecked(prescription.getBoolean("Monday"));
            ((CheckBox) findViewById(R.id.tuesday)).setChecked(prescription.getBoolean("Tuesday"));
            ((CheckBox) findViewById(R.id.wednesday)).setChecked(prescription.getBoolean("Wednesday"));
            ((CheckBox) findViewById(R.id.thursday)).setChecked(prescription.getBoolean("Thursday"));
            ((CheckBox) findViewById(R.id.friday)).setChecked(prescription.getBoolean("Friday"));
            ((CheckBox) findViewById(R.id.saturday)).setChecked(prescription.getBoolean("Saturday"));
            ((CheckBox) findViewById(R.id.sunday)).setChecked(prescription.getBoolean("Sunday"));

            // Are you due to take today?
            String weekdays[] = new DateFormatSymbols(Locale.UK).getWeekdays();
            int day = Calendar.getInstance().get(Calendar.DAY_OF_WEEK);
            String today = weekdays[day];
            if (prescription.getBoolean(today)) {
                // Should be taking prescription today

                HashMap<String, String> params = new HashMap<String, String>();
                params.put("prescriptionid", prescription.getString("prescriptionid"));
                int preCheckedCount = Integer.parseInt(Request.post("getPrescriptionCount", params, this));

                // Alter Text
                TextView info = ((TextView) findViewById(R.id.takePrescriptionInfo));
                info.setText(
                        "You are due to take this prescription "
                                + prescription.getString("frequency") + " times today. \n"
                                + "Each dose consists of " + prescription.getString("quantity") + " x "
                                + prescription.getString("dosage") + prescription.getString("dosageunit") + " "
                                + prescription.getString("dosageform") + "(s).\n\n"
                                + "Please record the taking of each dose below:"
                );
                info.setTextColor(getResources().getColor(R.color.success));

                // Print Checkboxes
                LinearLayout checkboxContainer = (LinearLayout) findViewById(R.id.takeCheckboxes);
                for (int x = 0; x < prescription.getInt("frequency"); x++) {
                    LinearLayout holder = new LinearLayout(this);
                    holder.setOrientation(LinearLayout.VERTICAL);

                    // Create Checkbox
                    CheckBox c = new CheckBox(this);
                    c.setGravity(Gravity.CENTER);
                    c.setGravity(Gravity.CENTER);
                    c.setId(x);
                    // Should this box be checked?
                    if (x < preCheckedCount) {
                        c.setChecked(true);
                    }
                    // Record dosage functionality
                    c.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View v) {
                            // Requests off main thread, no result
                            new AsyncTask<Void, Void, Void>() {
                                @Override
                                protected Void doInBackground(Void... v) {
                                    // Track number of boxes ticked
                                    int checkCount = 0;
                                    try {
                                        for (int x = 0; x < prescription.getInt("frequency"); x++) {
                                            if (((CheckBox) findViewById(x)).isChecked()) {
                                                checkCount++;
                                            }
                                        }
                                        // Send number and prescriptionid
                                        HashMap<String, String> pres = new HashMap<String, String>();
                                        pres.put("prescriptionid", prescription.getString("prescriptionid"));
                                        pres.put("currentcount", Integer.toString(checkCount));
                                        Request.post("takeprescription", pres, getApplicationContext());
                                    } catch (JSONException e) {
                                        Feedback.toast("Could not load details", false, getApplicationContext());
                                    }
                                    return null;
                                }
                            }.execute();
                        }
                    });

                    // Display dose number
                    TextView number = new TextView(this);
                    number.setText(Integer.toString(x + 1));
                    number.setGravity(Gravity.CENTER);

                    // Add to page
                    holder.addView(c);
                    holder.addView(number);
                    checkboxContainer.addView(holder);
                }
            }
        } catch (JSONException e) {
            Feedback.toast("Could not load prescription", false, this);
        }
    }
}
