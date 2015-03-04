package justhealth.jhapp;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.view.Gravity;
import android.widget.Toast;

import java.util.HashMap;

/**
 * Created by Stephen on 28/01/15.
 */
public class Logout extends Activity {

    public static void logout(Context context) {
        //redirect to login
        Intent it = new Intent(context, Login.class);
        it.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        context.startActivity(it);

        //remove data from shared preferences
        SharedPreferences account = context.getSharedPreferences("account", 0);
        //remove the device from the database so it no longer receives push notifications
        String username = account.getString("username", null);
        String regId = account.getString("registrationid", null);
        HashMap<String, String> details = new HashMap<>();
        details.put("username", username);
        details.put("registrationid", regId);

        String response = Request.post("deleteAndroidRegistrationID", details, context);
        if (response.equals("True")) {

            SharedPreferences.Editor edit = account.edit();
            edit.clear();
            edit.commit();


            //Toast - user feedback
            CharSequence text = "Logout Successful. We hope to see you soon.";
            //Length
            int duration = Toast.LENGTH_LONG;
            Toast toast = Toast.makeText(context, text, duration);
            //Position
            toast.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL, 0, 100);
            toast.show();
        } else {
            CharSequence text = "Logout Failed. Please try again.";
            //Length
            int duration = Toast.LENGTH_LONG;
            Toast toast = Toast.makeText(context, text, duration);
            //Position
            toast.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL, 0, 100);
            toast.show();
        }
    }
}
