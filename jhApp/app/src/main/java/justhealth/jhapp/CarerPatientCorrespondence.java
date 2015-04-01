package justhealth.jhapp;

import android.annotation.TargetApi;
import android.app.ActionBar;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TableRow;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

/**
 * Created by Stephen on 06/03/15.
 */
public class CarerPatientCorrespondence extends Activity  {

    //JSONArray of the notes about a patient
    JSONArray notes;
    //Patients username, first name and surname
    String patientUsername;
    String patientFirstName;
    String patientSurname;

    /**
     * Runs when  the page is first loaded. This sets the correct XML layout for the page and sets
     * the action bar. Runs the method to retrieve the notes from the JustHealth API.
     * @param savedInstanceState a bundle if the state of the application was to be saved.
     */
    @TargetApi(Build.VERSION_CODES.HONEYCOMB)
    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.patient_correspondence);

        patientUsername = getIntent().getStringExtra("patientUsername");
        patientFirstName = getIntent().getStringExtra("patientFirstName");
        patientSurname = getIntent().getStringExtra("patientSurname");

        // Set up your ActionBar
        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle(patientFirstName + "'s Notes");

        //get Notes
        getNotes();

    }

    /**
     * This creates the action bar menu items
     * @param menu The options menu in which you place your items.
     * @return You must return true for the menu to be displayed; if you return false it will not be shown.
     */
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu items for use in the action bar
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.action_bar_carer_correspondence, menu);
        return super.onCreateOptionsMenu(menu);
    }

    /**
     * This method defines the actions when the menu items are pressed
     * @param item The item that has been pressed
     * @return returns true if the action has been executed.
     */
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle presses on the action bar items
        switch (item.getItemId()) {
            case R.id.add:
                Intent intent = new Intent(CarerPatientCorrespondence.this, CarerAddPatientCorrespondence.class);
                intent.putExtra("patientUsername", patientUsername);
                intent.putExtra("patientFirstName", patientFirstName);
                startActivity(intent);
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }

    /**
     * This makes a post request to the JustHealth API to retrieve the notes from the database
     * for a given patient. Also, must pass the carer username to the API as part of the security
     * check.
     */
    private void getNotes() {
        LinearLayout linearLayout = (LinearLayout) findViewById(R.id.correspondenceView);
        linearLayout.removeAllViews();
        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);

        final HashMap<String, String> details = new HashMap<String, String>();

        //Text Boxes
        details.put("carer", username);
        details.put("patient", patientUsername);

        new AsyncTask<Void, Void, JSONArray>() {
            ProgressDialog progressDialog;

            /**
             * This displays the loading dialog to the user.
             */
            @Override
            protected void onPreExecute() {
                progressDialog = ProgressDialog.show(CarerPatientCorrespondence.this, "Loading...", "Loading notes", true);
            }

            /**
             * This makes the post request (off of the main thread) to the JustHealth API to get the notes
             * of a patient.
             * @param params Shows that there are no parameters to the method
             * @return returns a JSONArray of the patient notes
             */
            @Override
            protected JSONArray doInBackground(Void... params) {
                try {
                    String response = Request.post("getCorrespondence", details, getApplicationContext());
                    return new JSONArray(response);
                } catch (Exception e) {
                    return null;
                }
            }

            /**
             * Assigns the notes that are returned from the JustHealth API and assigns them to the
             * class wide variable. Loops through the array and sends each note to the method addToView.
             * Dismisses the spinning dialog (loading)
             * @param response the JSONArray of the patient notes.
             */
            @Override
            protected void onPostExecute(JSONArray response) {
                try {
                    super.onPostExecute(response);

                    notes = response;

                } catch (Exception e) {
                    e.printStackTrace();
                }


                for (int i = 0; i < notes.length(); i++) {
                    try {
                        JSONObject obj = notes.getJSONObject(i);
                        final String title = obj.getString("title");
                        final String date = obj.getString("datetime");
                        final String content = obj.getString("notes");
                        addToView(title, date, content);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
                progressDialog.dismiss();
            }
        }.execute();
    }

    /**
     * Adds each of the notes to the view and styles each part (i.e. the title, date and content)
     * accordingly.
     *
     * @param title the title of the note
     * @param date the date that the note was added
     * @param content the note itself
     */
    private void addToView(String title, String date, String content) {

        TextView textViewTitle = new TextView(this);
        textViewTitle.setLayoutParams(new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT));
        textViewTitle.setText(title);
        textViewTitle.setTextColor(Color.rgb(51, 122, 185));
        textViewTitle.setTextSize(20);
        textViewTitle.setTypeface(null, Typeface.BOLD);

        LinearLayout linearLayout = (LinearLayout) findViewById(R.id.correspondenceView);
        linearLayout.setBackgroundColor(Color.WHITE);
        linearLayout.addView(textViewTitle);


        TextView textViewDate = new TextView(this);
        textViewDate.setLayoutParams(new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT));
        textViewDate.setText(date);
        textViewDate.setTextColor(Color.rgb(128, 128, 128));
        textViewTitle.setTextSize(20);
        textViewDate.setTypeface(null, Typeface.BOLD_ITALIC);

        linearLayout.addView(textViewDate);


        TextView textViewContent = new TextView(this);
        textViewContent.setText(content);
        textViewContent.setTextColor(Color.rgb(128, 128, 128));
        textViewTitle.setTextSize(18);
        textViewContent.setTypeface(null, Typeface.ITALIC);

        linearLayout.addView(textViewContent);

        LinearLayout.LayoutParams llp1 = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        llp1.setMargins(0, 0, 0, 30); // llp.setMargins(left, top, right, bottom);    }
        TextView space1 = new TextView(this);
        space1.setLayoutParams(llp1);
        linearLayout.addView(space1);

        View v = new View(this);
        v.setLayoutParams(new TableRow.LayoutParams(TableRow.LayoutParams.FILL_PARENT, 1));
        v.setBackgroundColor(Color.rgb(51, 51, 51));
        linearLayout.addView(v);

        LinearLayout.LayoutParams llp = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        llp.setMargins(50, 0, 0, 30); // llp.setMargins(left, top, right, bottom);    }
        TextView space = new TextView(this);
        space.setLayoutParams(llp);
        linearLayout.addView(space);
    }
}
