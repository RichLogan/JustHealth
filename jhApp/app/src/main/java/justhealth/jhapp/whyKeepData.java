package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.os.Bundle;

/**
 * Created by Stephen on 18/03/15.
 */
public class whyKeepData extends Activity {
    /**
     * Creates the action bar items for the Why should we keep your data page
     *
     * @param savedInstanceState The options menu in which the items are placed
     * @return True must be returned in order for the terms and conditions page to be displayed
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.why_keep_data);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Why should we keep your data?");
    }
}
