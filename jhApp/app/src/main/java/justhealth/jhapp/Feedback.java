package justhealth.jhapp;

import android.content.Context;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.Toast;

public class Feedback {
    public static void toast(String value, Boolean success, Context context) {
        CharSequence text = value;
        int duration = Toast.LENGTH_LONG;
        Toast toast = Toast.makeText(context, text, duration);
        //Position
        toast.setGravity(Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL, 0, 100);
        if (!success) {
            toast.getView().setBackgroundColor(Color.RED);
        }
        toast.show();
    }
}
