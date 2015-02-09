package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.util.HashMap;

public class ForgotPassword extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.forgot_password);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Forgot Password");

        Button submitButton = (Button) findViewById(R.id.submit);
        submitButton.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        getDetails();
                    }
                }
        );
    }

    private void getDetails() {
        HashMap<String, String> details = new HashMap<String, String>();
        details.put("username", ((EditText) findViewById(R.id.loginUsername)).getText().toString());
        details.put("confirmemail", ((EditText) findViewById(R.id.email)).getText().toString());
        details.put("newpassword", ((EditText) findViewById(R.id.newPassword)).getText().toString());
        details.put("confirmnewpassword", ((EditText) findViewById(R.id.confirmNewPassword)).getText().toString());
        details.put("confirmdob", ((EditText) findViewById(R.id.dob)).getText().toString());
        post(details);
    }

    public void post(HashMap<String, String> details) {
        String response = Request.post("resetPassword", details, getApplicationContext());

        if (!response.equals("True")) {
            Feedback.toast(response, false, getApplicationContext());
        }
    }
}