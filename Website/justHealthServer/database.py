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
    accountdeactivated = BooleanField(default=False)
    accountlocked = BooleanField(default=False)
    dob = DateField()
    email = CharField(max_length=100)
    loginattempts = IntegerField()
    username = CharField(max_length=25, primary_key=True)
    verified = BooleanField(default=False)

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

class Relationship(BaseModel):
    code = IntegerField(null=True)
    connectionid = PrimaryKeyField()
    requestor = ForeignKeyField(db_column='requestor', null=True, rel_model=Client, to_field='username', related_name = 'requestor')
    requestortype = CharField(max_length=50, null=True)
    target = ForeignKeyField(db_column='target', null=True, rel_model=Client, to_field='username', related_name='target')
    targettype = CharField(max_length=50, null=True)

    class Meta:
        db_table = 'relationship'

class Patientcarer(BaseModel):
    carer = ForeignKeyField(db_column='carer', rel_model=Client, to_field='username', related_name='carer')
    patient = ForeignKeyField(db_column='patient', rel_model=Client, to_field='username', related_name='patient')

    class Meta:
        primary_key = CompositeKey('carer', 'patient')
        db_table = 'patientcarer'

def createAll():
    dropAll()
    Client.create_table()
    Patient.create_table()
    Carer.create_table()
    uq8LnAWi7D.create_table()
    Deactivatereason.create_table()
    Userdeactivatereason.create_table()
    Relationship.create_table()
    Patientcarer.create_table()

def dropAll():
    if Client.table_exists():
        Client.drop_table(cascade=True)

    if Patient.table_exists():
        Patient.drop_table(cascade=True)

    if Carer.table_exists():
        Carer.drop_table(cascade=True)

    if uq8LnAWi7D.table_exists():
        uq8LnAWi7D.drop_table(cascade=True)

    if Deactivatereason.table_exists():
        Deactivatereason.drop_table(cascade=True)

    if Userdeactivatereason.table_exists():
        Userdeactivatereason.drop_table(cascade=True)

    if Relationship.table_exists():
        Relationship.drop_table(cascade=True)

    if Patientcarer.table_exists():
        Patientcarer.drop_table(cascade=True)
