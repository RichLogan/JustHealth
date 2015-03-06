package justhealth.jhapp;

import android.app.Activity;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.support.v4.content.WakefulBroadcastReceiver;

/**
 * Created by Stephen on 26/02/15.
 */
public class GcmBroadcastReceiver extends WakefulBroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        ComponentName component = new ComponentName(context.getPackageName(), GcmIntentService.class.getName());

        startWakefulService(context, intent.setComponent(component));
        setResultCode(Activity.RESULT_OK);
    }
}
