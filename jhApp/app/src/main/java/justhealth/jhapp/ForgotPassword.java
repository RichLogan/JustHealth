package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.util.HashMap;

public class ForgotPassword extends Activity {

    /**
     * This method runs when the page is first loaded.
     * Sets the correct xml layout and sets the action bar.
     * OnClickListener on the submit button of the page, runs the getDetails method.
     *
     * @param savedInstanceState a bundle if the state of the application was to be saved.
     */
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

    /**
     * Gets the details from the EditText boxes and assigns them to a HashMap.
     */
    private void getDetails() {
        HashMap<String, String> details = new HashMap<String, String>();
        details.put("username", ((EditText) findViewById(R.id.loginUsername)).getText().toString());
        details.put("confirmemail", ((EditText) findViewById(R.id.email)).getText().toString());
        details.put("newpassword", ((EditText) findViewById(R.id.newPassword)).getText().toString());
        details.put("confirmnewpassword", ((EditText) findViewById(R.id.confirmNewPassword)).getText().toString());
        details.put("confirmdob", ((EditText) findViewById(R.id.dob)).getText().toString());
        post(details);
    }

    public void post(final HashMap<String, String> details) {
        new AsyncTask<Void, Void, String>() {

            ProgressDialog progressDialog;
            String responseString;

            /**
             * Sets the loading spinner to display to the user
             */
            @Override
            protected void onPreExecute() {
                progressDialog = ProgressDialog.show(ForgotPassword.this, "Loading...", "Just resetting your password", true);
                System.out.println(details);
            }

            /**
             * Makes the post request to the JustHealth API
             * @param v Shows that no parameters are being passed to the method.
             * @return The response from the JustHealth API after the post request.
             */
            @Override
            protected String doInBackground(Void... v) {
                responseString = Request.post("resetpassword", details, getApplicationContext());
                return responseString;
            }

            /**
             * Feedback the response to the user, using a toast.
             * @param response The response from the JustHealth API.
             */
            @Override
            protected void onPostExecute(String response) {
                progressDialog.dismiss();


                if (!response.equals("True")) {
                    Feedback.toast(response, false, getApplicationContext());
                } else {
                    Feedback.toast("Your password has been successfully reset", true, getApplicationContext());
                    finish();
                    startActivity(new Intent(ForgotPassword.this, Login.class));
                }
            }
        }.execute();
    }
}