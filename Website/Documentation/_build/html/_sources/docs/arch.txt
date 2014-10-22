Architecture
======================================

The JustHealth web application is a simple and lightweight application.

It consists of three distinct parts:

1. The application code itself
2. A PostgreSQL database
3. An ORM that connects the application to the database

The Application Code
--------------------

The application is written in `Python <https://www.python.org/>`_ using a web framework called `Flask <http://flask.pocoo.org/>`_

We chose to use Python/Flask as one developer (Rich) had previous positive experience with in during his placement year. It was easy to learn and very logical to use, allowing us to build the functionality we wanted quickly.

The Database
------------

Behind the application is a `postgreSQL <http://www.postgresql.org/>`_ database hosted on http://penguin.kent.ac.uk. This is provided by the University.

The ORM
-------

The final piece is an Object Relational Mapper known as `peewee <https://github.com/coleifer/peewee>`_. An Object Relational Mapper allows us to interact with our database from our application as though it was an object in Python. This negates the need to write SQL and the weaknesses associated with it, such as SQL injection attacks.

peewee is very lightweight and, again, highly logical to understand and use. It's full documentation can be found here: http://peewee.readthedocs.org/en/latest/ and will be referenced throughout.
