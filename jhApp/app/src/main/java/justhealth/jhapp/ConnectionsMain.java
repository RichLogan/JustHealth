package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.RelativeLayout;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class ConnectionsMain extends Activity {

    JSONArray incoming = null;
    JSONArray outgoing = null;
    JSONArray completed = null;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.connections_main);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Connections");

        // Assign Button Actions
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

        getConnections();
        loadBadges();
    }

    private void getConnections() {
        HashMap<String, String> getConnectionsInfo = new HashMap<String, String>();
        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        getConnectionsInfo.put("username", username);

        String response = Request.post("getConnections", getConnectionsInfo, getApplicationContext());

        try {
            JSONObject result = new JSONObject(response);
            outgoing = new JSONArray(result.getString("outgoing"));
            incoming = new JSONArray(result.getString("incoming"));
            completed = new JSONArray(result.getString("completed"));
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private void loadBadges() {
        String incomingCount = Integer.toString(incoming.length());
        String outgoingCount = Integer.toString(outgoing.length());
        String completedCount = Integer.toString(completed.length());

        ((TextView) findViewById(R.id.incomingBadge)).setText(incomingCount);
        ((TextView) findViewById(R.id.outgoingBadge)).setText(outgoingCount);
        ((TextView) findViewById(R.id.completedBadge)).setText(completedCount);
    }
}