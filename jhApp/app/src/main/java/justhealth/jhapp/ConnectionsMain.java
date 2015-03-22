package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.RelativeLayout;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

/**
 * Allows a user access to their incoming, outgoing and completed connections through the creation of ConnectionsView.
 */
public class ConnectionsMain extends Activity {

    JSONArray incoming = null;
    JSONArray outgoing = null;
    JSONArray completed = null;

    /**
     * This method runs when the page is first loaded.
     * Sets the correct xml layout to be displayed and loads the action bar. It has action listeners
     * for the incoming/outgoing and completed buttons (the type of connections).
     * The getConnections method is also run.
     *
     * @param savedInstanceState a bundle if the state of the application was to be saved.
     */
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.connections_main);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Connections");

        // Assign Button Actions

        //Incoming button
        RelativeLayout incomingButton = (RelativeLayout) findViewById(R.id.incomingButton);
        incomingButton.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    Intent intent = new Intent(ConnectionsMain.this, ConnectionsView.class);
                    intent.putExtra("type", "incoming");
                    startActivity(intent);
                }
            }
        );

        // Outgoing button
        RelativeLayout outgoingButton = (RelativeLayout) findViewById(R.id.outgoingButton);
        outgoingButton.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    Intent intent = new Intent(ConnectionsMain.this, ConnectionsView.class);
                    intent.putExtra("type", "outgoing");
                    startActivity(intent);
                }
            }
        );

        // Completed button
        RelativeLayout completedButton = (RelativeLayout) findViewById(R.id.completedButton);
        completedButton.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    Intent intent = new Intent(ConnectionsMain.this, ConnectionsView.class);
                    intent.putExtra("type", "completed");
                    startActivity(intent);
                }
            }
        );

        // Load Connections
        getConnections();
    }

    /**
     * Retrieves ALL connections from the database in order for counts to be calculated and displayed via loadBadges()
     * This is done asynchronously, off of the main thread.
     */
    private void getConnections() {
        final HashMap<String, String> getConnectionsInfo = new HashMap<String, String>();
        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        getConnectionsInfo.put("username", username);

        new AsyncTask<Void, Void, Void>() {
            @Override
            protected Void doInBackground(Void... v) {
                String response = Request.post("getConnections", getConnectionsInfo, getApplicationContext());
                try {
                    JSONObject result = new JSONObject(response);
                    outgoing = new JSONArray(result.getString("outgoing"));
                    incoming = new JSONArray(result.getString("incoming"));
                    completed = new JSONArray(result.getString("completed"));
                } catch (Exception e) {
                    e.printStackTrace();
                    Feedback.toast("Unable to get your connections", false, getApplicationContext());
                }
                return null;
            }

            protected void onPostExecute(Void v) {
                loadBadges();
            }
        }.execute();
    }

    /**
     * Loads the number of connections for each category (Incoming, Outgoing, Completed) onto their respective button.
     */
    private void loadBadges() {
        String incomingCount = Integer.toString(incoming.length());
        String outgoingCount = Integer.toString(outgoing.length());
        String completedCount = Integer.toString(completed.length());

        ((TextView) findViewById(R.id.incomingBadge)).setText(incomingCount);
        ((TextView) findViewById(R.id.outgoingBadge)).setText(outgoingCount);
        ((TextView) findViewById(R.id.completedBadge)).setText(completedCount);
    }
}