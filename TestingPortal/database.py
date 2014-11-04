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
    expectedresults = CharField(max_length=10000)
    iteration = IntegerField()
    prerequisites = CharField(max_length=10000, null=True)
    testid = IntegerField()
    testname = CharField(max_length=1000)
    teststeps = CharField(max_length=10000)

    class Meta:
        primary_key = CompositeKey('iteration','testid')
        db_table = 'tests'

class Run(BaseModel):
    actualresult = CharField(max_length=50)
    comments = CharField(max_length=10000, null=True)
    datetime = DateTimeField()
    issue = IntegerField(null=True)
    iteration = ForeignKeyField(db_column='iteration', rel_model=Tests, to_field='iteration')
    runid = IntegerField()
    tester = ForeignKeyField(db_column='tester', rel_model=Users, to_field='name', related_name="run.tester")
    testid = ForeignKeyField(db_column='testid', rel_model=Tests, to_field='testid', related_name="run.testid")

    class Meta:
        primary_key = CompositeKey('iteration','testid', 'runid')
        db_table = 'run'
        

class Testruns(BaseModel):
    iteration = ForeignKeyField(db_column='iteration', rel_model=Tests, to_field='iteration')
    runid = ForeignKeyField(db_column='runid', rel_model=Run, to_field='runid', related_name="Testruns.runid")
    testid = ForeignKeyField(db_column='testid', rel_model=Tests, to_field='testid', related_name="Testruns.testid")

    class Meta:
        primary_key = CompositeKey('iteration','testid','runid')
        db_table = 'testruns'