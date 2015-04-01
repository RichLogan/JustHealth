package justhealth.jhapp;

import android.content.Context;
import android.graphics.Color;
import android.graphics.drawable.Drawable;
import android.widget.Button;
import android.widget.LinearLayout;

/**
 * Android doesn't have a method to programmatically apply styles, so rolled our own
 */
public class Style {

    /**
     * Most of the time we're programmatically generating buttons, so this allows use to apply
     * our primary/success/warning/danger styles.
     *
     * @param b The button to style
     * @param type The style to apply (primary/success/warning/danger)
     * @param ll The linear layout the button will be applied to
     * @param c getApplicationContext()
     */
    public static void styleButton(Button b, String type, LinearLayout ll, Context c) {
        //Deprecated method because min API: 11
        Drawable background;
        if (type.equals("primary")) {
            background = c.getResources().getDrawable(R.drawable.primary_button);
            b.setBackgroundDrawable(background);
        }
        else if (type.equals("success")) {
            background = c.getResources().getDrawable(R.drawable.success_button);
            b.setBackgroundDrawable(background);
        }
        else if (type.equals("warning")) {
            background = c.getResources().getDrawable(R.drawable.warning_button);
            b.setBackgroundDrawable(background);
        }
        else if (type.equals("danger")) {
            background = c.getResources().getDrawable(R.drawable.danger_button);
            b.setBackgroundDrawable(background);
        }
        b.setTextColor(Color.WHITE);
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, 250);
        params.setMargins(10, 25, 10, 25);
        b.setLayoutParams(params);
        ll.addView(b);
    }
}