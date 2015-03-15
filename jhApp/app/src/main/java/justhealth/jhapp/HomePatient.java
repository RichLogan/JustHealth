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

public class HomePatient extends Activity {
    /**
     * Creates the action bar items for the home patient page
     * @param savedInstanceState The options menu in which the items are placed
     * @return True must be returned in order for the terms and conditions page to be displayed
     * This page displays 6 buttons for a user to access all settings options
     */
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.home_patient);

        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle(username);

        //Settings page
        IconTextView settings = (IconTextView) findViewById(R.id.settings);
        settings.setOnClickListener(
                new Button.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(HomePatient.this, Settings.class));
                    }
                }
        );

        //Search Page
        IconTextView search = (IconTextView) findViewById(R.id.search);
        search.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomePatient.this, Search.class));
                }
            }
        );

        //Connections page
        IconTextView connections = (IconTextView) findViewById(R.id.connections);
        connections.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomePatient.this, ConnectionsMain.class));
                }
            }
        );

        //Personal Appoinments page
        IconTextView appointments = (IconTextView) findViewById(R.id.appointments);
        appointments.setOnClickListener(
                new Button.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(HomePatient.this, SelfAppointments.class));
                    }
                }
        );

        //Profile page
        IconTextView profile = (IconTextView) findViewById(R.id.profile);
        profile.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomePatient.this, Profile.class));
                }
            }
        );

        //Medication oage
        IconTextView medication  = (IconTextView) findViewById(R.id.medication);
        medication.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomePatient.this, PatientPrescription.class));
                }
            }
        );
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (!Request.serverAvailable()) {
            Feedback.toast(getString(R.string.connectionIssue), false, getApplicationContext());
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu items for use in the action bar
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.action_bar_home_screen_patient, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle presses on the action bar items
        switch (item.getItemId()) {
            case R.id.search_badge:
                startActivity(new Intent(HomePatient.this, SearchNHSWebsite.class));
                return true;
            case R.id.notes:
                startActivity(new Intent(HomePatient.this, PatientCorrespondence.class));
            default:
                return super.onOptionsItemSelected(item);
        }
    }
}