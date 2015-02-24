package justhealth.jhapp;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.os.AsyncTask;
import android.os.Bundle;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GooglePlayServicesUtil;
import com.google.android.gms.gcm.GoogleCloudMessaging;

import java.io.IOException;
import java.util.HashMap;

/**
 * JustHealth main application. The user will never see this, but it acts as the primary activity
 * and mainly handles setup required for Google Cloud Messaging (Push notifications).
 *
 * It also checks whether a user is logged in and their account type in order to present them
 * with the correct activity.
 */
public class Main extends Activity {


    // JustHealth Google Developer Project Number
    String SENDER_ID = "1054401665950";

    Context context;
    GoogleCloudMessaging gcm;
    SharedPreferences account;
    String regid;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        account = getSharedPreferences("account", 0);
        //account.edit().clear().commit();

         if (!isLoggedIn()) {
            System.out.println("Logged out");
            finish();
            startActivity(new Intent(Main.this, Login.class));
        }
        else {

             System.out.println("Logged In");
             System.out.println(account.getString("username", null));

             context = getApplicationContext();

             // Check for GooglePlayServices support
             if (checkPlayServices()) {
                 System.out.println("Check google play services");
                 gcm = GoogleCloudMessaging.getInstance(this);
                 regid = getRegistrationId();

                 if (regid.isEmpty()) {
                     registerInBackground();
                 }

                 //Redirect where they need to go.
                 redirect();
             } else {
                 Feedback.toast("No valid Google Play Services APK found.", false, context);
             }
         }
    }

    /**
     * Runs on reopen of application
     */
    protected void onResume() {
        super.onResume();
        if (!isLoggedIn()) {
            System.out.println("Logged out");
            finish();
            startActivity(new Intent(Main.this, Login.class));
        }
        else {
            System.out.println("Logged in");
            System.out.println(account.getString("username", null));
            checkPlayServices();
            redirect();
        }
    }

    /**
     * Checks whether a user appears to be logged in or not
     *
     * @return Whether a user is logged in (true) or not (false)
     */
    private boolean isLoggedIn() {
        String username = account.getString("username", null);
        if (username == null) {
            return false;
        }
        return true;
    }

    /**
     * Redirects a user to where they should go on app open.
     */
    private void redirect() {
        String accountType = getSharedPreferences("account", 0).getString("accountType", null);
        System.out.println("Account Type: " + accountType);
        if (accountType.equals("Patient")) {
            // Found logged in Patient
            finish();
            startActivity(new Intent(Main.this, HomePatient.class));
        }
        else if (accountType.equals("Carer")) {
            // Found logged in Carer
            finish();
            startActivity(new Intent(Main.this, HomeCarer.class));
        }
        else if (accountType.equals("Admin")) {
            // Found admin
            Feedback.toast("Administrators cannot yet use the Android Application", false , context);
        }
        else {
            // Should never happen
            finish();
            Feedback.toast("Something somewhere has broken. Please try again", false, context);
        }

    }

    /**
     * Check the device to make sure it has the Google Play Services APK. If
     * it doesn't, display a dialog that allows users to download the APK from
     * the Google Play Store or enable it in the device's system settings.
     */
    private boolean checkPlayServices() {
        int resultCode = GooglePlayServicesUtil.isGooglePlayServicesAvailable(this);
        if (resultCode != ConnectionResult.SUCCESS) {
            if (GooglePlayServicesUtil.isUserRecoverableError(resultCode)) {
                GooglePlayServicesUtil.getErrorDialog(resultCode, this, 9000).show();
            } else {
                Feedback.toast("Your device's OS does not support Google Play Services", false, context);
            }
            return false;
        }
        return true;
    }

    /**
     * Gets the current registration ID for application on GCM service.
     * If result is empty, the app needs to register.
     *
     * @return registration ID, or empty string if there is no existing registration ID.
     */
    private String getRegistrationId() {
        SharedPreferences account = getSharedPreferences("account", 0);
        String registrationId = account.getString("registrationid", "");
        if (registrationId.isEmpty()) {
            return "";
        }

        // Check if app was updated; if so, it must clear the registration ID
        // since the existing registration ID is not guaranteed to work with
        // the new app version.
        int registeredVersion = account.getInt("appversion", 0);
        int currentVersion = getAppVersion();
        if (registeredVersion != currentVersion) {
            Feedback.toast("Updating...", true, context);
            return "";
        }
        return registrationId;
    }

    /**
     * @return Application's version code from the {@code PackageManager}.
     */
    private int getAppVersion() {
        try {
            PackageInfo packageInfo = context.getPackageManager().getPackageInfo(context.getPackageName(), 0);
            return packageInfo.versionCode;
        } catch (PackageManager.NameNotFoundException e) {
            throw new RuntimeException("Could not get package name: " + e);
        }
    }

    private void registerInBackground() {
        new AsyncTask() {
            @Override
            protected Object doInBackground(Object[] params) {
                String msg = "";
                try {
                    if (gcm == null) {
                        gcm = GoogleCloudMessaging.getInstance(context);
                    }
                    regid = gcm.register(SENDER_ID);
                    msg = "Device registered, registration ID=" + regid;
                    sendRegistrationIdToBackend(regid);
                    storeRegistrationId(regid);
                } catch (IOException ex) {
                    msg = "Error :" + ex.getMessage();
                    // TODO: If there is an error, don't just keep trying to register.Require the user to click a button again, or perform exponential back-off.
                }
                return msg;
            }

            @Override
            protected void onPostExecute(Object result) {
                System.out.println(result);
            }
        }.execute(null, null, null);
    }

    /**
     * Sends the registration ID to your server over HTTP, so it can use GCM/HTTP
     * or CCS to send messages to your app. Not needed for this demo since the
     * device sends upstream messages to a server that echoes back the message
     * using the 'from' address in the message.
     */
    private void sendRegistrationIdToBackend(String regid) {
        System.out.println("sending regid to backend API");
        String username = account.getString("username", null);
        HashMap<String, String> params = new HashMap<String, String>();
        params.put("username", username);
        params.put("registrationid", regid);
        String response = Request.post("saveAndroidRegistrationID", params, context);
        System.out.println(response);
        if (response.equals("False")) {
            System.out.println("Could not register device");
        }
    }

    /**
     * Stores the registration ID and app versionCode in the application's
     * {@code SharedPreferences}.
     *
     * @param regId registration ID
     */
    private void storeRegistrationId(String regId) {
        int appVersion = getAppVersion();
        System.out.println("Successfully stored Registration ID");
        SharedPreferences account = getSharedPreferences("account", 0);
        SharedPreferences.Editor editor = account.edit();
        editor.putString("registrationid", regId);
        editor.putInt("appversion", appVersion);
        editor.apply();
    }
}