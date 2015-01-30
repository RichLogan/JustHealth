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
import android.widget.ImageButton;

public class HomeCarer extends Activity {

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.home_carer);

        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle(username);

        IconTextView settings = (IconTextView) findViewById(R.id.settings);
        settings.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomeCarer.this, Settings.class));
                }
            }
        );

        IconTextView search = (IconTextView) findViewById(R.id.search);
        search.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomeCarer.this, Search.class));
                }
            }
        );

        IconTextView connections = (IconTextView) findViewById(R.id.connections);
        connections.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomeCarer.this, Connections.class));
                }
            }
        );

        IconTextView mypatients = (IconTextView) findViewById(R.id.mypatients);
        mypatients.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomeCarer.this, MyPatients.class));
                }
            }
        );

        IconTextView appointments = (IconTextView) findViewById(R.id.myAppointments);
        appointments.setOnClickListener(
                new Button.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(HomeCarer.this, SelfAppointments.class));
                    }
                }
        );

        IconTextView profile = (IconTextView) findViewById(R.id.profile);
        profile.setOnClickListener(
                new Button.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(HomeCarer.this, Profile.class));
                    }
                }
        );
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu items for use in the action bar
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.action_bar_home_screens, menu);
        return super.onCreateOptionsMenu(menu);
    }

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
