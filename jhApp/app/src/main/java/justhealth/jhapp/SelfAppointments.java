package justhealth.jhapp;

import android.annotation.TargetApi;
import android.app.ActionBar;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.StrictMode;
import android.provider.CalendarContract;
import android.view.ContextThemeWrapper;
import android.view.Gravity;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;

/**
 * Created by Stephen on 09/12/14.
 */
public class SelfAppointments extends Activity {
    private String string;
    //Hold all of the appointments
    JSONArray getApps = null;

    @TargetApi(Build.VERSION_CODES.HONEYCOMB)
    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.self_appointments);
        // Inflate your custom layout
        final ViewGroup actionBarLayout = (ViewGroup) getLayoutInflater().inflate(
                R.layout.appointment_action_bar, null);

        // Set up your ActionBar
        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Upcoming Appointments");

        getUpcomingAppointments();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu items for use in the action bar
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.action_bar_self_appointments, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle presses on the action bar items
        switch (item.getItemId()) {
            case R.id.archived:
                Intent archived = new Intent(SelfAppointments.this, SelfArchivedAppointments.class);
                archived.putExtra("appointments", getApps.toString());
                startActivity(archived);
                return true;
            case R.id.add:
                startActivity(new Intent(SelfAppointments.this, CreateSelfAppointment.class));
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }


    private void getUpcomingAppointments() {
        //this will not work when API authentication is put in place
        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);
        String password = account.getString("password", null);

        HashMap<String, String> details = new HashMap<String, String>();

        //Text Boxes
        details.put("loggedInUser", username);
        details.put("targetUser", username);
        String postRequest = Request.post("getAllAppointments", details, this);

        try {
            getApps = new JSONArray(postRequest);

        } catch (JSONException e) {
            e.printStackTrace();
        }


        for (int i = 0; i < getApps.length(); i++) {
            try {
                JSONObject obj = getApps.getJSONObject(i);
                final String appid = obj.getString("appid");
                final String name = obj.getString("name");
                final String appType = obj.getString("apptype");
                final String startDate = obj.getString("startdate");
                final String startTime = obj.getString("starttime");
                final String endDate = obj.getString("enddate");
                final String endTime = obj.getString("endtime");
                final String address = obj.getString("addressnamenumber");
                final String postcode = obj.getString("postcode");
                final String description = obj.getString("description");
                final String isPrivate = obj.getString("private");
                final String androidId = obj.getString("androideventid");

                final HashMap<String, String> appDetails = new HashMap<>();
                appDetails.put("appid", appid);
                appDetails.put("name", name);
                appDetails.put("appType", appType);
                appDetails.put("startDate", startDate);
                appDetails.put("startTime", startTime);
                appDetails.put("endDate", endDate);
                appDetails.put("endTime", endTime);
                appDetails.put("addressNameNumber", address);
                appDetails.put("postcode", postcode);
                appDetails.put("details", description);
                appDetails.put("private", isPrivate);
                appDetails.put("androidId", androidId);

                Date appDateTime = getDateTimeObject(startDate, startTime);
                Date now = new Date();
                if (appDateTime.after(now)) {

                    ContextThemeWrapper newContext = new ContextThemeWrapper(getBaseContext(), R.style.primaryButton);
                    Button app = new Button(newContext);
                    app.setBackgroundColor(Color.rgb(51, 122, 185));
                    app.setText(name + " " + startDate + " " + startTime);
                    LinearLayout layout = (LinearLayout) findViewById(R.id.upcomingAppointmentView);

                    layout.addView(app, new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.MATCH_PARENT));

                    LinearLayout.LayoutParams center = (LinearLayout.LayoutParams) app.getLayoutParams();
                    center.setMargins(0,30,0,0);
                    center.gravity = Gravity.CENTER;
                    app.setLayoutParams(center);

                    System.out.println("onclick listener applied");
                    app.setOnClickListener(new Button.OnClickListener() {
                        public void onClick(View view) {
                            appointmentAction(appDetails);
                        }
                    });
                }

            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }

    private void appointmentAction(final HashMap<String, String> appointmentDetails) {
        System.out.println("method running");
        AlertDialog.Builder alert = new AlertDialog.Builder(SelfAppointments.this);
        alert.setTitle("Appointment Options")
                .setItems(R.array.patient_appointments_options, new DialogInterface.OnClickListener() {
                    @TargetApi(Build.VERSION_CODES.ICE_CREAM_SANDWICH)
                    public void onClick(DialogInterface dialog, int which) {
                        if (which == 0) {
                            //View appointment
                            HashMap<String, Integer> appStart = getDateTimeFormat(appointmentDetails.get("startDate"), "00:00");
                            Calendar start = Calendar.getInstance();
                            start.set(appStart.get("year"), appStart.get("month"), appStart.get("day"), appStart.get("hour"), appStart.get("minute"));
                            Uri.Builder builder = CalendarContract.CONTENT_URI.buildUpon();
                            builder.appendPath("time");
                            ContentUris.appendId(builder, start.getTimeInMillis());
                            Intent intent = new Intent(Intent.ACTION_VIEW)
                                    .setData(builder.build());
                            startActivity(intent);
                        } else if (which == 1) {
                            //Edit appointment
                            Intent intent = new Intent(SelfAppointments.this, EditSelfAppointment.class);
                            intent.putExtra("appointmentDetails", appointmentDetails);
                            startActivity(intent);
                        } else if (which == 2) {
                            //Delete appointment
                            AlertDialog.Builder alert = new AlertDialog.Builder(SelfAppointments.this);

                            alert.setTitle("Delete Appointment");
                            alert.setMessage("Are you sure you want to delete this Appointment?");

                            alert.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int whichButton) {
                                    deleteAppointment(appointmentDetails);
                                }
                            });

                            alert.setNegativeButton("No", new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int whichButton) {
                                    // Cancelled.
                                }
                            });

                            alert.show();
                        }
                        //others to be added here
                    }
                });
        alert.show();
    }

    @TargetApi(Build.VERSION_CODES.ICE_CREAM_SANDWICH)
    private void deleteAppointment(HashMap<String, String> appointmentDetails) {
        //The API takes the username and AppID
        appointmentDetails.get("appid");
        SharedPreferences account = getSharedPreferences("account", 0);
        String username = account.getString("username", null);

        HashMap<String, String> details = new HashMap<String, String>();

        details.put("username", username);
        details.put("appid", appointmentDetails.get("appid"));
        //should return "Appointment Deleted"
        String postRequest = Request.post("deleteAppointment", details, this);
        System.out.println(appointmentDetails.get("androidId"));
        if (appointmentDetails.get("androidId") != "null") {
            long eventID = Long.parseLong(appointmentDetails.get("androidId"));
            ContentResolver cr = getContentResolver();
            ContentValues values = new ContentValues();
            Uri deleteUri = null;
            deleteUri = ContentUris.withAppendedId(CalendarContract.Events.CONTENT_URI, eventID);
            int rows = getContentResolver().delete(deleteUri, null, null);

            if (rows > 0) {
                if (postRequest.equals("Appointment Deleted")) {
                    //show the alert to say it is successful
                    Context context = getApplicationContext();
                    CharSequence text = "Appointment Deleted.";
                    //Length
                    int duration = Toast.LENGTH_LONG;
                    Toast toast = Toast.makeText(context, text, duration);
                    //Position
                    toast.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL, 0, 100);
                    toast.show();
                }
            }
        } else {
            if (postRequest.equals("Appointment Deleted")) {
                //show the alert to say it is successful
                Context context = getApplicationContext();
                CharSequence text = "Appointment Deleted.";
                //Length
                int duration = Toast.LENGTH_LONG;
                Toast toast = Toast.makeText(context, text, duration);
                //Position
                toast.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL, 0, 100);
                toast.show();
            }
        }

        finish();
        startActivity(getIntent());


    }


    private HashMap<String, Integer> getDateTimeFormat(String date, String time) {
        HashMap<String, Integer> formattedDateTime = new HashMap<>();

        System.out.println(date);
        System.out.println(time);
        Integer year = Integer.parseInt(date.substring(0, 4));
        Integer month = Integer.parseInt(date.substring(5, 7));
        month -= 1;  //because January = 0... December = 11
        Integer day = Integer.parseInt(date.substring(8, 10));
        Integer hour = Integer.parseInt(time.substring(0, 2));
        Integer minute = Integer.parseInt(time.substring(3, 5));

        formattedDateTime.put("year", year);
        formattedDateTime.put("month", month);
        formattedDateTime.put("day", day);
        formattedDateTime.put("hour", hour);
        formattedDateTime.put("minute", minute);
        return formattedDateTime;
    }

    private Date getDateTimeObject(String date, String time) {
        String dateTime = date + " " + time;
        System.out.println("string: " + dateTime);
        DateFormat format = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        try {
            Date newDate = format.parse(dateTime);
            System.out.println("DateType: " + newDate);
            return newDate;
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return null;
    }
}