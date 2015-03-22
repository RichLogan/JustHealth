package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class Profile extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.profile);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Profile");

        // Load in saved Profile Information
        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        ((TextView) findViewById(R.id.profileUsername)).setText("Username: " + username);
        ((TextView) findViewById(R.id.profileAccount)).setText("Account Type: " + account.getString("accountType", null));

        // Get all Profile Information
        loadProfile(username);
    }

    private String getProfile(String username) {
        HashMap<String, String> profileInfo = new HashMap<String, String>();
        profileInfo.put("username", username);
        return Request.post("getAccountInfo", profileInfo, getApplicationContext());
    }

    private void loadProfile(final String username) {

        new AsyncTask<Void, Void, String>() {
            @Override
            protected String doInBackground(Void... p) {
                return getProfile(username);
            }

            protected void onPostExecute(final String profile) {
                try {
                    JSONObject profileInfo = new JSONObject(profile);

                    //Get TextViews
                    TextView username = (TextView) findViewById(R.id.profileUsername);
                    TextView name = (TextView) findViewById(R.id.profileName);
                    TextView dob = (TextView) findViewById(R.id.profileDOB);
                    TextView gender = (TextView) findViewById(R.id.profileGender);
                    TextView accountType = (TextView) findViewById(R.id.profileAccount);
                    TextView email = (TextView) findViewById(R.id.profileEmail);

                    //Populate TextViews
                    username.setText("Username: " + profileInfo.getString("username"));
                    name.setText("Name: " + profileInfo.getString("firstname") + " " + profileInfo.getString("surname"));
                    dob.setText("Date of Birth: " + profileInfo.getString("dob"));
                    gender.setText("Gender: " + profileInfo.getString("gender"));
                    accountType.setText("Account Type: " + profileInfo.getString("accounttype"));
                    email.setText(profileInfo.getString("email"));

                    // Display Profile Picture
                    String filepath = LoadImage.getProfilePictureURL(profileInfo.getString("profilepicture"));
                    ImageView profilePicture = (ImageView) findViewById(R.id.profilePicture);
                    new LoadImage(profilePicture, false, getApplicationContext()).execute(filepath);

                    //Edit Profile Link
                    Button editProfile = (Button) findViewById(R.id.editProfile);
                    editProfile.setOnClickListener(
                            new Button.OnClickListener() {
                                public void onClick(View view) {
                                    Intent intent = new Intent(getBaseContext(), EditProfile.class);
                                    intent.putExtra("profileInfo", profile);
                                    startActivityForResult(intent, 1);
                                }
                            }
                    );
                } catch (Exception e) {
                    e.printStackTrace();
                    Feedback.toast("Unable to connect to the server", false, getApplicationContext());
                }
            }
        }.execute();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        // If they changed something, reload...
        try {
            if (data.getExtras().containsKey("response")) {
                Boolean success = false;
                if (resultCode == 1) {
                    success = true;
                }
                Feedback.toast(data.getStringExtra("response"), success, getApplicationContext());
                System.out.println(data.getStringExtra("response"));
                finish();
                startActivity(getIntent());
            }
        // They didn't change anything so data is null, no need to reload.
        } catch (NullPointerException e) {}
    }
}