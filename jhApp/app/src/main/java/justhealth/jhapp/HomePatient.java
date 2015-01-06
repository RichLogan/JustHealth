package justhealth.jhapp;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;

public class HomePatient extends Activity {

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.home_patient);

        ImageButton settings = (ImageButton) findViewById(R.id.settings);
        settings.setOnClickListener(
                new Button.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(HomePatient.this, Settings.class));
                    }
                }
        );

        Button search = (Button) findViewById(R.id.search);
        search.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomePatient.this, Search.class));
                }
            }
        );

        Button connections = (Button) findViewById(R.id.connections);
        connections.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomePatient.this, Connections.class));
                }
            }
        );

        Button appointments = (Button) findViewById(R.id.appointments);
        appointments.setOnClickListener(
                new Button.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(HomePatient.this, SelfAppointments.class));
                    }
                }
        );

        ImageButton profile = (ImageButton) findViewById(R.id.profile);
        profile.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomePatient.this, Profile.class));
                }
            }
        );

        Button medication  = (Button) findViewById(R.id.medication);
        medication.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomePatient.this, PatientMedication.class));
                }
            }
        );
    }
}