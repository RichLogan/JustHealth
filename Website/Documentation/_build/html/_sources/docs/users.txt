User Functionality
===================

This document will list the key pieces of functionality that control user management. The server side code representing all of the functions can be found in the :py:mod:`accounts` module.

The application has a number of different types of users, including:

1. Patients
2. Carers
3. Relatives
4. Medical Professionals

Each user is represented by a Client record in the PostgreSQL databsae, and represented in our database by the following class:

.. automodule:: database
    :members: Client

Register
--------

The registration function is a simple form where a user can input their account information.

It takes the following input from either the Web application or the Android application through an HTTP POST request:

1. Username
2. First Name
3. Surname
4. Date of Birth
5. Gender
6. Account Type
7. Date of Birth
8. Email Address
9. Password
10. Confirm Password
11. Terms and Conditions Accept

If this passes through the valiadtion it is used to insert a new Client record:

.. automodule:: accounts
    :members:
    :undoc-members:
