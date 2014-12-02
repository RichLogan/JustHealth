//package justhealth.jhapp;
//
//import android.annotation.TargetApi;
//import android.app.AlertDialog;
//import android.content.DialogInterface;
//import android.content.Intent;
//import android.content.SharedPreferences;
//import android.graphics.Color;
//import android.os.Build;
//import android.os.Bundle;
//import android.os.StrictMode;
//import android.support.v7.app.ActionBarActivity;
//import android.text.Editable;
//import android.text.InputFilter;
//import android.text.InputType;
//import android.util.Base64;
//import android.view.Gravity;
//import android.view.View;
//import android.view.ViewGroup;
//import android.widget.Button;
//import android.widget.EditText;
//import android.widget.ImageButton;
//import android.widget.LinearLayout;
//import android.widget.PopupWindow;
//import android.widget.TableLayout;
//import android.widget.TableRow;
//import android.widget.TextView;
//
//import org.apache.http.HttpResponse;
//import org.apache.http.NameValuePair;
//import org.apache.http.client.ClientProtocolException;
//import org.apache.http.client.HttpClient;
//import org.apache.http.client.entity.UrlEncodedFormEntity;
//import org.apache.http.client.methods.HttpPost;
//import org.apache.http.impl.client.DefaultHttpClient;
//import org.apache.http.message.BasicNameValuePair;
//import org.apache.http.util.EntityUtils;
//import org.json.JSONArray;
//import org.json.JSONException;
//import org.json.JSONObject;
//
//import java.io.IOException;
//import java.util.ArrayList;
//import java.util.HashMap;
//import java.util.List;
//import java.util.Map;
//import java.util.Set;
//
///**
//* Created by charlottehutchinson on 01/12/14.
//*/
//
//public class PatientMedication extends ActionBarActivity {
//
//
//    private int rowOfTable = 0;
//
//    protected void onCreate(Bundle savedInstanceState) {
//        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
//        StrictMode.setThreadPolicy(policy);
//
//        super.onCreate(savedInstanceState);
//        setContentView(R.layout.patient_medication);
//        getPrescriptions();
//    }
//
//
//    @TargetApi(Build.VERSION_CODES.KITKAT)
//    private void getConnections() {
//        HashMap<String, String> getPrescriptionsInfo = new HashMap<String, String>();
//
//        //this is adding the username as null - INCORRECT
//        SharedPreferences account = getSharedPreferences("account", 0);
//        String username = account.getString("username", null);
//        String password = account.getString("password", null);
//
//        //add search to HashMap
//        getPrescriptionsInfo.put("username", username);
//
//        //Create new HttpClient and Post Header
//        HttpClient httpclient = new DefaultHttpClient();
//        String authentication = username + ":" + password;
//        String encodedAuthentication = Base64.encodeToString(authentication.getBytes(), Base64.NO_WRAP);
//
//        HttpPost httppost = new HttpPost("http://raptor.kent.ac.uk:5000/api/getPrescriptions");
//        httppost.setHeader("Authorization", "Basic " + encodedAuthentication);
//        System.out.println(encodedAuthentication);
//        //assigns the HashMap to list, for post request encoding
//        try {
//            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);
//
//            Set<Map.Entry<String, String>> detailsSet = getPrescriptionsInfo.entrySet();
//            for (Map.Entry<String, String> string : detailsSet) {
//                nameValuePairs.add(new BasicNameValuePair(string.getKey(), string.getValue()));
//            }
//
//            //pass the list to the post request
//            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
//            HttpResponse response = httpclient.execute(httppost);
//
//            String responseString = EntityUtils.toString(response.getEntity());
//            System.out.print(responseString);
//            JSONArray prescriptions = null;
//
//            try {
//                queryReturn = new JSONObject(responseString);
//                System.out.println(queryReturn);
//                String outgoingString = queryReturn.getString("Prescriptions");
//                prescriptions = new JSONArray(outgoingString);
//
//            } catch (JSONException e) {
//                e.printStackTrace();
//            }
//
//            System.out.print(queryReturn);
//            printprescriptions(prescriptions);
//
//        } catch (ClientProtocolException e) {
//            //TODO Auto-generated catch block
//        } catch (IOException e) {
//            //TODO Auto-generated catch block
//        } catch (NullPointerException e) {
//            //TODO Auto-generated catch block
//        }
//    }
//
//// button to list medication per patient
//
//
//
//
//
//
//
////        protected void onCreate(Bundle savedInstanceState) {
////            super.onCreate(savedInstanceState);
////            setContentView(R.layout. patient_medication);
////
////            Button connections = (Button) findViewById();
////            connections.setOnClickListener(
////                    new Button.OnClickListener() {
////                        public void onClick(View view) {
////                            startActivity(new Intent(AlertDialog.this));
////                        }
////                    }
////            );
////        }
////    }
//
////onlick on medication, alert box to show more details
////private void medicationdeatils() {
////
////    AlertDialog.Builder alert = new AlertDialog.Builder(this);
////
////    alert.setTitle("Your Medication");
////    alert.setMessage(message);
////
////
////    alert.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
////        public void onClick(DialogInterface dialog, int whichButton) {
////            // Cancelled.
////        }
////    });
////
////    alert.show();
////}
//
//
//}
//
//
//
