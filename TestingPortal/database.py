from peewee import *

database = PostgresqlDatabase('justhealthtestcase', **{'host': 'penguin.kent.ac.uk', 'password': 'ynu7mit', 'port': 5432, 'user': 'justhealthtestcase'})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class Users(BaseModel):
    name = CharField(max_length=100, primary_key=True)
    role = CharField(max_length=100, null=True)

    class Meta:
        db_table = 'users'

class Tests(BaseModel):
    applicationtype = CharField(max_length=50)
    author = ForeignKeyField(db_column='author', rel_model=Users, to_field='name')
    autoid_test = IntegerField()
    expectedresults = CharField(max_length=10000)
    iteration = IntegerField()
    prerequisites = CharField(max_length=10000, null=True)
    testid = IntegerField()
    testname = CharField(max_length=1000)
    teststeps = CharField(max_length=10000)
    latesttestresult = CharField(max_length=15)

    class Meta:
        db_table = 'tests'
        primary_key = CompositeKey('iteration','testid')

class Run(BaseModel):
    actualresult = CharField(max_length=50)
    autoid_run = PrimaryKeyField()
    autoid_test = ForeignKeyField(db_column='autoid_test', rel_model=Tests, to_field='autoid_test')
    comments = CharField(max_length=10000, null=True)
    datetime = DateTimeField()
    issue = IntegerField(null=True)
    runid = IntegerField()
    tester = ForeignKeyField(db_column='tester', rel_model=Users, to_field='name')

    class Meta:
        db_table = 'run'

class Testruns(BaseModel):
    autoid_run = ForeignKeyField(db_column='autoid_run', rel_model=Run, to_field='autoid_run')
    autoid_test = ForeignKeyField(db_column='autoid_test', rel_model=Tests, to_field='autoid_test')

    class Meta:
        db_table = 'testruns'