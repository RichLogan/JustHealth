package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

/**
 * Created by charlottehutchinson on 06/11/14.
 */

public class Privacy extends Activity {


    /**
     * Creates the action bar items for the Privacy Policy page
     * @param savedInstanceState The options menu in which the items are placed
     * @return True must be returned in order for the Privacy Policy page to be displayed
     */
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.privacy);

        final ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Privacy");

    }
}

