package justhealth.jhapp;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;

public class HomeCarer extends Activity {

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.home_carer);

        ImageButton settings = (ImageButton) findViewById(R.id.settings);
        settings.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomeCarer.this, Settings.class));
                }
            }
        );

        Button search = (Button) findViewById(R.id.search);
        search.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomeCarer.this, Search.class));
                }
            }
        );

        Button connections = (Button) findViewById(R.id.connections);
        connections.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomeCarer.this, Connections.class));
                }
            }
        );

        Button mypatients = (Button) findViewById(R.id.mypatients);
        mypatients.setOnClickListener(
            new Button.OnClickListener() {
                public void onClick(View view) {
                    startActivity(new Intent(HomeCarer.this, MyPatients.class));
                }
            }
        );

        Button appointments = (Button) findViewById(R.id.myAppointments);
        appointments.setOnClickListener(
                new Button.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(HomeCarer.this, SelfAppointments.class));
                    }
                }
        );

        ImageButton profile = (ImageButton) findViewById(R.id.profile);
        profile.setOnClickListener(
                new Button.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(HomeCarer.this, Profile.class));
                    }
                }
        );
    }
}
