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
//        getPatientMedication();
//    }
//
//
//    private void getPatientMedication(JSONArray outgoing) {
//        TableLayout searchTable = (TableLayout) findViewById(R.id.patient_medication);
//
//        TableRow outgoingHeadRow = new TableRow(this);
//        outgoingHeadRow.setBackgroundColor(getResources().getColor(R.color.header));
//        TextView incomingConnections = new TextView(this);
//        incomingConnections.setText("Medication");
//        incomingConnections.setTextColor(Color.WHITE);
//
//        outgoingHeadRow.addView(incomingConnections);
//        searchTable.addView(outgoingHeadRow, 1);
//        //update row of table
//        rowOfTable += 2;
//
//    }
//
//}
//
//
//
//
