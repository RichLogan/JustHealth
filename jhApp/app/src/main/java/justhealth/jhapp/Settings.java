package justhealth.jhapp;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.widget.Button;

/**
 * Created by charlottehutchinson on 06/11/14.
 */

public class Settings extends ActionBarActivity{

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.settings);

        Button deactivate = (Button)findViewById(R.id.deactivate);
        deactivate.setOnClickListener(
                new Button.OnClickListener() {
            public void onClick(View view) {
                startActivity(new Intent(Settings.this, DeactivateAccount.class));
            }
        }
        );
    }
}
