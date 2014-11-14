package justhealth.jhapp;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.StrictMode;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Created by Stephen Tate on 14/11/2014.
 */
public class Search extends ActionBarActivity {

    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.search);

        //check for the search button being pressed
        Button search = (Button) findViewById(R.id.searchButton);
        search.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        searchName();
                    }
                }
        );

    }

    private void searchName() {
        HashMap<String, String> searchInformation = new HashMap<String, String>();

        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);

        //add search to HashMap
        searchInformation.put("username", username);
        searchInformation.put("searchTerm", ((EditText) findViewById(R.id.searchField)).getText().toString());

        //Create new HttpClient and Post Header
        HttpClient httpclient = new DefaultHttpClient();
        HttpPost httppost = new HttpPost("http://raptor.kent.ac.uk:5000/api/searchPatientCarer");

        //assigns the HashMap to list, for post request encoding
        try {
            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);

            Set<Map.Entry<String, String>> detailsSet = searchInformation.entrySet();
            for (Map.Entry<String, String> string : detailsSet) {
                nameValuePairs.add(new BasicNameValuePair(string.getKey(), string.getValue()));
            }

            //pass the list to the post request
            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
            HttpResponse response = httpclient.execute(httppost);
        } catch (ClientProtocolException e) {
            //TODO Auto-generated catch block
        } catch (IOException e) {
            //TODO Auto-generated catch block
        }
    }
}
