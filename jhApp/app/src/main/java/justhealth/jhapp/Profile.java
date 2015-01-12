package justhealth.jhapp;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class Profile extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.profile);
        print(getProfile());
    }

    private String getProfile() {
        SharedPreferences account = getSharedPreferences("account", 0);
        String currentUser = account.getString("username", null);

        HashMap<String, String> profileInfo = new HashMap<String, String>();
        profileInfo.put("username", currentUser);

        return Request.post("getAccountInfo", profileInfo, getApplicationContext());
    }

    private void print(String profile) {

        try {
            JSONObject profileInfo = new JSONObject(profile);

            //Get TextViews
            TextView username = (TextView) findViewById(R.id.profileUsername);
            TextView firstName = (TextView) findViewById(R.id.profileFirstName);
            TextView surname = (TextView) findViewById(R.id.profileSurname);
            TextView dob = (TextView) findViewById(R.id.profileDOB);
            TextView gender = (TextView) findViewById(R.id.profileGender);
            TextView accountType = (TextView) findViewById(R.id.profileAccount);
            TextView email = (TextView) findViewById(R.id.profileEmail);

            //Populate TextViews
            username.setText(profileInfo.getString("username"));
            firstName.setText(profileInfo.getString("firstname"));
            surname.setText(profileInfo.getString("surname"));
            dob.setText(profileInfo.getString("dob"));
            gender.setText(profileInfo.getString("gender"));
            accountType.setText(profileInfo.getString("accounttype"));
            email.setText(profileInfo.getString("email"));
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}