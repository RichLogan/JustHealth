package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
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

    //The username of the user that has tried to login
    private String username;
    //The password that the have logged in with
    private String expiredPassword;
    //The account type of the user that has logged in (Patient/Carer)
    private String accountType;

    /**
     * This method is invoked when the page is first loaded. Sets the correct xml layout and shows
     * the action bar. Assigns the class variables from what is passed with the intent. OnclickListener
     * for the password reset button.
     *
     * @param savedInstanceState a bundle if the state of the application was to be saved.
     */
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

    /**
     * Adds the newpassword and confirmnewpassword to a HashMap and makes the post request to the
     * JustHealth API.
     * Subsequently, resets the SharedPreferences values and feedbacks to the user.
     */
    private void sendResetExpiredPassword() {
        final HashMap<String, String> details = new HashMap<String, String>();

        //Text Boxes
        details.put("username", username);

        //check the passwords match before adding to the HashMap
        final String password = ((EditText) findViewById(R.id.newPassword)).getText().toString();
        String confirm = ((EditText) findViewById(R.id.confirmNewPassword)).getText().toString();
        if (password.equals(confirm)) {
            //even though the if statement covers this they still need to both be sent to not break back-end validation
            details.put("newpassword", password);
            details.put("confirmnewpassword", confirm);
        } else {
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
        edit.putString("accountType", accountType);
        edit.apply();

        Feedback.toast("Password changed successfully.", true, getApplicationContext());
        new AsyncTask<Void, Void, String>() {

            ProgressDialog progressDialog;
            String response;

            /**
             * Shows the loading dialog
             */
            @Override
            protected void onPreExecute() {
                progressDialog = ProgressDialog.show(ExpiredPassword.this, "Loading...", "Resetting your password", true);
            }

            /**
             * Makes the post request to the JustHealth API off of the main thread
             * @param v Shows that there are no parameters passed to the method
             * @return Returns the response from the JustHealth API
             */
            @Override
            protected String doInBackground(Void... v) {
                response = Request.post("expiredResetPassword", details, getApplicationContext());
                return response;
            }

            /**
             * Dismisses the loading dialog.
             * Sets SharedPreferences and redirects  the user to the correct home page.
             * @param response
             */
            @Override
            protected void onPostExecute(String response) {
                progressDialog.dismiss();

                System.out.println(response);

                if (response.equals("True")) {
                    //overwriting with new encrypted password
                    String encryptedPassword = getEncryptedPassword(password);
                    SharedPreferences account = getSharedPreferences("account", 0);
                    SharedPreferences.Editor edit = account.edit();
                    edit.putString("password", encryptedPassword);
                    edit.putString("accountType", accountType);
                    edit.apply();
                    finish();
                    startActivity(new Intent(ExpiredPassword.this, Main.class));
                } else if (response.equals("Unmatched")) {
                    SharedPreferences account = getSharedPreferences("account", 0);
                    SharedPreferences.Editor edit = account.edit();
                    edit.remove("username");
                    edit.remove("password");
                    edit.remove("accountType");
                    edit.clear();
                    Feedback.toast("The two passwords you entered did not match, please try again.", false, getApplicationContext());
                    Intent intent = getIntent();
                    finish();
                    startActivity(intent);
                } else {
                    SharedPreferences account = getSharedPreferences("account", 0);
                    SharedPreferences.Editor edit = account.edit();
                    edit.remove("username");
                    edit.remove("password");
                    edit.remove("accountType");
                    edit.clear();
                    Feedback.toast("Oops, something went wrong. Please try again.", false, getApplicationContext());
                    Intent intent = getIntent();
                    finish();
                    startActivity(intent);
                }

            }
        }.execute();
    }

    /**
     * Queries the JustHealth API to retrieve the encrypted password
     * @param plaintextPassword The plaintext password that the user types into the reset box
     * @return The encrypted password
     */
    private String getEncryptedPassword(String plaintextPassword) {
        HashMap<String, String> ptPassword = new HashMap<String, String>();
        ptPassword.put("password", plaintextPassword);
        String response = Request.post("encryptPassword", ptPassword, getApplicationContext());
        return response;
    }
}
