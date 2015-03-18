package justhealth.jhapp;

import android.app.Activity;
import android.app.ActionBar;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.os.AsyncTask;
import android.os.Bundle;
//import android.support.v7.app.ActionBarActivity;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MenuInflater;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ProgressBar;

import com.joanzapata.android.iconify.IconDrawable;
import com.joanzapata.android.iconify.Iconify;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

/**
 * Functionality to allow a carer to view all Prescriptions for any patient that they are connected to.
 */
public class CarerPrescriptions extends Activity{

    private String username;
    private String firstname;
    private int loadCounter = 3;
    private ProgressDialog loading;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.carer_prescriptions);

        //Get data passed from MyPatients
        final Bundle extras = getIntent().getExtras();
        if (extras != null) {
            username = extras.getString("targetUsername");
            firstname = extras.getString("firstName");
        }

        final String user = username;

        // Action Bar
        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle(firstname + "'s Prescriptions");
        actionBar.setDisplayShowCustomEnabled(true);
        actionBar.setCustomView(R.layout.action_bar_carer_prescriptions);

        final Button addPrescription = (Button) findViewById(R.id.addPrescriptionActionBar);
        addPrescription.setText("{fa-plus}");
        addPrescription.setTextSize(TypedValue.COMPLEX_UNIT_SP, 20);
        Iconify.addIcons(addPrescription);
        addPrescription.setOnClickListener(new Button.OnClickListener() {
            public void onClick(View view) {
                Intent add = new Intent(CarerPrescriptions.this, AddPrescription.class);
                add.putExtra("username", user);
                startActivityForResult(add, 1);
            }
        });

        loadPrescriptions();
    }

    private void loadPrescriptions() {
        final HashMap<String, String> parameters = new HashMap<String, String>();
        parameters.put("username", username);
        loading = ProgressDialog.show(CarerPrescriptions.this, "Loading...", "Loading " + firstname + "'s prescriptions", true);
        loadUpcomingPrescriptions(parameters);
        loadActivePrescriptions(parameters);
        loadExpiredPrescriptions(parameters);
    }

    private void loadActivePrescriptions(final HashMap<String, String> parameters) {
        new AsyncTask<Void, Void, String>() {
            @Override
            protected String doInBackground(Void... params) {
                return Request.post("getActivePrescriptions", parameters, getApplicationContext());
            }

            @Override
            protected void onPostExecute(String result) {
                super.onPostExecute(result);
                try {
                    displayPrescriptions(new JSONArray(result), "active");
                } catch (JSONException e) {System.out.println("Failed");}
                loadCounter--;
                if (loadCounter <= 0) {
                    loading.dismiss();
                }
            }
        }.execute();
    }

    private void loadUpcomingPrescriptions(final HashMap<String, String> parameters) {
        new AsyncTask<Void, Void, String>() {
            @Override
            protected String doInBackground(Void... params) {
                return Request.post("getUpcomingPrescriptions", parameters, getApplicationContext());
            }

            @Override
            protected void onPostExecute(String result) {
                super.onPostExecute(result);
                try {
                    displayPrescriptions(new JSONArray(result), "upcoming");
                } catch (JSONException e) {System.out.println("Failed");}
                loadCounter--;
                if (loadCounter <= 0) {
                    loading.dismiss();
                }
            }
        }.execute();
    }

    private void loadExpiredPrescriptions(final HashMap<String, String> parameters) {
        new AsyncTask<Void, Void, String>() {
            @Override
            protected String doInBackground(Void... params) {
                return Request.post("getExpiredPrescriptions", parameters, getApplicationContext());
            }

            @Override
            protected void onPostExecute(String result) {
                super.onPostExecute(result);
                try {
                    displayPrescriptions(new JSONArray(result), "expired");
                } catch (JSONException e) {System.out.println("Failed");}
                loadCounter--;
                if (loadCounter <= 0) {
                    loading.dismiss();
                }
            }
        }.execute();
    }

    /**
     * Builds a list of buttons that provide basic details about each prescription. These can be clicked for more a more in-depth description.
     * @param prescriptionList The retrieved JSONArray of prescriptions from getPrescriptions()
     * @param type The type of prescription you are looking at. One of 'active', 'upcoming', 'expired'
     */
    private void displayPrescriptions(JSONArray prescriptionList, String type) {
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
                final String startdate = prescription.getString("startdate");
                final String enddate = prescription.getString("enddate");
                final String stockleft = prescription.getString("stockleft");
                final String prerequisite = prescription.getString("prerequisite");
                final String dosageform = prescription.getString("dosageform");

                //Create a button
                Button prescriptionButton = new Button(this);
                String prescriptionString = medication + ":\n" + "Take " + quantity + " x " + dosage + " " + dosageunit + " " + dosageform + "(s)\n" + frequency + " times " + "a day";
                prescriptionButton.setText(prescriptionString);

                //Add button to view
                int layout = R.id.prescriptionButtons;
                if (type.equals("active")) {
                    layout = R.id.activePrescriptionButtons;
                }
                else if (type.equals("upcoming")) {
                    layout = R.id.upcomingPrescriptionButtons;
                }
                else if (type.equals("expired")) {
                    layout = R.id.expiredPrescriptionButtons;
                }

                Style.styleButton(prescriptionButton, "primary", (LinearLayout)findViewById(layout), getApplicationContext());

                prescriptionButton.setOnClickListener(new View.OnClickListener() {
                    public void onClick(View v) {
                        AlertDialog.Builder alert = new AlertDialog.Builder(CarerPrescriptions.this);
                        alert.setTitle(medication + " (" + dosage + dosageunit + ")");
                        alert.setMessage("Start Date: " + startdate + "\nEnd Date: " + enddate + "\nExtra Info: " + prerequisite);
                        alert.setNegativeButton("Edit", new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int whichButton) {
                                Intent intent = new Intent(getBaseContext(), EditPrescription.class);
                                intent.putExtra("prescription", prescription.toString());
                                startActivityForResult(intent, 1);
                            }
                        });
                        alert.setNeutralButton("Delete", new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int whichButton) {
                                AlertDialog.Builder confirmDelete = new AlertDialog.Builder(CarerPrescriptions.this);
                                confirmDelete.setTitle(medication + " (" + dosage + dosageunit + ")");
                                confirmDelete.setMessage("Are you sure you want to delete this prescription?");
                                confirmDelete.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                                    public void onClick(DialogInterface dialog, int whichButton) {
                                        deletePrescription(prescriptionid);
                                    }
                                });
                                confirmDelete.setNegativeButton("No", null);
                                confirmDelete.show();
                            }
                        });
                        alert.setPositiveButton("Got It!", null);
                        alert.show();
                    }
                });
            }
            catch (JSONException e) {
                System.out.print(e.getStackTrace());
            }
        }
    }

    /**
     * Informs the calling activity whether the action was successful for not.
     * @param requestCode Internally used, autopopulated
     * @param resultCode 1 for success, 0 for failure
     * @param data Internally used, autopopulated
     */
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        try {
            if (data.getExtras().containsKey("response")) {
                Boolean success = (resultCode == 1);
                finish();
                startActivity(getIntent());
                Feedback.toast(data.getStringExtra("response"), success, getApplicationContext());
            }
        // Allows a user to exit without doing anything
        } catch (NullPointerException e) {}
    }

    /**
     * Functionality to delete a specific prescription from the database
     * @param prescriptionid The id of the prescription to delete
     */
    private void deletePrescription(String prescriptionid) {
        HashMap<String, String> parameters = new HashMap<String, String>();
        parameters.put("prescriptionid", prescriptionid);
        String response = Request.post("deletePrescription", parameters, getApplicationContext());
        if (response.equals("Deleted")) {
            Feedback.toast("Prescription Deleted", true, getApplicationContext());
        }
        else {
            Feedback.toast("Deletion failed, please try again.", false, getApplicationContext());
        }
        finish();
        startActivity(getIntent());
    }
}