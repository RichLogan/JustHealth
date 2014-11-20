package justhealth.jhapp;

import android.annotation.TargetApi;
import android.app.ActionBar;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.os.StrictMode;
import android.util.Base64;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TableLayout;
import android.widget.TableRow;
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
import java.io.UnsupportedEncodingException;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Created by Stephen Tate on 14/11/2014.
 */
public class Search extends ActionBarActivity {

    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.search);

        //check for the search button being pressed
        Button search = (Button) findViewById(R.id.searchButton);
        search.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        System.out.println("onclick");
                        searchName();
                    }
                }
        );

    }

    private void searchName() {
        HashMap<String, String> searchInformation = new HashMap<String, String>();

        //this is adding the username as null - INCORRECT
        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        String password = account.getString("password", null);
        //todo remove this line
        System.out.println(username);

        //add search to HashMap
        searchInformation.put("username", username);
        searchInformation.put("searchTerm", ((EditText) findViewById(R.id.searchField)).getText().toString());

        //Create new HttpClient and Post Header
        HttpClient httpclient = new DefaultHttpClient();
        String authentication = username + ":" + password;
        String encodedAuthentication = Base64.encodeToString(authentication.getBytes(), Base64.NO_WRAP);

        HttpPost httppost = new HttpPost("http://raptor.kent.ac.uk:5000/api/searchPatientCarer");
        httppost.setHeader("Authorization", "Basic " + encodedAuthentication);
        System.out.println(encodedAuthentication);
        //assigns the HashMap to list, for post request encoding
        try {
            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);

            Set<Map.Entry<String, String>> detailsSet = searchInformation.entrySet();
            for (Map.Entry<String, String> string : detailsSet) {
                nameValuePairs.add(new BasicNameValuePair(string.getKey(), string.getValue()));
            }

            //pass the list to the post request
            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
            HttpResponse response = httpclient.execute(httppost);

            String responseString = EntityUtils.toString(response.getEntity());
            System.out.print(responseString);
            JSONArray queryReturn = null;
            try {
                queryReturn = new JSONArray(responseString);
            } catch (JSONException e) {
                e.printStackTrace();
            }

            System.out.print(queryReturn);
            printTable(queryReturn);

        } catch (ClientProtocolException e) {
            //TODO Auto-generated catch block
        } catch (IOException e) {
            //TODO Auto-generated catch block
        } catch (NullPointerException e) {
            //TODO Auto-generated catch block
        }
    }

    private void printTable(JSONArray array) {
        TableLayout searchTable = (TableLayout) findViewById(R.id.searchTable);
        searchTable.removeAllViews();
        //create heading row
        TableRow head = new TableRow(this);
        //add properties to the header row
        head.setBackgroundColor(getResources().getColor(R.color.header));

        //create the headings of the table
        TextView headingUsername = new TextView(this);
        headingUsername.setTextColor(Color.WHITE);
        headingUsername.setPadding(5, 5, 5, 5);

        TextView headingFirstName = new TextView(this);
        headingFirstName.setTextColor(Color.WHITE);
        headingFirstName.setPadding(5, 5, 5, 5);

        TextView headingSurname = new TextView(this);
        headingSurname.setTextColor(Color.WHITE);
        headingSurname.setPadding(5, 5, 5, 5);

        TextView headingAction = new TextView(this);
        headingAction.setTextColor(Color.WHITE);
        headingAction.setPadding(5, 5, 5, 5);

        headingUsername.setText("Username");
        headingFirstName.setText("First Name");
        headingSurname.setText("Surname");
        headingAction.setText("Action");

        //add the headings to the row
        head.addView(headingUsername);
        head.addView(headingFirstName);
        head.addView(headingSurname);
        head.addView(headingAction);
        searchTable.addView(head, 0);


        for (int i = 0; i < array.length(); i++) {
            try {
                JSONObject obj = array.getJSONObject(i);
                System.out.println(obj);
                final String resultUsername = obj.getString("username");
                String resultFirstName = obj.getString("firstname");
                String resultSurname = obj.getString("surname");


                TableRow row = new TableRow(this);
                //add username to TextView
                TextView forUsername = new TextView(this);
                forUsername.setText(resultUsername);
                //add first name to TextView
                TextView forFirstName = new TextView(this);
                forFirstName.setText(resultFirstName);
                //add surname to TextView
                TextView forSurname = new TextView(this);
                forSurname.setText(resultSurname);
                //add connect button
                Button connect = new Button(this);
                connect.setText("Connect");
                connect.setTextColor(Color.WHITE);
                connect.setBackgroundColor(getResources().getColor(R.color.header));
                connect.setPadding(5, 5, 5, 5);
                connect.setOnClickListener(connectOnClick(connect, resultUsername));

                //add the views to the row
                row.addView(forUsername);
                row.addView(forFirstName);
                row.addView(forSurname);
                row.addView(connect);

                searchTable.addView(row, i + 1);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }

    View.OnClickListener connectOnClick(final Button button, final String targetUsername) {
        return new View.OnClickListener() {
            public void onClick(View view) {
                connectUsers(targetUsername);
                button.setText("Connection Requested");
                button.setTextSize(11);
                button.setClickable(false);
            }
        };
    }


    private void connectUsers(String targetUser) {
        HashMap<String, String> connectRequest = new HashMap<String, String>();

        //this is adding the username as null - INCORRECT
        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);

        //add search to HashMap
        connectRequest.put("username", username);
        connectRequest.put("target", targetUser);

        //Create new HttpClient and Post Header
        HttpClient httpclient = new DefaultHttpClient();
        HttpPost httppost = new HttpPost("http://raptor.kent.ac.uk:5000/api/createConnection");
        System.out.println(connectRequest);
        //assigns the HashMap to list, for post request encoding
        try {
            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);

            Set<Map.Entry<String, String>> detailsSet = connectRequest.entrySet();
            for (Map.Entry<String, String> string : detailsSet) {
                nameValuePairs.add(new BasicNameValuePair(string.getKey(), string.getValue()));
            }

            //pass the list to the post request
            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
            HttpResponse response = httpclient.execute(httppost);
            String responseString = EntityUtils.toString(response.getEntity());
            System.out.println(responseString);

        } catch (ClientProtocolException e) {
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

