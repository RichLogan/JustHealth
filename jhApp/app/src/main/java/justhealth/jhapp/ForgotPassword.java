package justhealth.jhapp;

import android.app.Activity;
import android.os.Bundle;
import android.os.StrictMode;
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
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class ForgotPassword extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.forgot_password);

        Button submitButton = (Button) findViewById(R.id.submit);
        submitButton.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        getDetails();
                    }
                }
        );
    }

    private void getDetails() {
        HashMap<String, String> details = new HashMap<String, String>();
        details.put("username", ((EditText) findViewById(R.id.loginUsername)).getText().toString());
        details.put("confirmemail", ((EditText) findViewById(R.id.email)).getText().toString());
        details.put("newpassword", ((EditText) findViewById(R.id.newPassword)).getText().toString());
        details.put("confirmnewpassword", ((EditText) findViewById(R.id.confirmNewPassword)).getText().toString());
        details.put("confirmdob", ((EditText) findViewById(R.id.dob)).getText().toString());
        post(details);
    }

    public void post(HashMap<String, String> details) {
        HttpClient httpclient = new DefaultHttpClient();
        HttpPost httppost = new HttpPost("http://raptor.kent.ac.uk:5000/api/resetpassword");

        try {
            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);

            Set<Map.Entry<String, String>> detailsSet = details.entrySet();
            for (Map.Entry<String, String> s : detailsSet) {
                System.out.println(s);
                nameValuePairs.add(new BasicNameValuePair(s.getKey(), s.getValue()));
            }

            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
            HttpResponse response = httpclient.execute(httppost);
            System.out.println(response.getStatusLine());

            //HttpEntity responseEntity = response.getEntity();
            //InputStream is = responseEntity.getContent();
            //System.out.println(is.toString());
            String responseStr = EntityUtils.toString(response.getEntity());
            System.out.println(responseStr);

        } catch (ClientProtocolException e) {
            // TODO Auto-generated catch block
        } catch (IOException e) {
            // TODO Auto-generated catch block
        }
    }
}