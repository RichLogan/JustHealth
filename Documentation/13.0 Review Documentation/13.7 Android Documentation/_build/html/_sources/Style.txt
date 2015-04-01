.. java:import:: android.content Context

.. java:import:: android.graphics Color

.. java:import:: android.graphics.drawable Drawable

.. java:import:: android.widget Button

.. java:import:: android.widget LinearLayout

Style
=====

.. java:package:: justhealth.jhapp
   :noindex:

.. java:type:: public class Style

   Android doesn't have a method to programmatically apply styles, so rolled our own

Methods
-------
styleButton
^^^^^^^^^^^

.. java:method:: public static void styleButton(Button b, String type, LinearLayout ll, Context c)
   :outertype: Style

   Most of the time we're programmatically generating buttons, so this allows use to apply our primary/success/warning/danger styles.

   :param b: The button to style
   :param type: The style to apply (primary/success/warning/danger)
   :param ll: The linear layout the button will be applied to
   :param c: getApplicationContext()

