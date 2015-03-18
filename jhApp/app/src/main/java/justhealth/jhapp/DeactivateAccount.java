package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.StrictMode;
import android.util.Base64;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Created by stephentate on 04/11/14.
 */
public class DeactivateAccount extends Activity {
    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.deactivate_account);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Deactivate Account");

        populateSpinner();

        Button submit = (Button) findViewById(R.id.deactivateButton);
        submit.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                popUpDeactivate();
            }
        });

        TextView whyKeepData = (TextView) findViewById(R.id.linkKeepYourData);
        whyKeepData.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                startActivity(new Intent(DeactivateAccount.this, whyKeepData.class));
            }
        });
    }

    private void populateSpinner() {

        System.out.println("populateSpinner");
        ArrayList populateSpinner = new ArrayList<String>();

        String response = Request.get("getDeactivateReasons", getApplicationContext());
        System.out.println(response);
        JSONArray appointmentTypes = null;


        try {
            appointmentTypes = new JSONArray(response);
            for (int i = 0; i < appointmentTypes.length(); i++) {
                String app = appointmentTypes.getString(i);
                populateSpinner.add(app);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

        Spinner appointmentType = (Spinner) findViewById(R.id.reasonsDeactivate);
        appointmentType.setAdapter(new ArrayAdapter<String>(this, android.R.layout.simple_spinner_dropdown_item, populateSpinner));
    }

    /**
     * This method makes a post request to the API to deactivate an account. It adds all of the
     * parameters to a HashMap.
     * Once complete, it returns the appropriate message to the user.
     */
    private void popUpDeactivate() {
        final HashMap<String, String> reasons = new HashMap<String, String>();

        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        String password = account.getString("password", null);
        //user account to be deleted
        reasons.put("username", username);

        //checkbox whether all data should be deleted
        CheckBox deleteAll = (CheckBox) findViewById(R.id.checkBox);
        String delete;
        if (deleteAll.isChecked()) {
            delete = "on";
        }
        else {
            delete = "off";
        }
        reasons.put("deletecheckbox", delete);

        //additional comments field
        String comments = ((EditText) findViewById(R.id.comments)).getText().toString();
        reasons.put("comments", comments);

        //reason selected in the spinner
        final Spinner spinnerReason = (Spinner) findViewById((R.id.reasonsDeactivate));
        final String reason = String.valueOf(spinnerReason.getSelectedItem());
        reasons.put("reason", reason);

        new AsyncTask<Void, Void, String>() {

            ProgressDialog progressDialog;
            String response;

            @Override
            protected void onPreExecute() {
                progressDialog = ProgressDialog.show(DeactivateAccount.this, "Loading...", "Deactivating your JustHealth account", true);
                System.out.println(reasons);
            }

            @Override
            protected String doInBackground(Void... v) {
                response = Request.post("deactivateaccount", reasons, getApplicationContext());
                return response;
            }

            @Override
            protected void onPostExecute(String response) {

                if (response.equals("Deleted")) {
                    getSharedPreferences("account", 0).edit().clear().apply();
                    //show the alert to say it is successful
                    Context context = getApplicationContext();
                    CharSequence text = "Sorry to see your leaving. Please be assured that your account has been deactivated and all associated information with it has been deleted.";
                    //Length
                    int duration = Toast.LENGTH_LONG;
                    Toast toast = Toast.makeText(context, text, duration);
                    //Position
                    toast.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL, 0, 100);
                    progressDialog.dismiss();
                    toast.show();
                    finish();

                    Intent goToStart = new Intent(DeactivateAccount.this, Login.class);
                    startActivity(goToStart);
                } else if (response.equals("Kept")) {
                    //show the alert to say it is successful
                    Context context = getApplicationContext();
                    CharSequence text = "Sorry to see your leaving. Please be assured that your account has been deactivated. However, if you want to come back we have kept all of your details on file; it'll be quick and easy to reactivate.";
                    //Length
                    int duration = Toast.LENGTH_LONG;
                    Toast toast = Toast.makeText(context, text, duration);
                    //Position
                    toast.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL, 0, 100);
                    progressDialog.dismiss();
                    toast.show();

                    finish();
                    Intent goToStart = new Intent(DeactivateAccount.this, Login.class);
                    startActivity(goToStart);
                }
            }
        }.execute();
    }


}