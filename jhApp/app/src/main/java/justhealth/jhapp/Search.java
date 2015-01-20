package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class Search extends Activity {

    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.search);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Search");


        //check for the search button being pressed
        Button search = (Button) findViewById(R.id.searchButton);
        search.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        searchName();
                    }
                }
        );

    }

    private void searchName() {
        HashMap<String, String> searchInformation = new HashMap<String, String>();

        // Get Username
        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);

        // Add search to HashMap
        searchInformation.put("username", username);
        searchInformation.put("searchterm", ((EditText) findViewById(R.id.searchField)).getText().toString());

        String response = Request.post("searchPatientCarer", searchInformation, getApplicationContext());
        try {
            JSONArray queryReturn = new JSONArray(response);
            printTable(queryReturn);
        }
        catch (JSONException e) {
            System.out.println(e.getStackTrace());
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
                String resultUsername = obj.getString("username");
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

                // Check if connection is already established
                String resultMessage = null;
                try {
                    resultMessage = obj.getString("message");
                    connect.setText(resultMessage);
                    connect.setOnClickListener(
                        new Button.OnClickListener() {
                            public void onClick(View view) {
                                AlertDialog.Builder alert = new AlertDialog.Builder(Search.this);
                                alert.setTitle("View Connections");
                                alert.setMessage("Would you like to view this connection?");
                                alert.setNegativeButton("Cancel", null);
                                alert.setPositiveButton("Go to connections", new DialogInterface.OnClickListener() {
                                    public void onClick(DialogInterface dialog, int whichButton) {
                                        startActivity(new Intent(Search.this, Connections.class));
                                    }
                                });
                                alert.show();
                            }
                        }
                    );
                }
                catch (JSONException e) {
                    connect.setText("Connect");
                    connect.setOnClickListener(connectOnClick(connect, resultUsername));
                }
                connect.setTextColor(Color.WHITE);
                connect.setBackgroundColor(getResources().getColor(R.color.header));
                connect.setPadding(5, 5, 5, 5);

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

        Request.post("createConnection", connectRequest, getApplicationContext());
    }
}

