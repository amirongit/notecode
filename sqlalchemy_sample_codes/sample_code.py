from sqlalchemy import create_engine, text, insert, select, bindparam
from sqlalchemy.orm import Session
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry, relationship

# engine provides some interfaces for us to connect to the database, like
# connections, and also has a pool to manage all of our stablished
# connections.
engine = create_engine('sqlite+pysqlite:///:memory:', echo=False, future=True)

# working with transactions and the DBAPI
# using connect method, we can get a connection, which provides a method
# called execute, which executes executable objects
# a connection is a core level front-end.
with engine.connect() as conn:
    # the text method takes a query string and returns an statement which is
    # an executable object.
    result = conn.execute(text('SELECT \'hellow, world!\''))
    print(result.all())

# when executing DDL, we have to commit the changes using commit method on
# connection object.
with engine.connect() as conn:
    conn.execute(text('CREATE TABLE some_table (x int, y int)'))
    conn.execute(
            text('INSERT INTO some_table (x, y) VALUES (:x, :y)'),
            [{'x': 1, 'y': 1}, {'x': 2, 'y': 2}])
    conn.commit()
    result = conn.execute(text('SELECT * FROM some_table'))
    print(result.all())

# to avoid using commit method when executing DDL, we can use begin method on
# engine object instead of connect.
# this way, after the last line of the context manager, our changes will be
# commited automatically.
with engine.begin() as conn:
    conn.execute(
            text('INSERT INTO some_table (x, y) VALUES (:x, :y)'),
            [{'x': 6, 'y': 8}, {'x': 9, 'y': 10}])

# the returned object by running statements are in the form of Result objects,
# whose use cases is shown below.
with engine.connect() as conn:
    result = conn.execute(text('SELECT x, y FROM some_table'))
    for row in result:
        print(row)
    result = conn.execute(text('SELECT x, y FROM some_table'))
    for row in result:
        print(f'x: {row.x}, y: {row.y}')
    result = conn.execute(text('SELECT x, y FROM some_table'))
    for row in result:
        print(f'x: {row[0]}, y: {row[1]}')
    result = conn.execute(text('SELECT x, y FROM some_table'))
    for x, y in result:
        print(f'x: {x}, y: {y}')
    result = conn.execute(text('SELECT x, y FROM some_table'))
    for dict_row in result.mappings():
        print(f'x: {dict_row["x"]}, y: {dict_row["y"]}')

# to pass multiple parameters to a statement, we can pass a list of dictonaries
# made of keys and the values of parameters to the excution function.
# or if we want to pass a single parameter, we can pass it just one dictonary.
with engine.connect() as conn:
    result = conn.execute(
        text('SELECT x, y FROM some_table WHERE y > :y'),
        {'y': 2})
    for row in result:
        print(f'x: {row.x}, y: {row.y}')

# also we can call bindparams method on an executable object to pass it a
# single parameter.
with engine.connect() as conn:
    result = conn.execute(
        text('SELECT x, y FROM some_table WHERE'
             ' y > :y ORDER BY x, y').bindparams(y=6))
    for row in result:
        print(f'x: {row.x}, y: {row.y}')

# the interactive object to use in ORM level is session, it is used similar to
# connection.
with Session(engine) as sess:
    result = sess.execute(
            text('SELECT x, y FROM some_table WHERE'
                 ' y > :y ORDER BY x, y').bindparams(y=6))
    for row in result:
        print(f'x: {row.x}, y: {row.y}')

with Session(engine) as sess:
    result = sess.execute(text('UPDATE some_table SET y=:y WHERE x=:x'),
                          [{'x': 9, 'y': 11}, {'x': 13, 'y': 15}])
    sess.commit()

# working with database metadata
# the metadata is the data about the actual data that we are storing, like
# table name and columns.
metadata = MetaData()

# a table can be decleared or reflected from an existing table in the
# database.
# to create a table in core level, we assign a table object to a variable
# which will be how we refer to the table.
# a table takes a name, a metadata to store itself in it and a set of column
# objects which represent columns.
user_table = Table('user_account', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('name', String(30)),
                   Column('fullname', String))


address_table = Table('address', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('user_id', ForeignKey('user_account.id'),
                             nullable=False),
                      Column('email_address', String, nullable=False))

# in a core level table, columns will be stored in an attribute called c.
# after declearing tables, we can emmit them buy calling create_all method on
# it's metadata and passing it the engine.
metadata.create_all(engine)

# to get a metdata in ORM level, we should create a registry object which
# contains a metadata in itself.
mapper_registry = registry()

# a mapped class represents a table in ORM level, so to create a table, we
# need a base class to inherit from, to get this base calss, we call
# generate_base method on our registry object.
# we can also use sqlalchemy.orm.declarative_base function to get a base
# class.
Base = mapper_registry.generate_base()

# a mapped class is any python class we would like to create, which will then
# have attributes linked to table columns.
# a table object will be stored inside a mapped class in a class variable
# callde __table__.


class User(Base):
    __tablename__ = 'user_account'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    addresses = relationship('Address', back_populates='user')

    def __repr__(self):
        return (f'User(id={self.id!r}, name={self.name!r},'
                f' fullname={self.fullname!r})')


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(ForeignKey('user_account.id'), nullable=False)
    user = relationship('User', back_populates='addresses')

    def __repr__(self):
        return f'Address(id={self.id!r}, email_address={self.email_address!r})'


mapper_registry.metadata.create_all(engine)

# another method to create mapped classes is to put a table object directly in
# it.


class UserHybrid(Base):
    __table__ = user_table
    addresses = relationship('AddressHybrid', back_populates='user')

    def __repr__(self):
        return (f'User(id={self.id!r}, name={self.name!r},'
                f' fullname={self.fullname!r})')


class AddressHybrid(Base):
    __table__ = address_table
    user = relationship('UserHybrid', back_populates='addresses')

    def __repr__(self):
        return f'Address(id={self.id!r}, email_address={self.email_address!r})'


mapper_registry.metadata.create_all(engine)


with engine.connect() as conn:
    conn.execute(
            text('INSERT INTO some_table (x, y) VALUES (:x, :y)'),
            [{'x': 1, 'y': 1}, {'x': 2, 'y': 2}])
    conn.commit()

# to reflect a table from an existing database, we create a table with the
# same name and pass it the engine connected to the database as autoaload_with
# parameter.
some_table = Table('some_table', metadata, autoload_with=engine)

# working with data
# to insert data in core level, we should create an insert statement using
# insert function.
# all statements are executable objects.
# to specify one set of values for the insert statement, we can call values
# method on the returned object and pass our values to it.
statement = insert(user_table).values(name='spongebob',
                                      fullname='Spongebob Squarepants')

# all statements can be compiled to turn in to raw SQL.
compiled = statement.compile()

with engine.connect() as conn:
    result = conn.execute(statement)
    conn.commit()
    # information about the last transaction can be accessed turough
    # attributes.
    print(result.inserted_primary_key)
    print(result.lastrowid)

# if we have more than one set of values to insert, we can pass them to
# execute function instead of values method.
with engine.connect() as conn:
    result = conn.execute(insert(user_table),
                          [{'name': 'sandy', 'fullname': 'Sandy Cheeks'},
                           {'name': 'patrick', 'fullname': 'Patrick Star'}])
    conn.commit()

# select is another type of statements.
# we can specify the where caluse by passing a conditional python statement to
# it.
# to use the result of a select statement which can return multiple rows, we
# can call scalar_subquery on it.
# to put dynamic parameters inside an statement we can use bindparam
# function.
scalar_subquery = select(user_table.c.id).where(
        user_table.c.name == bindparam('name')).scalar_subquery()

# in above select statement, we get the id of a user with the given name, in
# blow statement, we use this id to match it with the inserted email.
# the select statement takes a name parameter, and the insert statement takes
# an email parameter, both statements are combined together so as their
# parameters.
with engine.connect() as conn:
    result = conn.execute(
            insert(address_table).values(user_id=scalar_subquery),
            [{'name': 'spongebob',
              'email_address': 'spongebob@sqlalchemy.org'},
             {'name': 'sandy',
              'email_address': 'sandy@sqlalchemy.org'}])
    conn.commit()

# another way to combine a select statement with an insert is to use
# from_select method on the insert statement, specifying the
# parameter swhich will be returned by the select statement.
select_statement = select(user_table.c.id,
                          user_table.c.name + '@sqlalchemy.org').where(
                user_table.c.name == 'patrick')
insert_statement = insert(
        address_table).from_select(
                ['user_id', 'email_address'],
                select_statement)


with engine.connect() as conn:
    result = conn.execute(insert_statement)
    conn.commit()

# we can make use of select statement in ORM level, this way the statement
# should be executed using an ORM leve execution method like Session.execute.
statement = select(User).where(
        User.name == 'spongebob')

# we get a set of row objects when executing a select statement in core level.
with engine.connect() as conn:
    result = conn.execute(
        select(user_table).where(user_table.c.name == 'spongebob')
    )
    print(result.all()[0])

# we get a set of mapped class objects when executing a select statement in
# ORM level.
with Session(engine) as sess:
    result = sess.execute(
        select(User).where(User.name == 'spongebob')
    )
    print(result.all()[0])
