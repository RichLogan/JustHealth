package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

/**
 * Created by Stephen on 15/02/15.
 */
public class ExpiredPassword extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.expired_password);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Reset Password");

        Intent intent = getIntent();
        String message = intent.getStringExtra("message");

        TextView messageView = (TextView) findViewById(R.id.input);
        messageView.setText(message);

        Button registerButton = (Button) findViewById(R.id.submit);
        registerButton.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        sendResetExpiredPassword();
                    }
                }
        );


    }

    private void sendResetExpiredPassword() {
        HashMap<String, String> details = new HashMap<String, String>();

        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        //Text Boxes
        details.put("username", username);

        //check the passwords match before adding to the HashMap
        String password = ((EditText) findViewById(R.id.newPassword)).getText().toString();
        String confirm = ((EditText) findViewById(R.id.confirmNewPassword)).getText().toString();
        if (password.equals(confirm)) {
            //even though the if statement covers this they still need to both be sent to not break back-end validation
            details.put("newpassword", password);
            details.put("confirmnewpassword", confirm);
        }
        else {
            Feedback.toast("The two passwords entered do not match", false, getApplicationContext());
            Intent intent = getIntent();
            finish();
            startActivity(intent);
        }

        //make post request
        String response = Request.post("expiredResetPassword", details, getApplicationContext());
        if (response.equals("True")) {
            //overwriting with new encrypted password
            String encryptedPassword = getEncryptedPassword(password);
            SharedPreferences.Editor edit = account.edit();
            edit.putString("password", encryptedPassword);
            edit.commit();

            if (getAccountType(username).equals("Patient")) {
                startActivity(new Intent(ExpiredPassword.this, HomePatient.class));
            } else if (getAccountType(username).equals("Carer")) {
                startActivity(new Intent(ExpiredPassword.this, HomeCarer.class));
            }
        }
        else if(response.equals("Unmatched")) {
            Feedback.toast("The two passwords you entered did not match, please try again.", false, getApplicationContext());
            Intent intent = getIntent();
            finish();
            startActivity(intent);
        }
        else {
            Feedback.toast("Oops, something went wrong. Please try again.", false, getApplicationContext());
            Intent intent = getIntent();
            finish();
            startActivity(intent);
        }

    }

    private String getAccountType(String username) {
        HashMap<String, String> parameters = new HashMap<String, String>();
        parameters.put("username", username);

        String response = Request.post("getAccountInfo", parameters, getApplicationContext());
        try {
            JSONObject accountDetails = new JSONObject(response);
            String accountType  = accountDetails.getString("accounttype");
            return accountType;
        }
        catch (JSONException e) {
            System.out.println(e.getStackTrace());
        }
        return null;
    }

    private String getEncryptedPassword(String plaintextPassword) {
        HashMap<String, String> ptPassword = new HashMap<String, String>();
        ptPassword.put("password", plaintextPassword);
        String response = Request.post("encryptPassword", ptPassword, getApplicationContext());
        return response;
    }
}
