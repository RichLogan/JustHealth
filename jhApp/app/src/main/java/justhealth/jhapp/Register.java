package justhealth.jhapp;

import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.*;
import android.content.Intent;

import java.util.Set;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;


// Post Requests
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.HttpResponse;

import java.io.IOException;
import java.util.Map;

import android.os.StrictMode;

import org.apache.http.client.ClientProtocolException;
import org.apache.http.util.EntityUtils;

public class Register extends ActionBarActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.register);

        Button registerButton = (Button) findViewById(R.id.register);
        registerButton = (Button) findViewById(R.id.register);
        registerButton.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        sendRegister();
                    }
                }
        );

//        TextView termsAndConditions = (TextView)findViewById(R.id.tsandcs);
//        termsAndConditions.setOnClickListener(
//               new View.OnClickListener() {
//                   public void onClick(View view) {
//                       startActivity(new Intent(Register.this, TermsAndConditions.class));
//                   }
//               }
//        );

        TextView forgotPassword = (TextView) findViewById(R.id.link_to_forgot_password);
        forgotPassword.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(Register.this, ForgotPassword.class));
                    }
                }
        );
    }

    private void sendRegister() {

        HashMap<String, String> details = new HashMap<String, String>();

        //Text Boxes
        details.put("username", ((EditText) findViewById(R.id.username)).getText().toString());
        details.put("firstname", ((EditText) findViewById(R.id.firstName)).getText().toString());
        details.put("surname", ((EditText) findViewById(R.id.surname)).getText().toString());
        details.put("dob", ((EditText) findViewById(R.id.dob)).getText().toString());
        details.put("email", ((EditText) findViewById(R.id.email)).getText().toString());

        //Gender
        Boolean ismale = null;
        int id = ((RadioGroup) findViewById(R.id.sex)).getCheckedRadioButtonId();
        if (id == R.id.male) {
            ismale = true;
        } else if (id == R.id.female) {
            ismale = false;
        }
        details.put("ismale", ismale.toString());

        //Account Type
        final Spinner accountTypeSpinner = (Spinner) findViewById((R.id.accountType));
        final String accountType = String.valueOf(accountTypeSpinner.getSelectedItem());
        details.put("accounttype", accountType.toLowerCase());

        //Password
        String password = ((EditText) findViewById(R.id.password)).getText().toString();
        String confirmPassword = ((EditText) findViewById(R.id.confirmPassword)).getText().toString();

        if (((CheckBox) findViewById(R.id.tsandcs)).isChecked()) {
            System.out.println("come on");
            details.put("password", password);
            details.put("confirmpassword", confirmPassword);

            //TODO: set the terms and conditions properly
            details.put("terms", "on");

            post(details);
        } else {
            //Ts and cs not accepted
        }
    }

    public void post(HashMap<String, String> details) {
        // Create a new HttpClient and Post Header
        HttpClient httpclient = new DefaultHttpClient();
        HttpPost httppost = new HttpPost("http://raptor.kent.ac.uk:5000/api/registerUser");

        try {
            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);

            Set<Map.Entry<String, String>> detailsSet = details.entrySet();
            for (Map.Entry<String, String> s : detailsSet) {
                System.out.println(s);
                nameValuePairs.add(new BasicNameValuePair(s.getKey(), s.getValue()));
            }

            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
            HttpResponse response = httpclient.execute(httppost);
            System.out.println(response.getStatusLine());

            //HttpEntity responseEntity = response.getEntity();
            //InputStream is = responseEntity.getContent();
            //System.out.println(is.toString());
            String responseStr = EntityUtils.toString(response.getEntity());
            System.out.println(responseStr);

        } catch (ClientProtocolException e) {
            // TODO Auto-generated catch block
        } catch (IOException e) {
            // TODO Auto-generated catch block
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.register, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    //validation on password and confirm password
    public boolean isPasswordValid(String password, String confirmPassword) {
        boolean status = false;
        if (confirmPassword != null && password != null) {
            if (password.equals(confirmPassword)) {
                status = true;
            }
        }
        return status;
    }
}

