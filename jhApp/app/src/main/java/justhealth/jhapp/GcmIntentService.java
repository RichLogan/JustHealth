package justhealth.jhapp;

import android.app.IntentService;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.media.RingtoneManager;
import android.net.Uri;
import android.opengl.Visibility;
import android.os.Bundle;
import android.os.SystemClock;
import android.support.v4.app.NotificationCompat;
import android.widget.Toast;

import com.google.android.gms.gcm.GoogleCloudMessaging;

/**
 * Created by Stephen on 26/02/15.
 */
public class GcmIntentService extends IntentService {
    public static int NOTIFICATION_ID = 0;
    private NotificationManager mNotificationManager;
    NotificationCompat.Builder builder;

    public GcmIntentService() {
        super("GcmIntentService");
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        Bundle extras = intent.getExtras();
        GoogleCloudMessaging gcm = GoogleCloudMessaging.getInstance(this);
        // The getMessageType() intent parameter must be the intent you received
        // in your BroadcastReceiver.
        String messageType = gcm.getMessageType(intent);

        if (!extras.isEmpty()) {  // has effect of unparcelling Bundle
            /*
             * Filter messages based on message type.
             */
            if (GoogleCloudMessaging.
                    MESSAGE_TYPE_SEND_ERROR.equals(messageType)) {
                String title = extras.get("title").toString();
                String content = "Send error: " + extras.get("message").toString();
                sendNotification(title, content);
            } else if (GoogleCloudMessaging.
                    MESSAGE_TYPE_DELETED.equals(messageType)) {
                String title = extras.get("title").toString();
                String content = "Deleted messages on server: " + extras.get("message").toString();
                sendNotification(title, content);
                // If it's a regular GCM message, do some work.
            } else if (GoogleCloudMessaging.
                    MESSAGE_TYPE_MESSAGE.equals(messageType)) {
                // This loop represents the service doing some work.
                /*for (int i=0; i<5; i++) {
                    System.out.println("GCM reply working");
                    try {
                        Thread.sleep(5000);
                    } catch (InterruptedException e) {
                    }
                }*/
                System.out.println("Working");
                // Post notification of received message.
                sendNotification(extras.get("title").toString(), extras.get("message").toString());
                System.out.println("Received Notification Sent");
            }
        }
        // Release the wake lock provided by the WakefulBroadcastReceiver.
        GcmBroadcastReceiver.completeWakefulIntent(intent);
    }

    /**
     * Adds the GCM message to a notification that can be displayed in the notification bar.
     * @param title The title of the notification
     * @param message The message of the notification
     */
    private void sendNotification(String title, String message) {
        mNotificationManager = (NotificationManager)
                this.getSystemService(Context.NOTIFICATION_SERVICE);

        //This is where the application opens too (we think) therefore this may need to be dynamic depending on Notification Type.
        PendingIntent contentIntent = PendingIntent.getActivity(this, 0,
                new Intent(this, Main.class), 0);

        NotificationCompat.Builder mBuilder =
                new NotificationCompat.Builder(this)
                        .setSmallIcon(R.drawable.pill)
                        .setContentTitle(title)
                        .setStyle(new NotificationCompat.BigTextStyle()
                                .bigText(message))
                        .setContentText(message);


        Uri notify = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
        mBuilder.setSound(notify);
        mBuilder.setContentIntent(contentIntent);
        mNotificationManager.notify(NOTIFICATION_ID, mBuilder.build());
        notificationInteger(NOTIFICATION_ID);
    }

    /**
     * Sets the notification ID between 0 and 9, allows 10 notifications from Justhealth to be
     * displayed before they cancel each other out.
     *
     * @param count the current ID of the notification
     */
    private void notificationInteger(int count) {
        if (count < 10) {
            count += 1;
            NOTIFICATION_ID = count;
        }
        else {
            NOTIFICATION_ID = 0;
        }
    }
}
