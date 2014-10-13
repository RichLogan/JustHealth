# Generated From:
# $ pwiz.py -e postgresql -u justhealthtest -H penguin.kent.ac.uk -p 5432 justhealthtest -P rded$or
from peewee import *

database = PostgresqlDatabase('justhealthtest', **{'host': 'penguin.kent.ac.uk', 'password': 'rded$or', 'port': 5432, 'user': 'justhealthtest'})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class Client(BaseModel):
    accountlocked = BooleanField()
    dob = DateField()
    email = CharField(max_length=100)
    firstname = CharField(max_length=100)
    iscarer = BooleanField()
    ismale = BooleanField()
    surname = CharField(max_length=100)
    username = CharField(max_length=25, primary_key=True)
    verified = BooleanField()
    accountlocked = BooleanField()

    class Meta:
        db_table = 'client'

class uq8LnAWi7D(BaseModel):
    expirydate = DateField(null=True)
    iscurrent = BooleanField(null=True)
    password = CharField(max_length=255)
    recordid = PrimaryKeyField()
    username = ForeignKeyField(db_column='username', rel_model=Client, to_field='username')

    class Meta:
        db_table = 'uq8lnawi7d'
