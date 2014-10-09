from peewee import *

db = PostgresqlDatabase("justhealth", host="penguin.kent.ac.uk",port=5432,user="justhealth",password="dsomoid")

class Client(Model):
    username = PrimaryKeyField()
    firstName = CharField()
    surname = CharField()
    dob = DateField()
    isMale = BooleanField()
    isCarer = BooleanField()
    email = CharField()
    verified = BooleanField()
    accountLocked = BooleanField()

    class Meta:
      database = db

class uq8LnAWi7D(Model):
    recordId = PrimaryKeyField()
    username = ForeignKeyField(Client)
    password = CharField()
    isCurrent = BooleanField()
    expiryDate = DateField()

    class Meta:
        database = db
