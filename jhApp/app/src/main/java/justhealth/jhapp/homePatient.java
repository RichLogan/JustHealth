package justhealth.jhapp;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;

/**
 * Created by charlottehutchinson on 04/11/14.
 */



    public class homePatient extends ActionBarActivity {

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.home_patient);

        ImageButton settings = (ImageButton) findViewById(R.id.settings);
        settings.setOnClickListener(
                new Button.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(homePatient.this, homePatient.class));
                    }
                }
        );

        Button search = (Button) findViewById(R.id.search);
        search.setOnClickListener(
                new Button.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(homePatient.this, Search.class));
                    }
                }
        );
    }
}



