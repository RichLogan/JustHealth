.. java:import:: android.content Context

.. java:import:: android.content SharedPreferences

.. java:import:: android.graphics Bitmap

.. java:import:: android.graphics BitmapFactory

.. java:import:: android.os AsyncTask

.. java:import:: android.util Base64

.. java:import:: android.widget ImageView

.. java:import:: java.io InputStream

.. java:import:: java.net URL

.. java:import:: java.net URLConnection

LoadImage
=========

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class LoadImage extends AsyncTask<String, Void, Bitmap>

   Loads An Image from a specified URL into a given ImageView Inspired by and uses code from: http://web.archive.org/web/20120802025411/http://developer.aiwgame.com/imageview-show-image-from-url-on-android-4-0.html

Fields
------
blur
^^^^

.. java:field::  boolean blur
   :outertype: LoadImage

context
^^^^^^^

.. java:field::  Context context
   :outertype: LoadImage

iv
^^

.. java:field::  ImageView iv
   :outertype: LoadImage

Constructors
------------
LoadImage
^^^^^^^^^

.. java:constructor:: public LoadImage(ImageView iv, boolean blur, Context context)
   :outertype: LoadImage

   LoadImage Constructor specifying a target TextView and Context

   :param iv: The target ImageView to load the image into
   :param blur: Whether to apply a blur to the image
   :param context: getApplicationContext()

Methods
-------
doInBackground
^^^^^^^^^^^^^^

.. java:method:: protected Bitmap doInBackground(String... url)
   :outertype: LoadImage

   Run through new LoadImage().execute(urls)

   :param url: The url of the requested image
   :return: A BitMap object of the image

fastblur
^^^^^^^^

.. java:method:: public static Bitmap fastblur(Bitmap sentBitmap, int radius)
   :outertype: LoadImage

   Mario Klingemann's function to efficiently provide a blur to a Bitmap

   :param sentBitmap: The bitmap image to blur
   :param radius: The level of blur to be applied
   :return: The blurred Bitmap

getProfilePictureURL
^^^^^^^^^^^^^^^^^^^^

.. java:method:: public static String getProfilePictureURL(String filename)
   :outertype: LoadImage

   Build the correct URL of a profilepicture image that is stored on the server

   :param filename: The filename of the image. Can be found via /api/getAccountInfo
   :return: The full URL of the resource

onPostExecute
^^^^^^^^^^^^^

.. java:method:: protected void onPostExecute(Bitmap image)
   :outertype: LoadImage

   Built in method that runs on completion of doInBackground(). Displays the loaded image into the target TextView iv

   :param image: The image to display

