package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.IconTextView;

public class HomeCarer extends Activity {

    /**
     * Creates the action bar items for the home carer page
     * @param savedInstanceState The options menu in which the items are placed
     * @return True must be returned in order for the terms and conditions page to be displayed
     * This page displays 6 buttons for a user to access all settings options
     */
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.home_carer);

        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle(username);

        System.out.println("Ping");
        Request.serverCheck(this);
        System.out.println("Completed");

        // Settings button
        IconTextView settings = (IconTextView) findViewById(R.id.settings);
        settings.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomeCarer.this, Settings.class));
                }
            }
        );

        // Search button
        IconTextView search = (IconTextView) findViewById(R.id.search);
        search.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomeCarer.this, Search.class));
                }
            }
        );

        // Search button
        IconTextView connections = (IconTextView) findViewById(R.id.connections);
        connections.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomeCarer.this, ConnectionsMain.class));
                }
            }
        );

        // My Patients button
        IconTextView mypatients = (IconTextView) findViewById(R.id.mypatients);
        mypatients.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomeCarer.this, MyPatients.class));
                }
            }
        );

        // Personal appointments button
        IconTextView appointments = (IconTextView) findViewById(R.id.myAppointments);
        appointments.setOnClickListener(
                new Button.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(HomeCarer.this, SelfAppointments.class));
                    }
                }
        );

        // Profile page button
        IconTextView profile = (IconTextView) findViewById(R.id.profile);
        profile.setOnClickListener(
                new Button.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(HomeCarer.this, Profile.class));
                    }
                }
        );
    }

    /**
     * When the page is loaded after the first time this method is run.
     */
    @Override
    protected void onResume() {
        super.onResume();
        Request.serverCheck(this);
    }

    /**
     * Creates the action bar items for the Carer Home page
     *
     * @param menu The options menu in which the items are placed
     * @return True must be returned in order for the options menu to be displayed
     */
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu items for use in the action bar
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.action_bar_home_screen_carer, menu);
        return super.onCreateOptionsMenu(menu);
    }

    /**
     * This method is called when any action from the action bar is selected
     *
     * @param item The menu item that was selected
     * @return in order for the method to work, true should be returned here
     */
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle presses on the action bar items
        switch (item.getItemId()) {
            case R.id.search_badge:
                startActivity(new Intent(HomeCarer.this, SearchNHSWebsite.class));
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }

}
