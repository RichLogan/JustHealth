from peewee import *

db = PostgresqlDatabase("dci29t33tqegt2", host="ec2-50-17-207-54.compute-1.amazonaws.com",port=5432,user="phweeqpzeffqac",password="9Kg9eyFSQtGX-fLxrt-LTmenj8")

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
