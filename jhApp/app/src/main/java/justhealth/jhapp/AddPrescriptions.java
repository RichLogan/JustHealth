
/**
 * Created by charlottehutchinson on 11/12/14.
 */


package justhealth.jhapp;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.StrictMode;
import android.widget.EditText;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class AddPrescriptions extends Activity {

    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.carer_add_prescription);
    }

    private void addPrescriptions() {

        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        String password = account.getString("password", null);

        HashMap<String, String> details = new HashMap<String, String>();

        //Text Boxes
        details.put("creator", username);
        details.put("medication", ((EditText) findViewById(R.id.medication)).getText().toString());
        details.put("Quantity", ((EditText) findViewById(R.id.quantity)).getText().toString());
        details.put("Dosage", ((EditText) findViewById(R.id.dosageValue)).getText().toString());
        details.put("Dosage Unit", ((EditText) findViewById(R.id.DosageUnit)).getText().toString());
        details.put("frequency", ((EditText) findViewById(R.id.frequency)).getText().toString());
        details.put("frequency Unit", ((EditText) findViewById(R.id.frequencyUnit)).getText().toString());
        details.put("Type", ((EditText) findViewById(R.id.Type)).getText().toString());
        details.put("startdate", ((EditText) findViewById(R.id.startDate)).getText().toString());
        details.put("enddate", ((EditText) findViewById(R.id.endDate)).getText().toString());
        details.put("endtime", ((EditText) findViewById(R.id.endTime)).getText().toString());
        details.put("stock", ((EditText) findViewById(R.id.StockLeft)).getText().toString());
        details.put("Observations", ((EditText) findViewById(R.id.Observations)).getText().toString());

    }

    private String addPrescriptions(String username) {
        HashMap<String, String> parameters = new HashMap<String, String>();
        parameters.put("username", username);

        String response = PostRequest.post("addPrescriptions", parameters);
        try {
            JSONObject accountDetails = new JSONObject(response);
            String accountType  = accountDetails.getString("accounttype");
            return accountType;
        }
        catch (JSONException e) {
            System.out.println(e.getStackTrace());
        }
        return null;
    }



}








