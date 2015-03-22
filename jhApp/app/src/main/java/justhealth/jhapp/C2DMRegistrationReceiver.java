package justhealth.jhapp;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

/**
 * This class defines how the android device that is running the application
 * is able to get its registration ID. RegistrationID of the device is subsequently
 * used for push notifications.
 */
public class C2DMRegistrationReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        String action = intent.getAction();
        if ("com.google.android.c2dm.intent.REGISTRATION".equals(action)) {
            System.out.println("Received registration ID");
            final String registrationId = intent.getStringExtra("registration_id");
            System.out.println("Reg:");
            System.out.println(registrationId);
        }
    }
}