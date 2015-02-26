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
    profilepicture = CharField(max_length=100, null=True)
    telephonenumber = CharField(max_length=100, null=True)
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
    password = CharField(max_length=255)
    username = ForeignKeyField(db_column='username', rel_model=Client, to_field='username')

    class Meta:
        primary_key = CompositeKey('password', 'username')
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

class Appointmenttype(BaseModel):
    type = CharField(max_length=25, primary_key=True)

    class Meta:
        db_table = 'appointmenttype'

class Appointments(BaseModel):
    appid = PrimaryKeyField()
    creator = ForeignKeyField(db_column='creator', rel_model=Client, to_field='username', related_name='creator')
    invitee = ForeignKeyField(db_column='invitee', rel_model=Client, to_field='username', null=True, related_name='invitee')
    name = CharField(max_length=1000)
    apptype = ForeignKeyField(db_column='apptype', rel_model=Appointmenttype, to_field='type', null=True, related_name='apptype')
    addressnamenumber = CharField(max_length=50, null=True)
    postcode = CharField(max_length=8, null=True)
    startdate = DateField()
    starttime = TimeField(formats='%H:%M')
    enddate = DateField()
    endtime = TimeField(formats='%H:%M')
    description = CharField(max_length=5000, null=True)
    private = BooleanField()
    androideventid = IntegerField(null=True)
    accepted = BooleanField(null=True)

    class Meta:
        db_table = 'appointments'

class Medication(BaseModel):
    name = CharField(primary_key=True)

    class Meta:
        db_table = 'medication'

class Prescription(BaseModel):
    prescriptionid = PrimaryKeyField()
    username = ForeignKeyField(db_column='username', rel_model=Client, to_field='username')
    medication = ForeignKeyField(db_column='name', rel_model=Medication, to_field='name')
    dosage = IntegerField(null=True)
    dosageunit = CharField(null=True)
    frequency = CharField(max_length=25, null=True)
    quantity = IntegerField(null=True)
    startdate = DateField(null=True)
    enddate = DateField(null=True)
    stockleft = IntegerField(null=True)
    prerequisite = CharField(null=True)
    dosageform = CharField(null=True)

    class Meta:
        db_table = 'prescription'

class Notificationtype(BaseModel):
    typename = CharField(max_length=25, primary_key=True)
    typeclass = CharField(max_length=25)

    class Meta:
        db_table = 'notificationtype'

class Notification(BaseModel):
    notificationid = PrimaryKeyField()
    username = ForeignKeyField(db_column='username', rel_model=Client, to_field="username")
    notificationtype = ForeignKeyField(db_column='notificationtype', rel_model=Notificationtype, to_field="typename")
    dismissed = BooleanField(default=False)
    relatedObject = IntegerField(null=True)
    relatedObjectTable = CharField(null=True)

    class Meta:
        db_table = 'notification'

class Reminder(BaseModel):
    reminder = PrimaryKeyField()
    username = ForeignKeyField(db_column='username', rel_model=Client, to_field="username")
    content = CharField(max_length=100)
    reminderClass = CharField(max_length=10)
    relatedObject = IntegerField()
    relatedObjectTable = CharField()
    extraDate = CharField(null=True)

class Androidregistration(BaseModel):
    username = ForeignKeyField(db_column='username', rel_model=Client, to_field="username")
    registrationid = CharField(unique=True)

    class Meta:
        db_table = 'androidregistration'

def createAll():
    """Creates all tables, dropping old instances if they exist"""
    dropAll()
    Client.create_table()
    Carer.create_table()
    Patient.create_table()
    uq8LnAWi7D.create_table()
    Deactivatereason.create_table()
    Userdeactivatereason.create_table()
    Relationship.create_table()
    Patientcarer.create_table()
    Appointmenttype.create_table()
    Appointments.create_table()
    Medication.create_table()
    Prescription.create_table()
    Notificationtype.create_table()
    Notification.create_table()
    Reminder.create_table()
    Androidregistration.create_table()

def dropAll():
    """Drops all tables providing that they exists"""
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
    if Appointments.table_exists():
        Appointments.drop_table(cascade=True)
    if Medication.table_exists():
        Medication.drop_table(cascade=True)
    if Prescription.table_exists():
        Prescription.drop_table(cascade=True)
    if Notificationtype.table_exists():
        Notificationtype.drop_table(cascade=True)
    if Notification.table_exists():
        Notification.drop_table(cascade=True)
    if Reminder.table_exists():
        Reminder.drop_table(cascade=True)
    if Androidregistration.table_exists():
        Androidregistration.drop_table(cascade=True)
