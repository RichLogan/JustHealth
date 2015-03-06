package justhealth.jhapp;

import android.annotation.TargetApi;
import android.app.ActionBar;
import android.app.Activity;
import android.os.Build;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.util.HashMap;

/**
 * Created by Stephen on 06/03/15.
 */
public class CarerAddPatientCorrespondence extends Activity {

    String patientUsername;
    String patientFirstName;
    @TargetApi(Build.VERSION_CODES.HONEYCOMB)
    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.carer_add_correspondence);

        patientUsername = getIntent().getStringExtra("patientUsername");
        patientFirstName = getIntent().getStringExtra("patientFirstName");

        // Set up your ActionBar
        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle(patientFirstName + ": Add Note");

        Button addNote = (Button) findViewById(R.id.submit);
        addNote.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        sendNote();
                    }
                }
        );
    }

    private void sendNote() {

        HashMap<String, String> details = new HashMap<>();
        details.put("carer", this.getSharedPreferences("account", 0).getString("username", null));
        details.put("patient", patientUsername);

        String title = ((EditText) findViewById(R.id.title)).getText().toString();
        String notes = ((EditText) findViewById(R.id.notes)).getText().toString();

        details.put("title", title);
        details.put("notes", notes);

        String response = Request.post("addCorrespondence", details, getApplicationContext());

        if(response.equals("True")) {
            Feedback.toast("Notes added successfully", true, this);
            finish();
        }
        else {
            Feedback.toast("Something went wrong. Please try again", false, this);
        }
    }
}
