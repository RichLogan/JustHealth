package justhealth.jhapp;

import android.content.Context;
import android.content.SharedPreferences;
import android.util.Base64;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

import java.io.IOException;
import java.net.URI;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Helper class containing static methods for communication with the JustHealth server.
 * Primarily provides access to POST and GET requests.
 */
public class Request {

    // The URL and port of the JustHealth Server
    private static String SERVER_URL = "http://raptor.kent.ac.uk:5000";

    /**
     * Method to get the active server's URL (protocol, host, port)
     * @return Full URL as String
     */
    public static String getServerURL() {
        return SERVER_URL;
    }

    /**
     * Provides POST request communication to JustHealth's public facing API located at /api
     * Takes credentials for the server from the logged in user's details
     * @param url The API function url for the request, not the full URL. e.g http://server/api/{THIS_URL_HERE}
     * @param parameters The parameters for the post request in the form of a HashMap<String, String> corresponding to the key/value pairs the API function expects.
     * @param context The current application context, usually provided by getApplicationContext(). Allows access to SharedPreferences.
     * @return The result of the API call as a String. This is most often JSON but should be decoded by the calling functionality.
     */
    public static String post(String url, HashMap<String, String> parameters, Context context) {
        // Create HTTP Objects
        HttpClient httpClient = new DefaultHttpClient();
        HttpPost httppost = new HttpPost(SERVER_URL + "/api/" + url);

        // Add Authentication
        SharedPreferences account = context.getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        String password = account.getString("password", null);
        String authentication = username + ":" + password;
        String encodedAuthentication = Base64.encodeToString(authentication.getBytes(), Base64.NO_WRAP);
        httppost.setHeader("Authorization", "Basic " + encodedAuthentication);

        // Convert Parameters to URL Encoded name/value pairs
        try {
            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);
            Set<Map.Entry<String, String>> detailsSet = parameters.entrySet();
            for (Map.Entry<String, String> string : detailsSet) {
                nameValuePairs.add(new BasicNameValuePair(string.getKey(), string.getValue()));
            }
            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
            HttpResponse response = httpClient.execute(httppost);

            return EntityUtils.toString(response.getEntity());
        }
        catch (Exception e) {
            Feedback.toast("Cannot connect to Server", false, context);
            return null;
        }
    }

    /**
     * Provides GET request communication to JustHealth's public facing API located at /api when no parameters need to be passed
     * @param url The API function url for the request, not the full URL. e.g http://server/api/{THIS_URL_HERE}
     * @param context The current application context, usually provided by getApplicationContext(). Allows access to SharedPreferences.
     * @return The result of the API call as a String. This is most often JSON but should be decoded by the calling functionality.
     */
    public static String get(String url, Context context) {
        HttpClient httpClient = new DefaultHttpClient();
        HttpGet httpget = new HttpGet();

        //Authentication
        SharedPreferences account = context.getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        String password = account.getString("password", null);
        String authentication = username + ":" + password;
        String encodedAuthentication = Base64.encodeToString(authentication.getBytes(), Base64.NO_WRAP);
        httpget.setHeader("Authorization", "Basic " + encodedAuthentication);

        try {
            URI website = new URI(SERVER_URL + "/api/" + url);
            httpget.setURI(website);
        } catch (Exception e) {
            System.out.println("Failed");
        }

        try {
            HttpResponse response = httpClient.execute(httpget);
            return EntityUtils.toString(response.getEntity());
        }
        catch (ClientProtocolException e) {
            //TODO Auto-generated catch block
        } catch (IOException e) {
            //TODO Auto-generated catch block
        } catch (NullPointerException e) {
            //TODO Auto-generated catch block
        }
        return "Failed";
    }
}