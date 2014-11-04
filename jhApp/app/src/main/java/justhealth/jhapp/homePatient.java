package justhealth.jhapp;

import android.content.Intent;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

/**
 * Created by charlottehutchinson on 04/11/14.
 */
public class homePatient  {

/**    @Override
    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);

        TextView deactivate = (TextView)findViewById(R.id.action_settings);
        deactivate.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(homePatient.this,ForgotPassword.class));
                    }
                }
        );



    }


   */

}
