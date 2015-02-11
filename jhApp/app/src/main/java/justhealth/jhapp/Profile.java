package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.ImageView;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.HashMap;

public class Profile extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.profile);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Profile");

        final String profileInfo = getProfile();
        print(profileInfo);

        print(getProfile());

        //Edit Profile Link
        Button editProfile = (Button) findViewById(R.id.editProfile);
        editProfile.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    Intent intent = new Intent(getBaseContext(), EditProfile.class);
                    intent.putExtra("profileInfo", profileInfo);
                    startActivityForResult(intent, 1);
                }
            }
        );
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
            TextView name = (TextView) findViewById(R.id.profileName);
            TextView dob = (TextView) findViewById(R.id.profileDOB);
            TextView gender = (TextView) findViewById(R.id.profileGender);
            TextView accountType = (TextView) findViewById(R.id.profileAccount);
            TextView email = (TextView) findViewById(R.id.profileEmail);

            //Populate TextViews
            username.setText("Username: " + profileInfo.getString("username"));
            name.setText("Name: " + profileInfo.getString("firstname") + " " + profileInfo.getString("surname"));
            dob.setText("D.O.B: " + profileInfo.getString("dob"));
            gender.setText("Gender: " + profileInfo.getString("gender"));
            accountType.setText("Account Type: " + profileInfo.getString("accounttype"));
            email.setText("Email: " + profileInfo.getString("email"));

            // Display Profile Picture
            String filepath = Request.getProfilePictureURL(profileInfo.getString("profilepicture"));
            new DownloadImage((ImageView) findViewById(R.id.profilePicture)).execute(filepath);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        // TODO Auto-generated method stub
        super.onActivityResult(requestCode, resultCode, data);
        if(data.getExtras().containsKey("response")){
            Boolean success = false;
            if (resultCode == 1) { success = true;}
            Feedback.toast(data.getStringExtra("response"), success, getApplicationContext());
            System.out.println(data.getStringExtra("response"));
            finish();
            startActivity(getIntent());
        }
    }

    // Thanks to http://web.archive.org/web/20120802025411/http://developer.aiwgame.com/imageview-show-image-from-url-on-android-4-0.html
    private class DownloadImage extends AsyncTask<String, Void, Bitmap> {
        ImageView iv;

        public DownloadImage(ImageView iv) {
            this.iv = iv;
        }

        protected Bitmap doInBackground(String... urls) {
            URL imageLocation;
            try {
                imageLocation = new URL(urls[0]);

                // Adding Authentication
                SharedPreferences account = getSharedPreferences("account", 0);
                String username = account.getString("username", null);
                String password = account.getString("password", null);
                String authentication = username + ":" + password;
                String encodedAuthentication = Base64.encodeToString(authentication.getBytes(), Base64.NO_WRAP);

                // Connect
                URLConnection loader = imageLocation.openConnection();
                loader.setRequestProperty("Authorization", "Basic " + encodedAuthentication);

                // Return Content
                InputStream content = loader.getInputStream();
                return BitmapFactory.decodeStream(content);
            } catch (Exception e) {
                e.printStackTrace();
                return null;
            }
        }

        protected void onPostExecute(Bitmap result) {
            iv.setImageBitmap(result);
        }
    }
}