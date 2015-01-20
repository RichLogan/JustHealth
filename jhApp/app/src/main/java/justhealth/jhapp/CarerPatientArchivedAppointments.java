package justhealth.jhapp;

import android.annotation.TargetApi;
import android.app.ActionBar;
import android.app.Activity;
import android.app.AlertDialog;
import android.app.SharedElementCallback;
import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.drawable.ColorDrawable;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.CalendarContract;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

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
 * Created by Stephen on 06/01/15.
 */
public class CarerPatientArchivedAppointments extends Activity {

    private JSONArray getApps;
    private String filter = "All";
    private String patient = "";
    private String firstname = "";
    private String surname = "";
    private String carerUsername = "";

    //LinearLayout that holds all of the buttons
    LinearLayout appointmentHolder;


    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.carer_patient_appointments);

        final ViewGroup actionBarLayout = (ViewGroup) getLayoutInflater().inflate(
                R.layout.appointment_action_bar, null);

        // Set up your ActionBar
        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Archived");

        actionBar.setDisplayShowCustomEnabled(true);
        actionBar.setCustomView(actionBarLayout);

        final Button addAppointment = (Button) findViewById(R.id.addAppointment);
        addAppointment.setText("Add");
        addAppointment.setOnClickListener(new Button.OnClickListener() {
            public void onClick(View view) {
                Intent add = new Intent(CarerPatientArchivedAppointments.this, CreateCarerPatientAppointment.class);
                add.putExtra("patient", patient);
                add.putExtra("firstName", firstname);
                add.putExtra("surname", surname);
                startActivity(add);
            }
        });

        //Get data passed from MyPatients

        final Bundle extras = getIntent().getExtras();
        if (extras != null) {
            patient = extras.getString("patient");
            firstname = extras.getString("firstName");
            surname = extras.getString("surname");
            try {
                getApps = new JSONArray(extras.getString("appointments"));
            }
            catch (JSONException e) {
                e.printStackTrace();
            }

        }

        Button filter = (Button) findViewById(R.id.filter);
        filter.setOnClickListener(new Button.OnClickListener() {
            public void onClick(View view) {
                filterOptions();
            }
        });

        final Button actionViewMore = (Button) findViewById(R.id.more);
        actionViewMore.setText("Upcoming");
        actionViewMore.setOnClickListener(new Button.OnClickListener() {
            public void onClick(View view) {
                finish();
            }
        });

        //get carer username
        SharedPreferences account = getSharedPreferences("account", 0);
        carerUsername = account.getString("username", null);

        //set the name of the patient
        TextView patientName = (TextView) findViewById(R.id.patientName);
        patientName.setText(firstname + " " + surname);

        getAppointments(patient);
    }

    private void getAppointments(String targetUsername) {

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
                final String creator = obj.getString("creator");

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
                appDetails.put("creator", creator);

                if(filter.equals("PatientsOnly")) {
                    if(creator.equals(targetUsername)) {
                        addToView(appDetails);
                    }
                }
                else if(filter.equals("CarerPatient")) {
                    if(creator.equals(getSharedPreferences("account", 0).getString("username", null))) {
                        addToView(appDetails);
                    }
                }
                else {
                    addToView(appDetails);
                }


            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }

    private void addToView(final HashMap<String, String> appointment) {
        String startDate = appointment.get("startDate");
        String startTime = appointment.get("startTime");
        String name = appointment.get("name");

        Date appDateTime = getDateTimeObject(startDate, startTime);
        Date now = new Date();
        if (appDateTime.before(now)) {
            appointmentHolder = new LinearLayout(this);
            Button app = new Button(this);
            final int buttonColour = getResources().getColor(R.color.button);
            app.setBackgroundDrawable(new ColorDrawable(buttonColour));
            app.setText(name + " " + startDate + " " + startTime);
            appointmentHolder = (LinearLayout) findViewById(R.id.appointments);
            appointmentHolder.addView(app, new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.MATCH_PARENT));

            LinearLayout.LayoutParams center = (LinearLayout.LayoutParams) app.getLayoutParams();
            center.gravity = Gravity.CENTER;
            app.setLayoutParams(center);

            System.out.println("onclick listener applied");
            app.setOnClickListener(new Button.OnClickListener() {
                public void onClick(View view) {
                    appointmentAction(appointment);
                }
            });
        }
    }

    private void appointmentAction(final HashMap<String, String> appointmentDetails) {
        System.out.println("method running");
        AlertDialog.Builder alert = new AlertDialog.Builder(CarerPatientArchivedAppointments.this);
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
                            if(appointmentDetails.get("creator").equals(carerUsername)) {
                                Intent intent = new Intent(CarerPatientArchivedAppointments.this, EditCarerPatientAppointment.class);
                                intent.putExtra("appointmentDetails", appointmentDetails);
                                intent.putExtra("firstName", firstname);
                                intent.putExtra("surname", surname);
                                startActivity(intent);
                            }
                            else {
                                Feedback.toast("Read Only Access Permitted", false, getApplicationContext());
                            }
                        } else if (which == 2) {
                            //Delete appointment
                            if (appointmentDetails.get("creator").equals(carerUsername)) {
                                AlertDialog.Builder alert = new AlertDialog.Builder(CarerPatientArchivedAppointments.this);

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
                            } else {
                                Feedback.toast("Read Only Access Permitted.", false, getApplicationContext());
                            }
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
                    Feedback.toast("Appointment Deleted", true, this);
                }
            }
        } else {
            if (postRequest.equals("Appointment Deleted")) {
                //show the alert to say it is successful
                Feedback.toast("Appointment Deleted", true, this);
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


    private void filterOptions() {
        AlertDialog.Builder alert = new AlertDialog.Builder(CarerPatientArchivedAppointments.this);
        alert.setTitle("Filter By:")
                .setItems(R.array.my_patient_filter_appointments, new DialogInterface.OnClickListener() {
                    @TargetApi(Build.VERSION_CODES.ICE_CREAM_SANDWICH)
                    public void onClick(DialogInterface dialog, int which) {
                        if (which == 0) {
                            filter = "None";
                            appointmentHolder.removeAllViews();
                            getAppointments(patient);
                        } else if (which == 1) {
                            filter = "PatientsOnly";
                            appointmentHolder.removeAllViews();
                            getAppointments(patient);
                        } else if (which == 2) {
                            appointmentHolder.removeAllViews();
                            filter = "CarerPatient";
                            getAppointments(patient);
                        }
                    }


                });
        alert.show();
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

