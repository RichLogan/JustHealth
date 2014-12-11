package justhealth.jhapp;

import android.annotation.TargetApi;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.Bundle;
import android.os.StrictMode;
import android.util.Base64;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.LinearLayout.LayoutParams;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
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


public class PatientMedication extends Activity {

    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.patient_medication);
        displayPrescriptions(getPrescriptions());
    }

    @TargetApi(Build.VERSION_CODES.KITKAT)
    private JSONArray getPrescriptions() {
        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        String password = account.getString("password", null);

        HashMap<String, String> getPrescriptionsInfo = new HashMap<String, String>();
        getPrescriptionsInfo.put("username", username);

        HttpClient httpclient = new DefaultHttpClient();
        String authentication = username + ":" + password;
        String encodedAuthentication = Base64.encodeToString(authentication.getBytes(), Base64.NO_WRAP);

        HttpPost httppost = new HttpPost("http://raptor.kent.ac.uk:5000/api/getPrescriptions");
        httppost.setHeader("Authorization", "Basic " + encodedAuthentication);

        try {
            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);

            Set<Map.Entry<String, String>> detailsSet = getPrescriptionsInfo.entrySet();
            for (Map.Entry<String, String> string : detailsSet) {
                nameValuePairs.add(new BasicNameValuePair(string.getKey(), string.getValue()));
            }

            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
            HttpResponse response = httpclient.execute(httppost);

            String responseString = EntityUtils.toString(response.getEntity());

            try {
                JSONArray result = new JSONArray(responseString);
                System.out.println(result);
                return result;

            } catch (JSONException e) {
                e.printStackTrace();
            }

        } catch (ClientProtocolException e) {
            //TODO Auto-generated catch block
        } catch (IOException e) {
            //TODO Auto-generated catch block
        } catch (NullPointerException e) {
            //TODO Auto-generated catch block
        }
        return null;
    }

    private void displayPrescriptions(JSONArray prescriptionList) {
        for(int x=0;x<prescriptionList.length();x++) {
            try {
                JSONObject prescription = prescriptionList.getJSONObject(x);
                final String username = prescription.getString("username");
                final String medication = prescription.getString("medication");
                final String dosage = prescription.getString("dosage");
                final String frequency = prescription.getString("frequency");
                final String quantity = prescription.getString("quantity");
                final String dosageunit = prescription.getString("dosageunit");
                final String frequencyunit = prescription.getString("frequencyunit");
                final String startdate = prescription.getString("startdate");
                final String enddate = prescription.getString("enddate");
                final String repeat = prescription.getString("repeat");
                final String stockleft = prescription.getString("stockleft");
                final String prerequisite = prescription.getString("prerequisite");
                final String dosageform = prescription.getString("dosageform");

                //Create a button
                Button prescriptionButton = new Button(this);
                String prescriptionString = medication + ":\n" + "Take " + quantity + " x " + dosage + " " + dosageunit + " " + dosageform + "(s)\n" + frequency + " x " + "a " + frequencyunit;
                prescriptionButton.setText(prescriptionString);

                //Add button to view
                LinearLayout ll = (LinearLayout)findViewById(R.id.prescriptionButtons);
                ll.addView(prescriptionButton,new LayoutParams(LayoutParams.MATCH_PARENT,LayoutParams.MATCH_PARENT));

                LinearLayout.LayoutParams center = (LinearLayout.LayoutParams)prescriptionButton.getLayoutParams();
                center.gravity = Gravity.CENTER;
                prescriptionButton.setLayoutParams(center);

                prescriptionButton.setOnClickListener(new View.OnClickListener() {
                    public void onClick(View v) {
                        AlertDialog.Builder alert = new AlertDialog.Builder(PatientMedication.this);
                        alert.setTitle(medication + " (" + dosage + dosageunit + ")");
                        alert.setMessage("Start Date: " + startdate + "\nEnd Date: " + enddate + "\nExtra Info: " + prerequisite + "\nRepeat: " + repeat);
                        alert.setNegativeButton("Got it!", new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int whichButton) {
                                // Cancelled.
                            }
                        });
                    alert.show();
                    }
                });
            }
            catch (JSONException e) {
                System.out.print(e.getStackTrace());
            }
        }
    }
}