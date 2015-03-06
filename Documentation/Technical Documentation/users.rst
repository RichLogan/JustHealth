===================
User Functionality
===================

This document will list the key pieces of functionality that control user management.

The application has a number of different types of users, including:

1. Patients
2. Carers
3. Relatives
4. Medical Professionals

Each user is represented by a Client record in the PostgreSQL databsae, and represented in our database by the following class:

.. automodule:: justHealthServer.database
    :members: Client
    :noindex:
