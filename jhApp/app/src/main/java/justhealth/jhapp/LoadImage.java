package justhealth.jhapp;

import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.util.Base64;
import android.widget.ImageView;

import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;

/**
 * Loads An Image from a specified URL into a given ImageView
 *
 * Inspired by and uses code from: http://web.archive.org/web/20120802025411/http://developer.aiwgame.com/imageview-show-image-from-url-on-android-4-0.html
 */
public class LoadImage extends AsyncTask<String, Void, Bitmap> {
    ImageView iv;
    Context context;

    /**
     * LoadImage Constructor specifying a target TextView and Context
     * @param iv The target ImageView to load the image into
     * @param context getApplicationContext()
     */
    public LoadImage(ImageView iv, Context context) {
        this.iv = iv;
        this.context = context;
    }

    /**
     * Run through new LoadImage().execute(urls)
     * @param url The url of the requested image
     * @return A BitMap object of the image
     */
    protected Bitmap doInBackground(String... url) {
        URL imageLocation;
        try {
            // Convert String to URL object
            imageLocation = new URL(url[0]);

            // Add Basic Authentication Authentication
            SharedPreferences account = context.getSharedPreferences("account", 0);
            String username = account.getString("username", null);
            String password = account.getString("password", null);
            String authentication = username + ":" + password;
            String encodedAuthentication = Base64.encodeToString(authentication.getBytes(), Base64.NO_WRAP);

            // Connect to URL
            URLConnection loader = imageLocation.openConnection();
            loader.setRequestProperty("Authorization", "Basic " + encodedAuthentication);

            // Return Content
            InputStream content = loader.getInputStream();
            return BitmapFactory.decodeStream(content);
        } catch (Exception e) {
            Feedback.toast("Image load failed", false, context);
            return null;
        }
    }

    /**
     * Built in method that runs on completion of doInBackground().
     * Displays the loaded image into the target TextView iv
     * @param image The image to display
     */
    protected void onPostExecute(Bitmap image) {
        iv.setImageBitmap(image);
    }
}