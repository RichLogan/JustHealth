package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.os.Bundle;

public class TermsAndConditions extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.terms_and_conditions);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("T & C's");
    }
}