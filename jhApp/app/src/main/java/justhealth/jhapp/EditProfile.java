package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.IconTextView;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Spinner;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class EditProfile extends Activity {

    //TODO: Date Picker

    /**
     * Sets the correct xml layout for the page and loads the action bar.
     * Sets an onClickListener on the update button and runs the method to load the existing
     * profile information.
     *
     * @param savedInstanceState a bundle if the state of the application was to be saved.
     */
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.edit_profile);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Profile");

        // Set update button
        Button update = (Button) findViewById(R.id.editProfileButton);
        update.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    AlertDialog.Builder alert = new AlertDialog.Builder(EditProfile.this);
                    alert.setTitle("Confirm Update");
                    alert.setMessage("Are you sure you want to update your details?");
                    alert.setNegativeButton("Cancel", null);
                    alert.setPositiveButton("Update", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int whichButton) {
                            editProfile();
                        }
                    });
                    alert.show();
                }
            }
        );

        // Load existing profile information
        loadProfile();
    }

    /**
     * Method not in use, was used to control the male/female spinner but figured that the user
     * will not be able to update this.
     */
    private void initSpinners() {
        // Gender Spinner
        final Spinner genderSpinner = (Spinner) findViewById(R.id.editGender);
        genderSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> arg0, View arg1, int arg2, long arg3) {
                String selected = genderSpinner.getSelectedItem().toString();
                IconTextView genderIcon = (IconTextView) findViewById(R.id.genderIcon);
                if (selected.equals("Male")) {
                    genderIcon.setText("{fa-male}");

                } else if (selected.equals("Female")) {
                    genderIcon.setText("{fa-female}");
                }
            }

            @Override
            public void onNothingSelected(AdapterView<?> arg0) {
                // TODO Auto-generated method stub
            }
        });
    }

    /**
     * Loads the existing profile information that was passed with the intent. Assigns the
     * information to TextViews on the page.
     */
    private void loadProfile() {
        final Bundle extras = getIntent().getExtras();
        if (extras != null) {
            try {
                // Get Existing ProfileInfo
                JSONObject profileInfo = new JSONObject(extras.getString("profileInfo"));

                // Populate TextViews
                ((TextView) findViewById(R.id.editFirstname)).setText(profileInfo.getString("firstname"));
                ((TextView) findViewById(R.id.editSurname)).setText(profileInfo.getString("surname"));
                ((TextView) findViewById(R.id.editDOB)).setText(profileInfo.getString("dob"));
                ((TextView) findViewById(R.id.editEmail)).setText(profileInfo.getString("email"));

                // Populate Gender Radio Button
                Spinner spinner = (Spinner) findViewById(R.id.editGender);
                if (profileInfo.getString("gender").equals("Male")) {
                    spinner.setSelection(0);
                }
                else {
                    spinner.setSelection(1);
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }

    /**
     * Executed when the profile is edited. Gets the inputs from the EditTexts and makes a post
     * request to the JustHealth API. Feedback the result to the user and return to the previous
     * page.
     */
    private void editProfile() {
        HashMap<String, String> parameters = new HashMap<String, String>();

        // Get current User
        parameters.put("username", getSharedPreferences("account", 0).getString("username", null));

        // Get values of TextViews
        parameters.put("firstname", ((EditText)findViewById(R.id.editFirstname)).getText().toString());
        parameters.put("surname", ((EditText)findViewById(R.id.editSurname)).getText().toString());
        parameters.put("dob", ((EditText)findViewById(R.id.editDOB)).getText().toString());
        parameters.put("email", ((EditText)findViewById(R.id.editEmail)).getText().toString());

        //Gender
        String ismale = "false";
        Spinner gender = (Spinner)findViewById(R.id.editGender);
        String genderValue = gender.getSelectedItem().toString();
        if (genderValue.equals("Male")) {
            ismale = "true";
        }
        parameters.put("ismale", ismale);

        String response = Request.post("editProfile", parameters, getApplicationContext());

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
