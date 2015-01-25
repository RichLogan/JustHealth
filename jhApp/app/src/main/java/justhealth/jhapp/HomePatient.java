package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.IconTextView;
import android.widget.ImageButton;
import android.widget.ImageView;

public class HomePatient extends Activity {

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.home_patient);

        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle(username);

        IconTextView settings = (IconTextView) findViewById(R.id.settings);
        settings.setOnClickListener(
                new Button.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(HomePatient.this, Settings.class));
                    }
                }
        );

        IconTextView search = (IconTextView) findViewById(R.id.search);
        search.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomePatient.this, Search.class));
                }
            }
        );

        IconTextView connections = (IconTextView) findViewById(R.id.connections);
        connections.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomePatient.this, Connections.class));
                }
            }
        );

        IconTextView appointments = (IconTextView) findViewById(R.id.appointments);
        appointments.setOnClickListener(
                new Button.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(HomePatient.this, SelfAppointments.class));
                    }
                }
        );

        IconTextView profile = (IconTextView) findViewById(R.id.profile);
        profile.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomePatient.this, Profile.class));
                }
            }
        );

        IconTextView medication  = (IconTextView) findViewById(R.id.medication);
        medication.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomePatient.this, PatientMedication.class));
                }
            }
        );
    }
}