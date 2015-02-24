package justhealth.jhapp;

import android.annotation.TargetApi;
import android.app.ActionBar;
import android.app.Activity;
import android.app.AlertDialog;
import android.app.PendingIntent;
import android.content.ContentUris;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.Drawable;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.StrictMode;
import android.provider.CalendarContract;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.Surface;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.joanzapata.android.iconify.IconDrawable;
import com.joanzapata.android.iconify.Iconify;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.Calendar;
import java.util.HashMap;

public class Login extends Activity implements SurfaceHolder.Callback {

    private MediaPlayer mp = null;
    SurfaceView surfaceView = null;
    SurfaceHolder surfaceHolder = null;

    @TargetApi(Build.VERSION_CODES.HONEYCOMB)
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

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu items for use in the action bar
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.action_bar_login, menu);
        return super.onCreateOptionsMenu(menu);
    }

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

    private void requestLogin() {
        HashMap<String, String> loginInformation = new HashMap<String, String>();
        loginInformation.put("username", ((EditText) findViewById(R.id.loginUsername)).getText().toString());

        String password = ((EditText) findViewById(R.id.loginPassword)).getText().toString();
        loginInformation.put("password", password);

        String encryptedPassword = getEncryptedPassword(password);
        System.out.println("This is the encrypted password: " + encryptedPassword);

        String response = Request.post("authenticate", loginInformation, getApplicationContext());

        if (response.equals("Authenticated")) {
            SharedPreferences account = getSharedPreferences("account", 0);
            SharedPreferences.Editor edit = account.edit();
            edit.putString("username", loginInformation.get("username"));
            edit.putString("password", encryptedPassword);

            String accountType = getAccountType(loginInformation.get("username"));
            edit.putString("accountType", accountType);
            edit.commit();
            startActivity(new Intent(Login.this, Main.class));
        }
        else if (response.equals("Reset")) {
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
        }
        else if (response.equals("<11")) {
            String expiredUsername = loginInformation.get("username");
            String expiredPassword = encryptedPassword;
            String expiredAccountType = getAccountType(expiredUsername);
            //options dialog
            giveResetOptions(expiredUsername, expiredPassword, expiredAccountType);
        }
        else {
            Feedback.toast(response, false, getApplicationContext());
        }
    }

    private String getAccountType(String username) {
        HashMap<String, String> parameters = new HashMap<String, String>();
        parameters.put("username", username);

        String response = Request.post("getAccountInfo", parameters, getApplicationContext());
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

    private String getEncryptedPassword(String plaintextPassword) {
        HashMap<String, String> ptPassword = new HashMap<String, String>();
        ptPassword.put("password", plaintextPassword);
        String response = Request.post("encryptPassword", ptPassword, getApplicationContext());
        return response;
    }

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

    public void registerWithServer() {
        Intent intent = new Intent("com.google.android.c2dm.intent.REGISTER");
        intent.putExtra("app", PendingIntent.getBroadcast(this, 0, new Intent(), 0));
        intent.putExtra("sender", "1054401665950");
        startService(intent);
    }
}