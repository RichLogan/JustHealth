# Generated From:
# $ pwiz.py -e postgresql -u justhealth -H penguin.kent.ac.uk -p 5432 justhealth -P dsomoid
from peewee import *

database = PostgresqlDatabase('justhealth', **{'host': 'penguin.kent.ac.uk', 'password': 'dsomoid', 'port': 5432, 'user': 'justhealth'})

class UnknownField(object):
    pass

class BaseModel(Model):
    """Base Model"""
    class Meta:
        database = database

class Client(BaseModel):
    """Represents a user of the application"""
    accountdeactivated = BooleanField()
    accountlocked = BooleanField()
    dob = DateField()
    email = CharField(max_length=100)
    loginattempts = IntegerField()
    username = CharField(max_length=25, primary_key=True)
    verified = BooleanField()

    class Meta:
        db_table = 'client'

class Carer(BaseModel):
    firstname = CharField(max_length=100)
    ismale = BooleanField()
    nhscarer = BooleanField(null=True)
    surname = CharField(max_length=100)
    username = ForeignKeyField(db_column='username', rel_model=Client, to_field='username', primary_key='username')

    class Meta:
        db_table = 'carer'

class Patient(BaseModel):
    firstname = CharField(max_length=100)
    ismale = BooleanField()
    surname = CharField(max_length=100)
    username = ForeignKeyField(db_column='username', rel_model=Client, to_field='username', primary_key='username')

    class Meta:
        db_table = 'patient'

class uq8LnAWi7D(BaseModel):
    expirydate = DateField(null=True)
    iscurrent = BooleanField(null=True)
    password = CharField(max_length=255, unique=True)
    username = ForeignKeyField(db_column='username', unique=True, rel_model=Client, to_field='username')

    class Meta:
        primary_key = CompositeKey('password, username')
        db_table = 'uq8lnawi7d'

class Deactivatereason(BaseModel):
    reason = CharField(max_length=255, primary_key=True)

    class Meta:
        db_table = 'deactivatereason'

class Userdeactivatereason(BaseModel):
    comments = CharField(max_length=1000, null=True)
    reason = ForeignKeyField(db_column='reason', null=True, rel_model=Deactivatereason, to_field='reason')

    class Meta:
        db_table = 'userdeactivatereason'
