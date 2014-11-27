package justhealth.jhapp;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.StrictMode;
import android.support.v7.app.ActionBarActivity;
import android.util.Base64;
import android.view.View;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Created by Ben McGregor on 21/11/2014.
 */
public class Profile extends ActionBarActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.profile);
        viewProfile();

    }

    private void viewProfile() {
        HashMap<String, String> profileInfo = new HashMap<String, String>();
        //retrieve username
        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username",null);
        String password = account.getString("password", null);

        //add username to HashMap
        profileInfo.put("username", username);

        //Create new HttpClient and Post Header
        HttpClient httpclient = new DefaultHttpClient();
        String authentication = username + ":" + password;
        String encodedAuthentication = Base64.encodeToString(authentication.getBytes(), Base64.NO_WRAP);

        HttpPost httppost = new HttpPost("http://raptor.kent.ac.uk:5000/api/getAccountInfo");
        httppost.setHeader("Authorization", "Basic " + encodedAuthentication);

        //assigns the HashMap to list, for post request encoding
        try {
            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);

            Set<Map.Entry<String, String>> detailsSet = profileInfo.entrySet();
            for (Map.Entry<String, String> string : detailsSet) {
                nameValuePairs.add(new BasicNameValuePair(string.getKey(), string.getValue()));
            }

            //pass the list to the post request
            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
            HttpResponse response = httpclient.execute(httppost);
            String responseString = EntityUtils.toString(response.getEntity());
            System.out.println(responseString);
            JSONObject queryReturn = null;
            try {
                queryReturn = new JSONObject(responseString);
            } catch (JSONException e) {
                e.printStackTrace();
            }

            print(queryReturn);

        } catch (ClientProtocolException e) {
            //TODO Auto-generated catch block
        } catch (IOException e) {
            //TODO Auto-generated catch block
        }

    }

    private void print(JSONObject response) {
        TextView username = (TextView) findViewById(R.id.profileUsername);
        TextView firstName = (TextView) findViewById(R.id.profileFirstName);
        TextView surname = (TextView) findViewById(R.id.profileSurname);
        TextView dob = (TextView) findViewById(R.id.profileDOB);
        TextView gender = (TextView) findViewById(R.id.profileGender);
        TextView accountType = (TextView) findViewById(R.id.profileAccount);
        TextView email = (TextView) findViewById(R.id.profileEmail);
        try {
            username.setText(response.getString("username"));
            firstName.setText(response.getString("firstname"));
            surname.setText(response.getString("surname"));
            dob.setText(response.getString("dob"));
            gender.setText(response.getString("gender"));
            accountType.setText(response.getString("accounttype"));
            email.setText(response.getString("email"));
            //assign object to view
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}

