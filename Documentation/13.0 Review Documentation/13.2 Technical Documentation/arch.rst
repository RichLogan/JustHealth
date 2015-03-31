=============
Architecture
=============

The JustHealth application is a simple and lightweight application.

It consists of 6 distinct parts:

1. The core application server and API
#. An object-relational mapper to interact with the database
#. A PostgreSQL database
#. A Web application for desktop users
#. An Android application for mobile users
#. This documentation

-----------------
Overall Structure
-----------------

Image of structure here.

-----------------------------------
The API server
-----------------------------------

JustHealth's API server is written in `Python <https://www.python.org/>`_ using a framework called `Flask <http://flask.pocoo.org/>`_. This allows us to write Python functions that map to views (URLs) that can either simply return data or load data into web pages through the use of the `Jinja 2 <http://jinja.pocoo.org/>`_ templating system which is included with Flask.

We have chosen to use Python/Flask as one developer (Rich) has had previous, highly positive, experience with all aspects of it during his placement year.

Flask is very easy to learn and very logical to use, allowing us to build functionality quickly and easily, most probably more so than if we had used the language we already had in common, `PHP <http://php.net>`_. Besides it being simple, it has also given great exposure to an entirely new language and different way of thinking.

We chose to design our application using a central server connected to the database which provides an accessible and secured API to expose functionality to the Web client and the Android client. This allows us only have to write core functionality in one place, and then simply implement these API calls onto the Web and Android application. It also has the added benefit of allowing any further applications to be written without requiring access to the server or database, which is vital if third party developers would like to develop a client for JustHealth.

As the Web Application is essentially part of the API server from a structural point of view, these function calls can be made internally. Accessing them from another client (e.g the Android application) requires the use of POST requests to the server which return the required information in JSON.

--------
The ORM
--------

An Object Relational Mapper allows us to interact with our database from our application as though tables were classes and records are objects in Python. This negates the need to write SQL and effectively somewhat abstracts the database layer, acting no different to any other part of the application. Models (tables) can be easily interacted with once defined, and the lack of SQL being written anywhere has the added benefit of eliminating the possibility of SQL injection attacks.

As Flask does not come prepackaged with an ORM, or other way to interact with a database, we used the Object Relational Mapper known as `peewee <https://github.com/coleifer/peewee>`_. Peewee is very lightweight and, again, highly logical to understand and use. It's full documentation can be found here: http://peewee.readthedocs.org/en/latest/. Incidentally, the peewee documentation, which is extremely helpful, served as the inspiration for JustHealth's documentation.

------------
The Database
------------

Behind the application is a `PostgreSQL <http://www.postgresql.org/>`_ database hosted on http://penguin.kent.ac.uk. This is provided and hosted by the University. We chose to use PostgreSQL due to the experience we had with the database software learned in our second year modules and the knowledge that it is easy to connect to PeeWee through the use of the `PsyCopg2 <http://initd.org/psycopg/>`_ driver.

We also had a mirror of this database to run our tests against, and a third database to store the results of our tests through the JustHealth testing portal.

--------------------
The Web application
--------------------

The Web application is considered a client of the server, much like the Android application. However, from a technical perspective it is integrated as part of the same Flask application as the API server, just for ease of creation and management. This also allows us to call the API methods from the Web Application internally, meaning we do not have to pass requests across the Internet, and avoiding the possiblility of problems arising from violating the Same-Origin policy. 

------------------------
The Android application
------------------------

JustHealth had decided to build its mobile application on the Android platform as opposed to any other as their research showed that this was the most widely used system and therefore, would allow us to be able to target as many users as possible. 

The Android application relies heavily on the API, accessing that functionality via HTTP POST request. 

In addition to calling and displaying API results, the main extra functionality of the Android application was:

1. Push Notifications using Google’s Cloud Messaging Service (GCM)
2. Integration with Android’s Native Calendar
3. Asynchronous Processing

Push Notifications involved working with Google's Cloud Messaging Service in order to push data to Android devices through the OS, the standard practise for applications requiring to alert their users. 

The native calender integration involved working with android on a lower level, and also working with version related issues that came into play depending on how evolved calendar interaction was on a specific Android SDK version. 

Asynchronous Processing and Thread Management was also used in order to ensure that the Android application was never waiting for requests to finish, and would not appear to freeze to the user. This meant loading in data quietly after a user loaded a page, or displaying a loading icon where the former would not make sense. 

-------------
Documentation
-------------

Comprehensive documentation can be found in a number places depending on the content:

**Examiner's Guide:** Accessible from the left pane.

**User Documentation:** Available at: 

**Technical Documentation:** Accessible from the left pane. 

**Corpus Index:** Available at: 