package justhealth.jhapp;

import android.annotation.TargetApi;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.provider.CalendarContract;
import android.util.Log;

import java.util.Calendar;
import java.util.GregorianCalendar;
import java.util.TimeZone;

/**
 * Created by Stephen on 11/12/14.
 */
public class CalendarAppointments extends Activity {

    @TargetApi(Build.VERSION_CODES.ICE_CREAM_SANDWICH)
    public void addEvent(/*String title, String addressNameNumber, String postcode, String description, String startDate, String startTime, String endDate, String endTime*/) {
        System.out.println("Method running");
        /*Intent intent = new Intent(Intent.ACTION_EDIT);
        intent.setType("vnd.android.cursor.item/event");
        intent.putExtra(CalendarContract.Events.TITLE, title);

        String location = addressNameNumber + ", " + postcode;
        intent.putExtra(CalendarContract.Events.EVENT_LOCATION, location);
        intent.putExtra(CalendarContract.Events.DESCRIPTION, description);

        String start = startDate + endTime;
        GregorianCalendar appStart = new GregorianCalendar(TimeZone.getTimeZone(start));
        intent.putExtra(CalendarContract.EXTRA_EVENT_BEGIN_TIME,
                appStart.getTimeInMillis());

        String end = endDate + endTime;
        GregorianCalendar appEnd = new GregorianCalendar(TimeZone.getTimeZone(end));
        intent.putExtra(CalendarContract.EXTRA_EVENT_BEGIN_TIME,
                appEnd.getTimeInMillis());*/





    }


}
