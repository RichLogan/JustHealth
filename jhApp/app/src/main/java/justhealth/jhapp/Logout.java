package justhealth.jhapp;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.view.Gravity;
import android.widget.Toast;

/**
 * Created by Stephen on 28/01/15.
 */
public class Logout extends Activity {

    public static void logout(Context context) {
        //redirect to login
        Intent it = new Intent(context,Login.class);
        it.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        context.startActivity(it);

        //remove data from shared preferences
        SharedPreferences account = context.getSharedPreferences("account", 0);
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
    }


}
