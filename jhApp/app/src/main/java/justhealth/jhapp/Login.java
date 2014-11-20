package justhealth.jhapp;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.StrictMode;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.LinearLayout;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class Login extends ActionBarActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);

        TextView register = (TextView)findViewById(R.id.link_to_forgot_password);
        register.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(Login.this, ForgotPassword.class));
                    }
                }
        );

        TextView forgotPassword = (TextView)findViewById(R.id.link_to_register);
        forgotPassword.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(Login.this, Register.class));
                    }
                }
        );

        TextView terms = (TextView)findViewById(R.id.link_to_terms);
        terms.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(Login.this, TermsAndConditions.class));
                    }
                }
        );

        Button loginButton = (Button)findViewById(R.id.login);
        loginButton = (Button) findViewById(R.id.login);
        loginButton.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        requestLogin();
                        startActivity(new Intent(Login.this, HomePatient.class));
                    }
                }
        );
    }

    private void requestLogin(){
        HashMap<String, String> loginInformation = new HashMap<String, String>();

        //add username to HashMap
        loginInformation.put("username", ((EditText) findViewById(R.id.loginUsername)).getText().toString());

        //add password to HashMap
        loginInformation.put("password", ((EditText) findViewById(R.id.loginPassword)).getText().toString());

        //Create new HttpClient and Post Header
        HttpClient httpclient = new DefaultHttpClient();
        HttpPost httppost = new HttpPost("http://raptor.kent.ac.uk:5000/api/authenticate");

        //assigns the HashMap to list, for post request encoding
        try {
            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);

            Set<Map.Entry<String,String>> detailsSet = loginInformation.entrySet();
            for (Map.Entry<String, String> string : detailsSet) {
                nameValuePairs.add(new BasicNameValuePair(string.getKey(), string.getValue()));
            }

            //pass the list to the post request
            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
            HttpResponse response = httpclient.execute(httppost);

            //Check Result
            String responseStr = EntityUtils.toString(response.getEntity());
            if (responseStr.equals("Authenticated")) {
                SharedPreferences account = getSharedPreferences("account", 0);
                SharedPreferences.Editor edit = account.edit();
                edit.putString("username", loginInformation.get("username"));
                edit.putString("password", loginInformation.get("password"));
                edit.commit();

                String username = account.getString("username", null);
                //todo remove this line
                System.out.println("login, added username to shared preferences: " + username);
            }
            else {
                System.out.println("Failed:");
                System.out.println(responseStr);

                //Check if the Layout already exists
                LinearLayout alert = (LinearLayout)findViewById(R.id.alertMessage);
                if(alert == null){
                    //Insert the alert message
                    LinearLayout insertAlert = (LinearLayout)findViewById(R.id.insertAlert);
                    View insertAlertView = getLayoutInflater().inflate(R.layout.alert_message, insertAlert, false);
                    insertAlert.addView(insertAlertView);
                }

                TextView myTextView = (TextView) findViewById(R.id.alertText);
                myTextView.setText(responseStr);
            }
        }
        catch (ClientProtocolException e) {
            //TODO Auto-generated catch block
        }
        catch (IOException e) {
            //TODO Auto-generated catch block
        }

    }
}