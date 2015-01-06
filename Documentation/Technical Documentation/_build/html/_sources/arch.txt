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

-----------------------------------
The API server and Web Application
-----------------------------------

JustHealth's API server and web application is written in `Python <https://www.python.org/>`_ using a web framework called `Flask <http://flask.pocoo.org/>`_.

We chose to use Python/Flask as one developer (Rich) had previous positive experience with in during his placement year.

It is very easy to learn and very logical to use, allowing us to build the functionality we wanted quickly and easily, most probably more so than if we had used the language we already had in common, `PHP <http://php.net>`_. Besides it being simple, it was also great exposure to an entire new language and different way of thinking.

--------
The ORM
--------

An Object Relational Mapper allows us to interact with our database from our application as though tables were classes and records are objects in Python. This negates the need to write SQL and effectively somewhat abstracts the database layer, acting no different to any other part of the application. Models (tables) can be easily interacted with once defined, and the lack of SQL being written anywhere has the added benefit of eliminating the possibility of SQL injection attacks.

We used the Object Relational Mapper known as `peewee <https://github.com/coleifer/peewee>`_. Peewee is very lightweight and, again, highly logical to understand and use. It's full documentation can be found here: http://peewee.readthedocs.org/en/latest/. Incidentally, the peewee documentation, which is extremely helpful, served as the inspiration for JustHealth's documentation.

------------
The Database
------------

Behind the application is a `PostgreSQL <http://www.postgresql.org/>`_ database hosted on http://penguin.kent.ac.uk. This is provided by the University.

There is also a mirror of this database which is used for testing.

--------------------
The Web application
--------------------

------------------------
The Android application
------------------------

-------------
Documentation
-------------
