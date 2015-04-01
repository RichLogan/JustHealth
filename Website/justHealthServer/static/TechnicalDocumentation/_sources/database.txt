========================
Database
========================

JustHealth uses a PostgreSQL database to store its data. This database is connected to using the PeeWee Python ORM. This allows the database/SQL layer to be abstracted to a certain point, as any tables/rows become classes/objects in our application, just like any other. 

Listed below are our model definitions that define our tables, as well as any helper methods. 

-------
Models
-------

.. automodule:: justHealthServer.database
  :members: BaseModel,Client,Carer,Patient,Admin,uq8LnAWi7D,Deactivatereason,Userdeactivatereason,Relationship,Patientcarer,Appointmenttype,Appointments,Medication,Prescription,Notes,TakePrescription,Notificationtype,Notification,Reminder,Androidregistration

-----------------
Helper Functions
-----------------

.. autofunction:: justHealthServer.database.createAll
.. autofunction:: justHealthServer.database.dropAll