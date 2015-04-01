package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.os.Bundle;

public class TermsAndConditions extends Activity {

    /**
     * Creates the action bar items for the Terms and Conditions page.
     *
     * @param savedInstanceState The options menu in which the items are placed.
     * @return True must be returned in order for the terms and conditions page to be displayed
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.terms_and_conditions);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("T & C's");
    }
}


