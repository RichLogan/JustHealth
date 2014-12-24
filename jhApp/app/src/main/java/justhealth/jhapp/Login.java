package justhealth.jhapp;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class Login extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);

        TextView register = (TextView) findViewById(R.id.link_to_forgot_password);
        register.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(Login.this, ForgotPassword.class));
                    }
                }
        );

        TextView forgotPassword = (TextView) findViewById(R.id.link_to_register);
        forgotPassword.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(Login.this, Register.class));
                    }
                }
        );

        TextView terms = (TextView) findViewById(R.id.link_to_terms);
        terms.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(Login.this, TermsAndConditions.class));
                    }
                }
        );

        Button loginButton = (Button) findViewById(R.id.login);
        loginButton = (Button) findViewById(R.id.login);
        loginButton.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        requestLogin();
                    }
                }
        );
    }

    private void requestLogin() {
        HashMap<String, String> loginInformation = new HashMap<String, String>();
        loginInformation.put("username", ((EditText) findViewById(R.id.loginUsername)).getText().toString());
        loginInformation.put("password", ((EditText) findViewById(R.id.loginPassword)).getText().toString());

        String response = PostRequest.post("authenticate", loginInformation);
        if (response.equals("Authenticated")) {
            SharedPreferences account = getSharedPreferences("account", 0);
            SharedPreferences.Editor edit = account.edit();
            edit.putString("username", loginInformation.get("username"));
            edit.putString("password", loginInformation.get("password"));
            edit.commit();

            if (getAccountType(loginInformation.get("username")).equals("Patient")) {
                startActivity(new Intent(Login.this, HomePatient.class));
            } else if (getAccountType(loginInformation.get("username")).equals("Carer")) {
                startActivity(new Intent(Login.this, HomeCarer.class));
            } else {
            }
        }
        else {
            Feedback.toast(response, false, getApplicationContext());
        }
    }

    private String getAccountType(String username) {
        HashMap<String, String> parameters = new HashMap<String, String>();
        parameters.put("username", username);

        String response = PostRequest.post("getAccountInfo", parameters);
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
}