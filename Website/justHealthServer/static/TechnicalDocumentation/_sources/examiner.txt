==============================
Examiners Guide to JustHealth 
==============================

---------
Welcome
---------

Welcome to JustHealth's Documentation!

If you are viewing this online, you can skip this section. If this is the paper copy please note that our corpus index file (your starting place after this document) can be found at: /corpusIndex.html. This lists all documentation, authorship and links to the resources.  

*Note: Above, '/' demonstrates the root of the filesystem on our hand in media (USB).*

------------------------
Website
------------------------

The Website, and JustHealth's API server can be found running at: http://raptor.kent.ac.uk:5000. 

Whilst you are welcome to create your own account, the following are provided with example data to get a feel for how the application would look. 

+--------------------+------------+------------+ 
| Account Type       | Username   | Password   | 
+====================+============+============+ 
| Carer              | emma19     | hello123   | 
+--------------------+------------+------------+ 
| Patient            | andydavis  | hello123   | 
+--------------------+------------+------------+ 
| Admin              | admin      | admin      | 
+--------------------+------------+------------+ 

**Please note:**
There may be a large amount of notifications present on these accounts, depending on how long the application has remained inactive. 

If you desire, you can also query the API directly. For functions and parameters required, please consult the API document. You can send requests to these functions in many ways, but methods we can endorse are:

- The chrome extension `PostMan`_
- The python `requests`_ library
- CURL

Note that when HTTP Basic authentication is required, the password is the encrypted version, which be accessed by sending the plaintext password to http://raptor.kent.ac.uk:5000/api/encryptPassword. 

For the accounts above, 'hello123' resolves to:

``736300023962325f8459e6763725467521acba39baa1133736f3303bf4528d68ca518fa55a3d27b5d25cd138842d2412fc0495176b2b8fee6d161d3c778386601c572dacb94744118d45671f``

------------------------
Android
------------------------

In order to run the Android application, you have two choices:

1. Run on an emulated device
2. Run on a physical device. 

**Emulated**

The easiest way, as the developers did, would be to load the /jhApp folder of the project into `Android Studio`_, and click run at the top. Wizards for creating virtual devices should be presented as part of the setup of Android Studio. 

This will create the virtual device and load the JustHealth application. Please note that graphics quality and performance can be severely impacted by running on an emulated device, and a physical device will always give a better experience. 

**Physical**

The final Android application .apk file is available here: `JustHealth Android Application`_. Navigating to this page via an Android device's browser should be enough to be able to install the application. 

This should run on any Android device running API level 11 (also known as HONEYCOMB or 3.0) and above. 

Please note, if running on a physical device, you must be connected either directly to the kent.ac.uk network, or through VPN: (`Kent Android VPN Details`_).

------------------------
Testing Portal
------------------------

The Testing Portal can be found running at: http://raptor.kent.ac.uk:5001/portal

Here you can query tests by Iteration and filter by All/Passed/Failed to see how we tracked our testing. 

---------------
Documentation
---------------

Comprehensive documentation can be found in a number places depending on the content:

**Examiner's Guide:** Accessible from the left pane.

**User Documentation:** Available at: `User Documentation`_

**Technical Documentation:** Accessible from the left pane. 

**Android Documentation:** Available at: `Android`_

-------------
Other Links
-------------

**GitHub**

Our project is hosted on GitHub, and we used their Issue Tracking and other tools to help manage our project. You can view all of this information here: https://github.com/RichLogan/JustHealth. Issues, contributions, and all history can be viewed using the links on the right of that page. 

**Trello**

Trello is essentially an online version of an information radiator. We used it to track task assignments, due dates and progress. You can publically access and view cards from here: https://trello.com/b/GtDAe1wy/just-health

They are sorted by Iteration and have labels associating them with specific parts of the project, such as documentation, API, database etc as well as green to mark complete. Faded cards are those that have not been interacted with recently.

For both GitHub and Trello, offline versions can be found through the Corpus Index. 

.. _`JustHealth Android Application`: http://raptor.kent.ac.uk:5000/static/JustHealth.apk
.. _`Kent Android VPN Details`: http://blogs.kent.ac.uk/mobiledevices/2014/02/20/how-to-connect-to-kent-vpn-on-an-android-device/
.. _`Android Studio`: http://developer.android.com/sdk/index.html
.. _`PostMan`: https://chrome.google.com/webstore/detail/postman-rest-client/fdmmgilgnpjigdojojpjoooidkmcomcm?hl=en
.. _`requests`: http://docs.python-requests.org/en/latest/
.. _`User Documentation`: http://raptor.kent.ac.uk:5000/static/UserDocumentation/index.html
.. _`Android`: http://raptor.kent.ac.uk:5000/static/AndroidDocumentation/index.html