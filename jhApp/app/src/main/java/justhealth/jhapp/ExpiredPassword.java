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

    private String username;
    private String expiredPassword;
    private String accountType;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.expired_password);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Reset Password");

        Intent intent = getIntent();
        String message = intent.getStringExtra("message");
        username = intent.getStringExtra("username");
        expiredPassword = intent.getStringExtra("password");
        accountType = intent.getStringExtra("accountType");

        TextView messageView = (TextView) findViewById(R.id.input);
        messageView.setText(message);

        Button reset = (Button) findViewById(R.id.submit);
        reset.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        sendResetExpiredPassword();
                    }
                }
        );


    }

    private void sendResetExpiredPassword() {
        HashMap<String, String> details = new HashMap<String, String>();

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
        //assign SharedPreferences for post request to authenticate
        SharedPreferences account = getSharedPreferences("account", 0);
        SharedPreferences.Editor edit = account.edit();
        edit.putString("username", username);
        edit.putString("password", expiredPassword);

        String response = Request.post("expiredResetPassword", details, getApplicationContext());

        if (response.equals("True")) {
            //overwriting with new encrypted password
            String encryptedPassword = getEncryptedPassword(password);
            edit.putString("password", encryptedPassword);
            edit.putString("accountType", accountType);
            edit.commit();

            startActivity(new Intent(ExpiredPassword.this, Main.class));
        }
        else if(response.equals("Unmatched")) {
            edit.remove("username");
            edit.remove("password");
            edit.clear();
            Feedback.toast("The two passwords you entered did not match, please try again.", false, getApplicationContext());
            Intent intent = getIntent();
            finish();
            startActivity(intent);
        }
        else {
            edit.remove("username");
            edit.remove("password");
            edit.clear();
            Feedback.toast("Oops, something went wrong. Please try again.", false, getApplicationContext());
            Intent intent = getIntent();
            finish();
            startActivity(intent);
        }

    }

    private String getEncryptedPassword(String plaintextPassword) {
        HashMap<String, String> ptPassword = new HashMap<String, String>();
        ptPassword.put("password", plaintextPassword);
        String response = Request.post("encryptPassword", ptPassword, getApplicationContext());
        return response;
    }
}
