========================
Full API Listing
========================

Listed below is the complete list of possible API functionality provided by JustHealth, broken down by their general function.

All API calls require valid HTTP Basic Authentication using a registered username and encrypted password unless otherwise noted. When there is a single parameter, usually called 'details', it is a list of all post request data. The individual field will be noted in the description by [ ]. 

---------
Accounts
---------

.. autofunction:: justHealthServer.api.registerUser

.. autofunction:: justHealthServer.api.authenticate

-------------
Appointments
-------------

--------------
Connnections
--------------

.. autofunction:: justHealthServer.api.createConnection

.. autofunction:: justHealthServer.api.completeConnection

.. autofunction:: justHealthServer.api.cancelRequest

.. autofunction:: justHealthServer.api.deleteConnection

--------------
Notifications
--------------

--------------
Prescriptions
--------------

----------
Reminders
----------