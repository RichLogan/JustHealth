package justhealth.jhapp;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
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
        populateSpinner();

        Button submit = (Button) findViewById(R.id.deactivateButton);
        submit.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                popUpDeactivate();
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

    private void popUpDeactivate() {
        HashMap<String, String> reasons = new HashMap<String, String>();

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

        String response = Request.post("deactivateaccount", reasons, this);
        if(response.equals("Deleted")) {
            getSharedPreferences("account", 0).edit().clear().commit();

            //show the alert to say it is successful
            Context context = getApplicationContext();
            CharSequence text = "Sorry to see your leaving. Please be assured that your account has been deactivated and all associated information with it has been deleted.";
            //Length
            int duration = Toast.LENGTH_LONG;
            Toast toast = Toast.makeText(context, text, duration);
            //Position
            toast.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL, 0, 100);
            toast.show();
            finish();

            Intent goToStart = new Intent(this, Login.class);
            startActivity(goToStart);
        }
        else if(response.equals("Kept")) {
            //show the alert to say it is successful
            Context context = getApplicationContext();
            CharSequence text = "Sorry to see your leaving. Please be assured that your account has been deactivated. However, if you want to come back we have kept all of your details on file; it'll be quick and easy to reactivate.";
            //Length
            int duration = Toast.LENGTH_LONG;
            Toast toast = Toast.makeText(context, text, duration);
            //Position
            toast.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL, 0, 100);
            toast.show();

            finish();
            Intent goToStart = new Intent(this, Login.class);
            startActivity(goToStart);
        }
    }


}