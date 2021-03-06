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
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;

import com.joanzapata.android.iconify.Iconify;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class Search extends Activity {

    /**
     * This method runs when the page is first loaded. Sets the correct xml layout and sets the
     * correct action bar. Onclick listener for the search button.
     *
     * @param savedInstanceState a bundle if the state of the application was to be saved.
     */
    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.search);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Search");

        // On Search Press
        Button search = (Button) findViewById(R.id.searchButton);
        search.setOnClickListener(
            new View.OnClickListener() {
                public void onClick(View view) {
                    searchName();
                }
            }
        );
    }

    /**
     * This makes a post request to the JustHealth API in order to be able to search for other
     * users. Gets the logged in user from shared preferences and the search term from the
     * JustHealth API.
     * If the json return is null then toasts nothing found, otherwise runs the printTable method,
     * to print the results to the page.
     */
    private void searchName() {
        HashMap<String, String> searchInformation = new HashMap<String, String>();

        // Get Username
        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);

        // Add search to HashMap
        searchInformation.put("username", username);
        searchInformation.put("searchterm", ((EditText) findViewById(R.id.searchField)).getText().toString());

        String response = Request.post("searchPatientCarer", searchInformation, getApplicationContext());
        if (response.equals("No users found")) {
            Feedback.toast("No users found matching your search query", false, getApplicationContext());
            return;
        }
        try {
            JSONArray queryReturn = new JSONArray(response);
            printTable(queryReturn);
        }
        catch (JSONException e) {
            Feedback.toast("Could not load search results", false, getApplicationContext());
        }
    }


    /**
     * Prints out the results (people to connect too) into a table.
     *
     * @param array JSONArray, the result of the post request, the people that the user may
     *              connect too.
     */
    private void printTable(JSONArray array) {
        TableLayout searchTable = (TableLayout) findViewById(R.id.searchTable);
        searchTable.removeAllViews();

        //create heading row
        TableRow head = new TableRow(this);
        head.setBackgroundColor(getResources().getColor(R.color.header));

        //create the headings of the table
        TextView headingUsername = new TextView(this);
        headingUsername.setTextColor(Color.WHITE);
        headingUsername.setPadding(0,0,25,0);

        TextView headingFirstName = new TextView(this);
        headingFirstName.setTextColor(Color.WHITE);
        headingFirstName.setPadding(0,0,25,0);

        TextView headingSurname = new TextView(this);
        headingSurname.setTextColor(Color.WHITE);
        headingSurname.setPadding(0,0,25,0);

        TextView headingAction = new TextView(this);
        headingAction.setTextColor(Color.WHITE);

        headingUsername.setText("Username");
        headingFirstName.setText("First Name");
        headingSurname.setText("Surname");
        headingAction.setText("");

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
                forUsername.setPadding(0,0,25,0);

                //add first name to TextView
                TextView forFirstName = new TextView(this);
                forFirstName.setText(resultFirstName);
                forFirstName.setPadding(0,0,25,0);

                //add surname to TextView
                TextView forSurname = new TextView(this);
                forSurname.setText(resultSurname);
                forSurname.setPadding(0,0,25,0);

                //Add connect button
                Button connect = new Button(this);
                connect.setTextColor(Color.WHITE);

                // Check if connection is already established
                try {
                    final String resultMessage = obj.getString("message");

                    if (resultMessage.equals("Already Connected")) {
                        connect.setText("{fa-check}");
                        connect.setBackgroundColor(getResources().getColor(R.color.primary));
                    }
                    else {
                        connect.setText("{fa-question}");
                        connect.setBackgroundColor(getResources().getColor(R.color.warning));
                    }

                    connect.setOnClickListener(new Button.OnClickListener() {
                        public void onClick(View view) {
                            AlertDialog.Builder alert = new AlertDialog.Builder(Search.this);
                            alert.setTitle(resultMessage);
                            alert.setMessage("Would you like to view this connection?");
                            alert.setNegativeButton("Cancel", null);
                            alert.setPositiveButton("Go to connections", new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int whichButton) {
                                    startActivity(new Intent(Search.this, ConnectionsMain.class));
                                }
                            });
                            alert.show();
                        }
                    });
                } catch (JSONException e) {
                    // No connection existing
                    connect.setText("{fa-user-plus}");
                    connect.setBackgroundColor(getResources().getColor(R.color.success));
                    connect.setOnClickListener(connectOnClick(connect, resultUsername));
                }

                // Render Icons
                Iconify.addIcons(connect);

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

    /**
     * This method is the action listener that is applied to the Connect button to create a new connection after searching for a user.
     * It runs the connect method, gives you the option to cancel or connect and changes the text on the button and stops the button being clicked again.
     *
     * @param button the button that the onclick listener is applied too
     * @param targetUsername the username of the person that they want to remove as a connection
     */

    View.OnClickListener connectOnClick(final Button button, final String targetUsername) {
        return new View.OnClickListener() {
            public void onClick(View view) {
                // Confirm connect to targerUsername
                AlertDialog.Builder alert = new AlertDialog.Builder(Search.this);
                alert.setTitle("Add Connection");
                alert.setMessage("Are you sure you would like to connect to " + targetUsername);
                alert.setNegativeButton("Cancel", null);
                alert.setPositiveButton("Confirm", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int whichButton) {

                        // Create Connection
                        HashMap<String, String> connectRequest = new HashMap<String, String>();
                        String username = getSharedPreferences("account", 0).getString("username", null);
                        connectRequest.put("username", username);
                        connectRequest.put("target", targetUsername);
                        String result = Request.post("createConnection", connectRequest, getApplicationContext());

                        // Display Information
                        AlertDialog.Builder alert = new AlertDialog.Builder(Search.this);
                        alert.setTitle("Request Sent");
                        alert.setMessage("Your connection code for " + targetUsername + " is: " + result);
                        alert.show();

                        // Disable Connection Button
                        button.setText(result);

                        // Change Button action to show the new connection
                        button.setOnClickListener(new Button.OnClickListener() {
                            public void onClick(View view) {
                                AlertDialog.Builder alert = new AlertDialog.Builder(Search.this);
                                alert.setTitle("Connections");
                                alert.setMessage("Would you like to view this connection?");
                                alert.setNegativeButton("Cancel", null);
                                alert.setPositiveButton("Go to connections", new DialogInterface.OnClickListener() {
                                    public void onClick(DialogInterface dialog, int whichButton) {
                                        startActivity(new Intent(Search.this, ConnectionsMain.class));
                                    }
                                });
                                alert.show();
                            }
                        });
                    }
                });
                alert.show();
            }
        };
    }
}
