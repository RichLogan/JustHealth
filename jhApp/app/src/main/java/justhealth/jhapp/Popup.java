package justhealth.jhapp;

import android.app.Activity;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewGroup.LayoutParams;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.PopupWindow;
import android.widget.TextView;

/**
 * Created by Stephen on 29/11/14.
 */
public class Popup extends ActionBarActivity {

    PopupWindow popUp;
    LinearLayout layout;
    String calledFrom;
    LinearLayout mainLayout;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        popUp = new PopupWindow(this);
        layout = new LinearLayout(this);
        mainLayout = new LinearLayout(this);

        calledFrom = getIntent().getStringExtra("calledFrom");

        if(calledFrom == "Connections") {
            connect();
        }

        /*tv = new TextView(this);
        but = new Button(this);
        but.setText("Click Me");
        but.setOnClickListener(new View.OnClickListener() {

            public void onClick(View v) {
                if (click) {
                    popUp.showAtLocation(layout, Gravity.BOTTOM, 10, 10);
                    popUp.update(50, 50, 300, 80);
                    click = false;
                } else {
                    popUp.dismiss();
                    click = true;
                }
            }

        });
        params = new ViewGroup.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT,
                ViewGroup.LayoutParams.WRAP_CONTENT);
        layout.setOrientation(LinearLayout.VERTICAL);
        tv.setText("Hi this is a sample text for popup window");
        layout.addView(tv, params);
        popUp.setContentView(layout);
        // popUp.showAtLocation(layout, Gravity.BOTTOM, 10, 10);
        mainLayout.addView(but, params);
        setContentView(mainLayout);*/
    }

    private void connect() {
        LayoutParams params = new ViewGroup.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT,
                ViewGroup.LayoutParams.WRAP_CONTENT);
        TextView title = new TextView(this);
        title.setText("Please enter the verification code given by the requester");
        mainLayout.addView(title, params);

        popUp.showAtLocation(mainLayout, Gravity.CENTER, 10, 10);
        popUp.setContentView(mainLayout);
    }

}
