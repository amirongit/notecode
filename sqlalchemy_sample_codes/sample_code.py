from sqlalchemy import create_engine, text, insert, select, bindparam
from sqlalchemy.orm import Session
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry, relationship

# Any SQLAlchemy application is started by creating an Engine object.
# It is the main source to get connections from.
engine = create_engine('sqlite+pysqlite:///:memory:', echo=False, future=True)

# working with transactions and the DBAPI
# By calling connect method on and Engine object, a Connection object is
# created which can be used as a context manager.
# A Connection provides an execution method called execute.
# Execution methods are capable of executing Executable objects.
# A Connection is a core level connection.
with engine.connect() as conn:
    result = conn.execute(text('SELECT \'hellow, world!\''))
    print(result.all())

# When executing DDL, changes need to be commited by calling commit method on
# the Connection object.
with engine.connect() as conn:
    conn.execute(text('CREATE TABLE some_table (x int, y int)'))
    conn.execute(
            text('INSERT INTO some_table (x, y) VALUES (:x, :y)'),
            [{'x': 1, 'y': 1}, {'x': 2, 'y': 2}])
    conn.commit()
    result = conn.execute(text('SELECT * FROM some_table'))
    print(result.all())

# To avoid having to commit changes when executing DDL, a context manager
# can be provided by calling begin method on the Engine object which commits
# changes automatically after it ends.
with engine.begin() as conn:
    conn.execute(
            text('INSERT INTO some_table (x, y) VALUES (:x, :y)'),
            [{'x': 6, 'y': 8}, {'x': 9, 'y': 10}])

# The return value from execution methods are in the form of Result objects,
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

# A list of dictionaries made of single key value pairs can be passed to an
# execution method in order to pass multiple sets of parameters to an
# Executable object.
# A single dictonary can be passed to an execution method in order to pass the
# Executable object a single set of parameters.
with engine.connect() as conn:
    result = conn.execute(
        text('SELECT x, y FROM some_table WHERE y > :y'),
        {'y': 2})
    for row in result:
        print(f'x: {row.x}, y: {row.y}')

# bindparams method can be called on Executable objects to pass them a set of
# parameters.
with engine.connect() as conn:
    result = conn.execute(
        text('SELECT x, y FROM some_table WHERE'
             ' y > :y ORDER BY x, y').bindparams(y=6))
    for row in result:
        print(f'x: {row.x}, y: {row.y}')

# The interactive object in ORM level is the Session object.
# Session object is used similar to Connection object and provides an
# execution method.
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
# Metadata is the data about the actual data that we are storing, like tables
# and columns.
metadata = MetaData()

# A table can be declared or reflected from an existing table in a
# database.
# In order to create a table in core level, a Table object is assigned to a
# variable which will be how the table is refered.
# A table takes a name, a MetaData object to store itself in it and a set of
# Column objects which represent columns.
user_table = Table('user_account', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('name', String(30)),
                   Column('fullname', String))


address_table = Table('address', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('user_id', ForeignKey('user_account.id'),
                             nullable=False),
                      Column('email_address', String, nullable=False))

# In a core level table, columns will be stored in an attribute called c.
# Core level tables can be emmited by calling create_all method on their
# metadata and passing it the Engine object.
metadata.create_all(engine)

# In ORM level, tables are created as mapped classes which should inherite
# from a base class.
# A mapped class is any python class that will have attributes which link to
# the columns in a table.
# In order to create a MetaData object for mapped classes, a registry should
# be created which contains a MetaData object in itself.
mapper_registry = registry()

# The base class which is needed by mapped classes can be generated by calling
# generate_base on a registry object.
# It can also be achived by calling sqlalchemy.orm.declarative_base function
Base = mapper_registry.generate_base()

# After declaring a mapped class, a core level table will be generated and
# stored in an attribute called __table__.


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

# Another method to create mapped classes is to assign a Table object to an
# attribute of the class called __table__.


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

# To reflect a table from an existing database, a Table object is created with
# the same name and the engine is passed to it as a named argument called
# autoaload_with.
some_table = Table('some_table', metadata, autoload_with=engine)

# working with data
# To execute anything, we need an Executable object.
# An Executable object can be achived by calling functions like insert, select
# or text.
# Eeach Executable object can represent an SQL statement.
# To specify a set of values for Executable and ValueBased objects, like an
# insert Executable object, we can call values method on them.
statement = insert(user_table).values(name='spongebob',
                                      fullname='Spongebob Squarepants')

# All Executable objects can be compiled to turn into raw SQL query string.
compiled = statement.compile()

with engine.connect() as conn:
    result = conn.execute(statement)
    conn.commit()
    # Information about the last excuted insert Executable object
    #can be accessed turough inserted_primary_key and lastrowid attributes of
    # the returned Result object.
    print(result.inserted_primary_key)
    print(result.lastrowid)

with engine.connect() as conn:
    result = conn.execute(insert(user_table),
                          [{'name': 'sandy', 'fullname': 'Sandy Cheeks'},
                           {'name': 'patrick', 'fullname': 'Patrick Star'}])
    conn.commit()

# bindparam function can be used in order to put dynamic parameters inside an
# Executable object.
# scalar_subquery method can be called on a select Executable object which is
# going to return multiple rows in order to make it able to be combined with
# another Executable object.
scalar_subquery = select(user_table.c.id).where(
        user_table.c.name == bindparam('name')).scalar_subquery()

# In some cases, two or more Executable objects can be combined together.
# When multiple Executable objects are combined together, their parameters
# will be combined too.
with engine.connect() as conn:
    result = conn.execute(
            insert(address_table).values(user_id=scalar_subquery),
            [{'name': 'spongebob',
              'email_address': 'spongebob@sqlalchemy.org'},
             {'name': 'sandy',
              'email_address': 'sandy@sqlalchemy.org'}])
    conn.commit()

# If a select Executable object is going to return a single row, it can be
# combined with other Executable objects without calling any methods on it.
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

# Executable objects can be used in both ORM and core level.

# Core level Executable objects should be executed by a core level execution
# method.
# A core level execution method returns Result objects filled with Row objects
# which are filled with elements.
# ( Supposing that the Executable object queries something and gets some rows
# back)
core_level_statement = select(user_table).where(
        user_table.c.name == 'spongebob')
with engine.connect() as conn:
    result = conn.execute(core_level_statement)
    print(result.all()[0])

# ORM level Executable objects should be executed by an ORM level execution
# method.
# An ORM level execution method returns Result objects filled with Row objects
# which are filled with mapped class objects.
# ( Supposing that the Executable object queries something and gets some rows
# back)
orm_level_statement = select(User).where(
        User.name == 'spongebob')
with Session(engine) as sess:
    result = sess.execute(orm_level_statement)
    print(result.all()[0])

# The from clause for a select Executable object will be generated based on
# the Table objects passed to select function in core level.
print(select(user_table))

# Indivisual columns to query are specified by passing Column objects into
# select function in core level.
print(select(user_table.c.name, user_table.c.fullname))

# The from clause for a select Executable object will be generated based on
# the mapped classes passed to select function in ORM level.
print(select(User))

# When an ORM level select Executable object is executed against a full
# entity, entity itself is returned within each Row object.
with Session(engine) as sess:
    result = sess.execute(select(User)).first()
    print(result)

# Indivisual columns to query are specified by passing mapped class attributes
# to select function in orm level.
print(select(User.name, User.fullname))

# When an ORM level select Executable object is executed against
# indivisual columns of an entity, Row objects are returned filled with
# elements.
with Session(engine) as sess:
    result = sess.execute(select(User.name, User.fullname)).first()
    print(result)


# Row objects can be returned filled with a mix of elements and mapped class
# objects.
with Session(engine) as sess:
    result = sess.execute(
            select(User.name, Address).where(
                User.id == Address.user_id).order_by(
                    Address.id)
            )
    print(result.all())
