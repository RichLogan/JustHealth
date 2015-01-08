package justhealth.jhapp;

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

public class PostRequest {

    public static String post(String url, HashMap<String, String> parameters) {

        HttpClient httpClient = new DefaultHttpClient();
        HttpPost httppost = new HttpPost("http://raptor.kent.ac.uk:5000/api/" + url);

        //Authentication
        //SharedPreferences account = getSharedPreferences("account", 0);
        //String username = account.getString("username", null);
        //String password = account.getString("password", null);

        //String authentication = username + ":" + password;
        //String encodedAuthentication = Base64.encodeToString(authentication.getBytes(), Base64.NO_WRAP);
        //httppost.setHeader("Authorization", "Basic " + encodedAuthentication);

        try {
            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);
            Set<Map.Entry<String, String>> detailsSet = parameters.entrySet();
            for (Map.Entry<String, String> string : detailsSet) {
                nameValuePairs.add(new BasicNameValuePair(string.getKey(), string.getValue()));
            }
            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
            HttpResponse response = httpClient.execute(httppost);

            String responseString = EntityUtils.toString(response.getEntity());

            return responseString;
        }
        catch (ClientProtocolException e) {
            //TODO Auto-generated catch block
        } catch (IOException e) {
            //TODO Auto-generated catch block
        } catch (NullPointerException e) {
            //TODO Auto-generated catch block
        }
        return null;
    }
}