package justhealth.jhapp;

import android.annotation.TargetApi;
import android.app.ActionBar;
import android.app.Activity;
import android.app.AlertDialog;
import android.app.PendingIntent;
import android.app.ProgressDialog;
import android.content.ContentUris;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.os.StrictMode;
import android.provider.CalendarContract;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.Calendar;
import java.util.HashMap;

public class Login extends Activity implements SurfaceHolder.Callback {

    private MediaPlayer mp = null;
    SurfaceView surfaceView = null;
    SurfaceHolder surfaceHolder = null;

    /**
     * Runs when the login page is first loaded. Attempts to load the video that is on the home page
     * of the web. Please not that this does not yet work.
     * Loads the action bar.
     * Add onClickListeners for the login, register and forgot password buttons on the page.
     *
     * @param savedInstanceState  a bundle if the state of the application was to be saved.
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);

        ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);

        surfaceView = (SurfaceView)findViewById(R.id.loginVideoSurface);
        surfaceHolder = surfaceView.getHolder();
        surfaceHolder.addCallback(this);
        mp = new MediaPlayer();

        TextView register = (TextView) findViewById(R.id.link_to_forgot_password);
        register.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(Login.this, ForgotPassword.class));
                    }
                }
        );

        TextView forgotPassword = (TextView) findViewById(R.id.link_to_register);
        forgotPassword.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        startActivity(new Intent(Login.this, Register.class));
                    }
                }
        );

        Button loginButton = (Button) findViewById(R.id.login);
        loginButton.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        requestLogin();
                    }
                }
        );
    }

    /**
     * Attempt in order to display the video, this currently runs the exception
     *
     * @param holder The placeholder for the video.
     */
    @Override
    public void surfaceCreated(SurfaceHolder holder) {
        // Thanks to: http://stackoverflow.com/questions/8830111/integrating-video-file-in-android-app-as-app-background
        try {
            mp.setDisplay(holder);
            mp.setDataSource(this, Uri.parse("android:resource://" + getPackageName() + "/" + R.raw.phone));
            mp.prepare();
            mp.start();
        } catch (IOException e) {
            System.out.println("Video load failed");
        }
    }

    @Override
    public void surfaceDestroyed(SurfaceHolder h) {System.out.println("1");}
    @Override
    public void surfaceChanged(SurfaceHolder h, int a, int b, int c) {System.out.println("1");}

    /**
     * Creates the action bar items for the Login page
     *
     * @param menu The options menu in which the items are placed
     * @return True must be returned in order for the options menu to be displayed
     */
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu items for use in the action bar
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.action_bar_login, menu);
        return super.onCreateOptionsMenu(menu);
    }

    /**
     * This method is called when any action from the action bar is selected
     *
     * @param item The menu item that was selected
     * @return in order for the method to work, true should be returned here
     */
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle presses on the action bar items
        switch (item.getItemId()) {
            case R.id.terms:
                startActivity(new Intent(Login.this, TermsAndConditions.class));
                return true;
            case R.id.privacy:
                startActivity(new Intent(Login.this, Privacy.class));
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }

    /**
     * This makes the async request to login, authentication and receiving the encrypted password
     * back from the JustHealth API.
     */
    private void requestLogin() {
        final HashMap<String, String> loginInformation = new HashMap<String, String>();
        final String username =  ((EditText) findViewById(R.id.loginUsername)).getText().toString();
        final String password = ((EditText) findViewById(R.id.loginPassword)).getText().toString();

        loginInformation.put("username", username);
        loginInformation.put("password", password);

        new AsyncTask<Void, Void, Void>() {

            String encryptedPassword;
            String response;
            ProgressDialog progressDialog;

            /**
             * Loads the progress dialog
             */
            @Override
            protected void onPreExecute() {
                progressDialog = ProgressDialog.show(Login.this,"Loading...", "Logging you in",true);
            }

            /**
             * Runs the getEncryptedPassword method
             * Makes the post request to the JustHealth API in order to authenticate.
             *
             * @param v shows that there are no parameters passed to the method that runs off of the
             *          main thread.
             * @return null
             */
            @Override
            protected Void doInBackground(Void... v) {
                encryptedPassword = getEncryptedPassword(password);
                response = Request.post("authenticate", loginInformation, getApplicationContext());
                return null;
            }

            /**
             * Gets different responses from the server and decides what to do next.
             * i.e. authenticates, forces a password change, asks the user about the password change
             * feedback wrong password etc.
             *
             * @param v shows that there are no parameters passed to the method that runs off of the
             *          main thread.
             */
            @Override
            protected void onPostExecute(Void v) {
                try {
                    switch (response) {

                        case "Authenticated":
                            SharedPreferences account = getSharedPreferences("account", 0);
                            SharedPreferences.Editor edit = account.edit();
                            edit.putString("username", loginInformation.get("username"));
                            edit.putString("password", encryptedPassword);
                            edit.apply();

                            String accountType = getAccountType(loginInformation.get("username"));
                            edit.putString("accountType", accountType);
                            edit.apply();

                            startActivity(new Intent(Login.this, Main.class));
                            break;

                        case "Reset":
                            String expiredUsername = loginInformation.get("username");
                            String expiredPassword = encryptedPassword;
                            String expiredAccountType = getAccountType(expiredUsername);

                            Intent reset = new Intent(Login.this, ExpiredPassword.class);
                            reset.putExtra("message", "Your password has expired and needs to be reset before you will be able to log in. " +
                                    "JustHealth enforce this from time-to-time to ensure that your " +
                                    "privacy and security are maximised whilst using the website.");
                            reset.putExtra("username", expiredUsername);
                            reset.putExtra("password", expiredPassword);
                            reset.putExtra("accountType", expiredAccountType);
                            startActivity(reset);
                            break;

                        case "<11":
                            expiredUsername = loginInformation.get("username");
                            expiredAccountType = getAccountType(expiredUsername);
                            giveResetOptions(expiredUsername, encryptedPassword, expiredAccountType);
                            break;

                        default:
                            Feedback.toast(response, false, getApplicationContext());
                            break;
                    }
                } catch (NullPointerException e) {
                    Feedback.toast(getString(R.string.connectionIssue), false, getApplicationContext());
                }
                progressDialog.dismiss();
            }
        }.execute();
    }

    /**
     * Makes a post request to the JustHealth API and get the account type of the user.
     *
     * @param username The username of the user that has logged in.
     * @return The account type of the user
     */
    private String getAccountType(String username) {
        HashMap<String, String> parameters = new HashMap<String, String>();
        parameters.put("username", username);

        String response = Request.post("getAccountInfo", parameters, getApplicationContext());
        try {
            JSONObject accountDetails = new JSONObject(response);
            return accountDetails.getString("accounttype");
        }
        catch (JSONException e) {
            System.out.println(e.getStackTrace());
        }
        return null;
    }

    /**
     * Makes a post request to the JustHealth API to get the encrypted password of the user.
     *
     * @param plaintextPassword the plaintext password the user has typed to login.
     * @return the encrypted password
     */
    private String getEncryptedPassword(String plaintextPassword) {
        HashMap<String, String> ptPassword = new HashMap<String, String>();
        ptPassword.put("password", plaintextPassword);


        return Request.post("encryptPassword", ptPassword, getApplicationContext());
    }

    /**
     * Run when the users password is due to expire in the next 11 days. Gives the user the option to
     * change their password not or later. Depending on the response they are taken to the reset
     * password page or their relevant home page.
     *
     * @param expiredUsername The username of the user
     * @param expiredPassword The password that they have used to login.
     *                        (The one that needs to be changed)
     * @param expiredAccountType The account type of the user.
     */
    private void giveResetOptions(final String expiredUsername, final String expiredPassword, final String expiredAccountType) {
        AlertDialog.Builder alert = new AlertDialog.Builder(Login.this);
        alert.setTitle("Password Expiring")
                .setItems(R.array.password_expiry_options, new DialogInterface.OnClickListener() {
                    @TargetApi(Build.VERSION_CODES.ICE_CREAM_SANDWICH)
                    public void onClick(DialogInterface dialog, int which) {
                        if (which == 0) {
                            Intent reset = new Intent(Login.this, ExpiredPassword.class);
                            reset.putExtra("message", "Your password is soon going to expire. " +
                                    "JustHealth enforce this from time-to-time to ensure that your " +
                                    "privacy and security are maximised whilst using the website");
                            reset.putExtra("username", expiredUsername);
                            reset.putExtra("password", expiredPassword);
                            reset.putExtra("accountType", expiredAccountType);
                            startActivity(reset);

                        } else if (which == 1) {
                            SharedPreferences account = getSharedPreferences("account", 0);
                            SharedPreferences.Editor edit = account.edit();
                            edit.putString("username", expiredUsername);
                            edit.putString("password", expiredPassword);

                            edit.putString("accountType", expiredAccountType);
                            edit.commit();

                            startActivity(new Intent(Login.this, Main.class));
                        }
                    }
                });
        alert.show();
    }

    /**
     * This method is not used. Was trial and error with the android notifications!
     * 
     */
    public void registerWithServer() {
        Intent intent = new Intent("com.google.android.c2dm.intent.REGISTER");
        intent.putExtra("app", PendingIntent.getBroadcast(this, 0, new Intent(), 0));
        intent.putExtra("sender", "1054401665950");
        startService(intent);
    }
}