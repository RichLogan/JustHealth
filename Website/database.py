from peewee import *

db = PostgresqlDatabase("justhealth", host="penguin.kent.ac.uk",port=5432,user="justhealth",password="dsomoid")

class Client(Model):
    username = CharField(primary_key=True)
    firstname = CharField()
    surname = CharField()
    dob = DateField()
    ismale = BooleanField()
    iscarer = BooleanField()
    email = CharField()
    verified = BooleanField()
    accountlocked = BooleanField()

    class Meta:
      database = db

class uq8LnAWi7D(Model):
    recordid = PrimaryKeyField()
    username = CharField()
    password = CharField()
    iscurrent = BooleanField()
    expirydate = DateField()

    class Meta:
        database = db
