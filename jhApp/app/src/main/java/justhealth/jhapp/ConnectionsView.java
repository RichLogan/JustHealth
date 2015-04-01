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
import android.support.v7.widget.CardView;
import android.text.Editable;
import android.text.InputFilter;
import android.text.InputType;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.SpinnerAdapter;
import android.widget.TextView;

import com.joanzapata.android.iconify.Iconify;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

/**
 * Lists of Connections of the given category (Incoming, Outgoing, Completed) as given by ConnectionsMain
 */
public class ConnectionsView extends Activity {
    String type;
    Boolean ignoreChange = true;

    /**
     * This method runs when the page is first loaded.
     * Sets the correct xml layout to be displayed and loads the action bar.
     * The print connections method is also run.
     *
     * @param savedInstanceState a bundle if the state of the application was to be saved.
     */
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.connections_view);

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        // Get Type Selected
        final HashMap<String, Integer> positions = new HashMap<String, Integer>();
        positions.put("incoming", 0);
        positions.put("outgoing", 1);
        positions.put("completed", 2);

        final Bundle extras = getIntent().getExtras();
        if (extras != null) {
            type = extras.getString("type");
            getActionBar().setNavigationMode(ActionBar.NAVIGATION_MODE_LIST);
            getActionBar().setSelectedNavigationItem(positions.get(type));
        }
        // Action Bar
        final ActionBar actions = getActionBar();
        final SpinnerAdapter adapter = ArrayAdapter.createFromResource(this, R.array.connectionActions, android.R.layout.simple_spinner_dropdown_item);
        ActionBar.OnNavigationListener callback = new ActionBar.OnNavigationListener() {
            String[] items = getResources().getStringArray(R.array.connectionActions);
            @Override
            public boolean onNavigationItemSelected(int position, long id) {
                if (!ignoreChange) {
                    // Set Type to selected
                    type = items[position];
                    actions.setSelectedNavigationItem(position);
                    // Redraw Connections
                    ViewGroup vg = (ViewGroup) findViewById(R.id.connectionsList);
                    vg.removeAllViews();
                    printConnections();
                    return true;
                }
                // Don't reset to position 0 first time they open the page (i.e. From the menu)
                actions.setSelectedNavigationItem(positions.get(type));
                ignoreChange = false;
                return true;
            }
        };
        actions.setDisplayShowTitleEnabled(false);
        actions.setListNavigationCallbacks(adapter, callback);

        // Print Connections
        printConnections();
    }

    /**
     * Prints the connections as Cards, displaying names, pictures, and a positive and negative
     * action that is defined by the type of connection it is.
     */
    private void printConnections() {
        try {
            // Connections of selected type
            JSONArray listConnections = new JSONArray(getConnections().getString(type));

            //Parent LinearLayout
            LinearLayout mainList = (LinearLayout) findViewById(R.id.connectionsList);
            mainList.setOrientation(LinearLayout.VERTICAL);

            //For every connection
            //Make the card, fill the insides (profile, picture, name, (code) etc..)
            for (int i = 0; i < listConnections.length(); i++) {
                // Get Connection's Details
                JSONObject connection = listConnections.getJSONObject(i);
                String username = connection.getString("username");
                String firstname = connection.getString("firstname");
                String surname = connection.getString("surname");
                String filepath = LoadImage.getProfilePictureURL(connection.getString("profilepicture"));

                // Card
                CardView card = new CardView(this);
                LinearLayout container = new LinearLayout(this);
                container.setOrientation(LinearLayout.VERTICAL);
                int cardHeight = 450;
                int profilePictureHeight = 325;
                int captionBarHeight = cardHeight - profilePictureHeight;
                // Profile Container
                FrameLayout profilePictureContainer = new FrameLayout(this);
                ImageView background = new ImageView(this);
                new LoadImage(background, true, getApplicationContext()).execute(filepath);
                background.setScaleType(ImageView.ScaleType.CENTER_CROP);
                // Profile Picture
                ImageView profilePicture = new ImageView(this);
                new LoadImage(profilePicture, false, getApplicationContext()).execute(filepath);
                profilePictureContainer.addView(background, FrameLayout.LayoutParams.MATCH_PARENT, profilePictureHeight);
                profilePictureContainer.addView(profilePicture);

                // Caption Container
                LinearLayout captionContainer = new LinearLayout(this);
                captionContainer.setOrientation(LinearLayout.HORIZONTAL);

                //Name
                TextView name = new TextView(this);
                name.setText(firstname + " " + surname);
                name.setPadding(25,0,25,0);
                name.setGravity(Gravity.CENTER | Gravity.CENTER_VERTICAL);
                captionContainer.addView(name);

                // Pushes buttons to the right (Thanks to http://stackoverflow.com/questions/3224193/set-the-layout-weight-of-a-textview-programmatically)
                View spacer = new View(this);
                spacer.setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT, 1f));
                captionContainer.addView(spacer);

                // Positive Action
                TextView positiveAction = new TextView(this);
                positiveAction.setGravity(Gravity.CENTER | Gravity.CENTER_VERTICAL);
                positiveAction.setBackgroundColor(getResources().getColor(R.color.success));
                positiveAction.setTextColor(getResources().getColor(R.color.white));
                setPositiveAction(positiveAction, connection);
                Iconify.addIcons(positiveAction);
                captionContainer.addView(positiveAction, 200, captionBarHeight);

                // Negative Action
                TextView negativeAction = new TextView(this);
                negativeAction.setGravity(Gravity.CENTER | Gravity.CENTER_VERTICAL);
                negativeAction.setBackgroundColor(getResources().getColor(R.color.danger));
                negativeAction.setTextColor(getResources().getColor(R.color.white));
                negativeAction.setText("{fa-user-times}");
                Iconify.addIcons(negativeAction);
                setNegativeAction(negativeAction, connection);
                captionContainer.addView(negativeAction, 200, captionBarHeight);

                // Add Containers
                container.addView(profilePictureContainer, LinearLayout.LayoutParams.MATCH_PARENT, profilePictureHeight);
                container.addView(captionContainer, LinearLayout.LayoutParams.FILL_PARENT, captionBarHeight);
                card.addView(container, LinearLayout.LayoutParams.MATCH_PARENT, cardHeight);
                mainList.addView(card, LinearLayout.LayoutParams.MATCH_PARENT, cardHeight);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    /**
     * Sets the positive action of a card to reflect the type of connection it is
     * @param pos The TextView representing the positive action button
     * @param details The details of this connection
     */
    private void setPositiveAction(TextView pos, final JSONObject details) {
        if (type.equals("incoming")) {
            pos.setText("{fa-user-plus}");
            pos.setOnClickListener(new View.OnClickListener(){
                @Override
                public void onClick(View v) {
                    try {
                        enterCode(details.getString("username"), "");
                    } catch (JSONException e) {
                        Feedback.toast("Could not access connection information", false, getApplicationContext());
                    }
                }
            });
        }
        else if (type.equals("outgoing")) {
            try {
                pos.setText(details.getString("code"));
            } catch (JSONException e) { e.printStackTrace(); }
        }
        else if (type.equals("completed")) {
            pos.setText("{fa-check}");
        }
    }

    /**
     * Sets the negative action of a card to reflect the type of connection it is
     * @param neg The TextView representing the negative action button
     * @param details The details of this connection
     */
    private void setNegativeAction(TextView neg, final JSONObject details) {
        neg.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    final HashMap<String, String> parameters = new HashMap<String, String>();
                    parameters.put("user", getSharedPreferences("account", 0).getString("username", null));
                    parameters.put("connection", details.getString("username"));

                    AlertDialog.Builder alert = new AlertDialog.Builder(ConnectionsView.this);
                    if (type.equals("incoming")) {
                        // Reject
                        alert.setTitle("Reject Connection/?");
                        alert.setMessage("Are you sure you want to reject the connection request from \"" + details.getString("firstname") + " " + details.getString("surname") + " (" + details.getString("username") + ")\"?");
                        alert.setPositiveButton("Confirm Reject", new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int whichButton) {
                                // Post to Reject
                                String response = Request.post("cancelConnection", parameters, getApplicationContext());
                                if (response.equals("True")) {
                                    finish();
                                    startActivity(getIntent());
                                }
                                else {
                                    Feedback.toast("Connection rejection failed. Please try again.", false, getApplicationContext());
                                }
                            }
                        });
                    } else if (type.equals("outgoing")) {
                        //Cancel
                        alert.setTitle("Cancel Connection/?");
                        alert.setMessage("Are you sure you want to cancel the connection request from \"" + details.getString("firstname") + " " + details.getString("surname") + " (" + details.getString("username") + ")\"?");
                        alert.setPositiveButton("Confirm Cancel", new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int whichButton) {
                                // Post to Cancel
                                String response = Request.post("cancelConnection", parameters, getApplicationContext());
                                if (response.equals("True")) {
                                    finish();
                                    startActivity(getIntent());
                                }
                                else {
                                    Feedback.toast("Cancellation failed. Please try again.", false, getApplicationContext());
                                }
                            }
                        });

                    } else if (type.equals("completed")) {
                        // Delete
                        alert.setTitle("Delete Connection/?");
                        alert.setMessage("Are you sure you want to delete your connection to \"" + details.getString("firstname") + " " + details.getString("surname") + " (" + details.getString("username") + ")\"?");
                        alert.setPositiveButton("Confirm Reject", new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int whichButton) {
                                String response = Request.post("deleteConnection", parameters, getApplicationContext());
                                if (response.equals("True")) {
                                    finish();
                                    startActivity(getIntent());
                                }
                                else {
                                    Feedback.toast("Connection deletion failed. Please try again.", false, getApplicationContext());
                                }
                            }
                        });
                    }
                    alert.setNegativeButton("No", null);
                    alert.show();
                } catch (JSONException e) {
                    Feedback.toast("Failed to get connection information", false, getApplicationContext());
                }
            }
        });
    }

    /**
     * Returns all Connection for the user
     * @return JSONObject of all connections
     */
    private JSONObject getConnections() {
        HashMap<String, String> getConnectionsInfo = new HashMap<String, String>();
        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        getConnectionsInfo.put("username", username);

        String response = Request.post("getConnections", getConnectionsInfo, getApplicationContext());

        try {
            return new JSONObject(response);
        } catch (JSONException e) {
            return null;
        }
    }

    /**
     * Displays a custom alert message in order to allow a user to enter the 4 digit code.
     * Also where feedback from submitCode() is displayed.
     * @param requestor The username to connect to
     * @param message Any extra message to display
     */
    private void enterCode(final String requestor, String message) {
        // Complete Connection
        AlertDialog.Builder alert = new AlertDialog.Builder(this);
        alert.setTitle("Please enter the verification code given by the requester");

        // Set an EditText view to get user input
        final EditText input = new EditText(getApplicationContext());
        input.setTextColor(Color.BLACK);
        input.setTextSize(25);
        input.setHint("Enter your connection's code");
        input.setGravity(Gravity.CENTER);
        input.setInputType(InputType.TYPE_CLASS_NUMBER);

        //set the maximum length of the field to be 4 numbers
        InputFilter[] filterArray = new InputFilter[1];
        filterArray[0] = new InputFilter.LengthFilter(4);
        input.setFilters(filterArray);
        alert.setView(input);
        alert.setMessage(message);
        alert.setPositiveButton("OK", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int whichButton) {
                Editable value = input.getText();
                String code = value.toString();
                submitCode(requestor, code);
            }
        });
        alert.setNegativeButton("Cancel", null);
        alert.show();
    }

    /**
     * This submits the code that was entered into the alert box by the user to the server.
     * Providing that the code is correct it then refreshes the connections page and informs the user.
     * If an incorrect code has been entered it also tells the user.
     * @param requestor the username of the user that has requested the connection.
     * @param codeAttempt the code that has been entered by the current user.
     */
    private void submitCode(String requestor, String codeAttempt) {
        HashMap<String, String> attemptParameters = new HashMap<String, String>();
        attemptParameters.put("username", getSharedPreferences("account", 0).getString("username", null));
        attemptParameters.put("requestor", requestor);
        attemptParameters.put("codeattempt", codeAttempt);

        String response = Request.post("completeConnection", attemptParameters, getApplicationContext());
        String expectedResponse = "Connection to " + requestor + " completed";
        if(response.equals(expectedResponse)) {
            Feedback.toast(expectedResponse, true, getApplicationContext());
            finish();
            startActivity(new Intent(ConnectionsView.this, ConnectionsMain.class));
        }
        else {
            enterCode(requestor, "An incorrect code was entered. Please try again.");
        }
    }
}
