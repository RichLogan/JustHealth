///**
//* Created by charlottehutchinson on 10/12/14.
//*/
//
//package justhealth.jhapp;
//    import android.content.SharedPreferences;
//    import android.os.Bundle;
//    import android.os.StrictMode;
//    import android.support.v7.app.ActionBarActivity;
//    import android.util.Base64;
//    import android.widget.EditText;
//
//    import org.apache.http.HttpResponse;
//    import org.apache.http.NameValuePair;
//    import org.apache.http.client.ClientProtocolException;
//    import org.apache.http.client.HttpClient;
//    import org.apache.http.client.entity.UrlEncodedFormEntity;
//    import org.apache.http.client.methods.HttpPost;
//    import org.apache.http.impl.client.DefaultHttpClient;
//    import org.apache.http.message.BasicNameValuePair;
//    import org.apache.http.util.EntityUtils;
//
//    import java.io.IOException;
//    import java.io.UnsupportedEncodingException;
//    import java.util.ArrayList;
//    import java.util.HashMap;
//    import java.util.List;
//    import java.util.Map;
//    import java.util.Set;
//
//public class Add_Prescriptions {
//
//        protected void onCreate(Bundle savedInstanceState) {
//            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
//            StrictMode.setThreadPolicy(policy);
//
//            super.onCreate(savedInstanceState);
//            setContentView(R.layout.carer_add_prescription);
//
//        }
//
//
//        private void AddPrescriptions() {
//
//            SharedPreferences account = getSharedPreferences("account", 0);
//            String username = account.getString("username", null);
//            String password = account.getString("password", null);
//
//            HashMap<String, String> details = new HashMap<String, String>();
//
//            //Text Boxes
//            details.put("creator", username);
//            details.put("medication", ((EditText) findViewById(R.id.medication)).getText().toString());
//            details.put("Quantity", ((EditText) findViewById(R.id.quantity)).getText().toString());
//            details.put("Dosage", ((EditText) findViewById(R.id.dosageValue)).getText().toString());
//            details.put("Dosage Unit", ((EditText) findViewById(R.id.DosageUnit)).getText().toString());
//            details.put("frequency", ((EditText) findViewById(R.id.frequency)).getText().toString());
//            details.put("frequency Unit", ((EditText) findViewById(R.id.frequencyUnit)).getText().toString());
//            details.put("Type", ((EditText) findViewById(R.id.Type)).getText().toString());
//            details.put("startdate", ((EditText) findViewById(R.id.startDate)).getText().toString());
//            details.put("enddate", ((EditText) findViewById(R.id.endDate)).getText().toString());
//            details.put("endtime", ((EditText) findViewById(R.id.endTime)).getText().toString());
//            details.put("stock", ((EditText) findViewById(R.id.StockLeft)).getText().toString());
//            details.put("Observations", ((EditText) findViewById(R.id.Observations)).getText().toString());
//
//
//            HttpClient httpclient = new DefaultHttpClient();
//            String authentication = username + ":" + password;
//            String encodedAuthentication = Base64.encodeToString(authentication.getBytes(), Base64.NO_WRAP);
//
//            HttpPost httppost = new HttpPost("http://raptor.kent.ac.uk:5000/api/addPrescriptions");
//            httppost.setHeader("Authorization", "Basic " + encodedAuthentication);
//            try {
//                List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);
//
//                Set<Map.Entry<String, String>> detailsSet = details.entrySet();
//                for (Map.Entry<String, String> string : detailsSet) {
//                    nameValuePairs.add(new BasicNameValuePair(string.getKey(), string.getValue()));
//                    System.out.println(nameValuePairs);
//                }
//
//                //pass the list to the post request
//                httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
//                System.out.println(httppost);
//                HttpResponse response = httpclient.execute(httppost);
//                String responseString = EntityUtils.toString(response.getEntity());
//
//                System.out.println(responseString);
//
//            } catch (ClientProtocolException e) {
//                e.printStackTrace();
//            } catch (UnsupportedEncodingException e) {
//                e.printStackTrace();
//            } catch (IOException e) {
//                e.printStackTrace();
//            }
//
//        }
//    }
//
