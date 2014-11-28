package justhealth.jhapp;

import android.annotation.TargetApi;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.os.StrictMode;
import android.support.v7.app.ActionBarActivity;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
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
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Created by Stephen on 25/11/2014.
 */
public class Connections extends ActionBarActivity {

    private int rowOfTable = 0;

    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.connections);
        getConnections();
    }

    @TargetApi(Build.VERSION_CODES.KITKAT)
    private void getConnections() {
        HashMap<String, String> getConnectionsInfo = new HashMap<String, String>();

        //this is adding the username as null - INCORRECT
        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        String password = account.getString("password", null);

        //add search to HashMap
        getConnectionsInfo.put("username", username);

        //Create new HttpClient and Post Header
        HttpClient httpclient = new DefaultHttpClient();
        String authentication = username + ":" + password;
        String encodedAuthentication = Base64.encodeToString(authentication.getBytes(), Base64.NO_WRAP);

        HttpPost httppost = new HttpPost("http://raptor.kent.ac.uk:5000/api/getConnections");
        httppost.setHeader("Authorization", "Basic " + encodedAuthentication);
        System.out.println(encodedAuthentication);
        //assigns the HashMap to list, for post request encoding
        try {
            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);

            Set<Map.Entry<String, String>> detailsSet = getConnectionsInfo.entrySet();
            for (Map.Entry<String, String> string : detailsSet) {
                nameValuePairs.add(new BasicNameValuePair(string.getKey(), string.getValue()));
            }

            //pass the list to the post request
            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
            HttpResponse response = httpclient.execute(httppost);

            String responseString = EntityUtils.toString(response.getEntity());
            System.out.print(responseString);
            JSONObject queryReturn = null;
            JSONArray outgoing = null;
            JSONArray incoming = null;
            JSONArray completed = null;
            try {
                queryReturn = new JSONObject(responseString);
                System.out.println(queryReturn);
                String outgoingString = queryReturn.getString("outgoing");
                outgoing = new JSONArray(outgoingString);
                String incomingString = queryReturn.getString("incoming");
                incoming = new JSONArray(incomingString);
                String completedString = queryReturn.getString("completed");
                completed = new JSONArray(completedString);

            } catch (JSONException e) {
                e.printStackTrace();
            }

            System.out.print(queryReturn);
            printTableHeader();
            printOutgoingConnections(outgoing);
            printIncomingConnections(incoming);
            printCompletedConnections(completed);

        } catch (ClientProtocolException e) {
            //TODO Auto-generated catch block
        } catch (IOException e) {
            //TODO Auto-generated catch block
        } catch (NullPointerException e) {
            //TODO Auto-generated catch block
        }
    }

    private void printTableHeader() {
        TableLayout searchTable = (TableLayout) findViewById(R.id.connectionsTable);

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

        TextView headingCode = new TextView(this);
        headingSurname.setTextColor(Color.WHITE);
        headingSurname.setPadding(5, 5, 5, 5);

        TextView headingAction = new TextView(this);
        headingAction.setTextColor(Color.WHITE);
        headingAction.setPadding(5, 5, 5, 5);

        headingUsername.setText("Username");
        headingFirstName.setText("First Name");
        headingSurname.setText("Surname");
        headingCode.setText("Code");
        headingAction.setText("Action");

        //add the headings to the row
        head.addView(headingUsername);
        head.addView(headingFirstName);
        head.addView(headingSurname);
        head.addView(headingCode);
        head.addView(headingAction);
        searchTable.addView(head, 0);
    }

    private void printOutgoingConnections(JSONArray outgoing){
        TableLayout searchTable = (TableLayout) findViewById(R.id.connectionsTable);

        TableRow outgoingHeadRow = new TableRow(this);
        outgoingHeadRow.setBackgroundColor(getResources().getColor(R.color.header));
        TextView incomingConnections = new TextView(this);
        incomingConnections.setText("Outgoing Connections");
        incomingConnections.setTextColor(Color.WHITE);

        outgoingHeadRow.addView(incomingConnections);
        searchTable.addView(outgoingHeadRow, 1);
        //update row of table
        rowOfTable += 2;

        if (outgoing.length() == 0) {
            TableRow row = new TableRow(this);
            TextView noRecords = new TextView(this);
            noRecords.setText("No Outgoing Connections");
            row.addView(noRecords);
            searchTable.addView(row, rowOfTable + 1);
            rowOfTable += 1;
        }
        else {

            for (int i = 0; i < outgoing.length(); i++) {
                try {
                    JSONObject obj = outgoing.getJSONObject(i);
                    System.out.println(obj);
                    String outgoingUsername = obj.getString("username");
                    String outgoingFirstName = obj.getString("firstname");
                    String outgoingSurname = obj.getString("surname");
                    String outgoingCode = obj.getString("code");


                    TableRow row = new TableRow(this);
                    //add username to TextView
                    TextView forUsername = new TextView(this);
                    forUsername.setText(outgoingUsername);
                    //add first name to TextView
                    TextView forFirstName = new TextView(this);
                    forFirstName.setText(outgoingFirstName);
                    //add surname to TextView
                    TextView forSurname = new TextView(this);
                    forSurname.setText(outgoingSurname);
                    //add verification code to TextView
                    TextView forCode = new TextView(this);
                    forCode.setText(outgoingCode);
                    //TextView to tell user awaiting response
                    TextView forAction = new TextView(this);
                    forAction.setText("Awaiting " + outgoingUsername + "'s Response");
                /*//add connect button
                Button connect = new Button(this);
                connect.setText("Connect");
                connect.setTextColor(Color.WHITE);
                connect.setBackgroundColor(getResources().getColor(R.color.header));
                connect.setPadding(5, 5, 5, 5);
                connect.setOnClickListener(connectOnClick(connect, resultUsername));*/

                    //add the views to the row
                    row.addView(forUsername);
                    row.addView(forFirstName);
                    row.addView(forSurname);
                    row.addView(forCode);
                    row.addView(forAction);

                    searchTable.addView(row, rowOfTable + i);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
            rowOfTable = outgoing.length();
        }
    }

    private void printIncomingConnections(JSONArray incoming){
        TableLayout searchTable = (TableLayout) findViewById(R.id.connectionsTable);

        TableRow incomingHeadRow = new TableRow(this);
        incomingHeadRow.setBackgroundColor(getResources().getColor(R.color.header));
        TextView incomingConnections = new TextView(this);
        incomingConnections.setText("Incoming Connections");
        incomingConnections.setTextColor(Color.WHITE);

        incomingHeadRow.addView(incomingConnections);
        searchTable.addView(incomingHeadRow, rowOfTable + 1);
        //update row of table
        rowOfTable += 1;

        if (incoming.length() == 0) {
            TableRow row = new TableRow(this);
            TextView noRecords = new TextView(this);
            noRecords.setText("No Incoming Connections");
            row.addView(noRecords);
            searchTable.addView(row, rowOfTable + 1);
            rowOfTable += 1;
        }
        else {

            for (int i = 0; i < incoming.length(); i++) {
                try {
                    JSONObject obj = incoming.getJSONObject(i);
                    System.out.println(obj);
                    String incomingUsername = obj.getString("username");
                    String incomingFirstName = obj.getString("firstname");
                    String incomingSurname = obj.getString("surname");
                    //add button


                    TableRow row = new TableRow(this);
                    //add username to TextView
                    TextView forUsername = new TextView(this);
                    forUsername.setText(incomingUsername);
                    //add first name to TextView
                    TextView forFirstName = new TextView(this);
                    forFirstName.setText(incomingFirstName);
                    //add surname to TextView
                    TextView forSurname = new TextView(this);
                    forSurname.setText(incomingSurname);
                    //add connect button
                    Button connect = new Button(this);
                    connect.setText("Connect");
                    connect.setTextColor(Color.WHITE);
                    connect.setBackgroundColor(getResources().getColor(R.color.header));
                    connect.setPadding(5, 5, 5, 5);
                    //add what to do on click

                    //add the views to the row
                    row.addView(forUsername);
                    row.addView(forFirstName);
                    row.addView(forSurname);
                    row.addView(connect);

                    searchTable.addView(row, rowOfTable + i);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
            rowOfTable += incoming.length();
        }
    }

    private void printCompletedConnections(JSONArray completed){
        TableLayout searchTable = (TableLayout) findViewById(R.id.connectionsTable);

        TableRow incomingHeadRow = new TableRow(this);
        incomingHeadRow.setBackgroundColor(getResources().getColor(R.color.header));
        TextView incomingConnections = new TextView(this);
        incomingConnections.setText("Completed Connections");
        incomingConnections.setTextColor(Color.WHITE);

        incomingHeadRow.addView(incomingConnections);
        searchTable.addView(incomingHeadRow, rowOfTable + 1);
        //update row of table
        rowOfTable += 1;

        if (completed.length() == 0) {
            TableRow row = new TableRow(this);
            TextView noRecords = new TextView(this);
            noRecords.setText("No Completed Connections");
            row.addView(noRecords);
            searchTable.addView(row, rowOfTable + 1);
            rowOfTable += 1;
        }
        else {


            for (int i = 0; i < completed.length(); i++) {
                try {
                    JSONObject obj = completed.getJSONObject(i);
                    System.out.println(obj);
                    String completedUsername = obj.getString("username");
                    String completedFirstName = obj.getString("firstname");
                    String completedSurname = obj.getString("surname");


                    TableRow row = new TableRow(this);
                    //add username to TextView
                    TextView forUsername = new TextView(this);
                    forUsername.setText(completedUsername);
                    //add first name to TextView
                    TextView forFirstName = new TextView(this);
                    forFirstName.setText(completedFirstName);
                    //add surname to TextView
                    TextView forSurname = new TextView(this);
                    forSurname.setText(completedSurname);
                    //add connect button
                    Button remove = new Button(this);
                    remove.setText("Remove");
                    remove.setTextSize(10);
                    remove.setTextColor(Color.WHITE);
                    remove.setBackgroundColor(getResources().getColor(R.color.header));
                    remove.setPadding(5, 5, 5, 5);
                    //add what to do on click

                    //add the views to the row
                    row.addView(forUsername);
                    row.addView(forFirstName);
                    row.addView(forSurname);
                    row.addView(remove);

                    searchTable.addView(row, rowOfTable + i);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
