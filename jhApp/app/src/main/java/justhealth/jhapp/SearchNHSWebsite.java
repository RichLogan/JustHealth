package justhealth.jhapp;

import android.app.ActionBar;
import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.util.HashMap;


public class SearchNHSWebsite extends Activity {

    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.nhs_interfacing);

        // Set up your ActionBar
        ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Search NHS Direct Website");

        //Set on click listener to search
        Button search = (Button) findViewById(R.id.search);
        search.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        getURL();
                    }
                }
        );

    }
    /**
     * This sends the searched term by the user in a new HashMap as a post request to the NHS website
     */
    private void getURL() {
        String searchTerms = ((EditText) findViewById(R.id.searchTerm)).getText().toString();

        HashMap<String, String> details = new HashMap<>();
        details.put("searchterms", searchTerms);

        String website = Request.post("searchNHSDirectWebsite", details, getApplicationContext());
        openBrowser(website);

    }

    /**
     * The method ensure a new browser is opened when a user searches the NHS website
     * @param website that will be passed in order for the browser to open
     */
    private void openBrowser(String website) {
        Intent i = new Intent(Intent.ACTION_VIEW);
        i.setData(Uri.parse(website));
        startActivity(i);
    }
}
