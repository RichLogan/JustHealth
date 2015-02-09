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

/**
 * Created by Stephen on 30/01/15.
 */
public class SearchNHSWebsite extends Activity {

    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.nhs_interfacing);

        ActionBar actionBar = getActionBar();
        actionBar.setDisplayShowHomeEnabled(true);
        actionBar.setTitle("Search NHS Direct Website");

        Button search = (Button) findViewById(R.id.search);
        search.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        getURL();
                    }
                }
        );

    }

    private void getURL() {
        String searchTerms = ((EditText) findViewById(R.id.searchTerm)).getText().toString();

        HashMap<String, String> details = new HashMap<>();
        details.put("searchterms", searchTerms);

        String website = Request.post("searchNHSDirectWebsite", details, getApplicationContext());
        openBrowser(website);

    }

    private void openBrowser(String website) {
        Intent i = new Intent(Intent.ACTION_VIEW);
        i.setData(Uri.parse(website));
        startActivity(i);
    }
}
