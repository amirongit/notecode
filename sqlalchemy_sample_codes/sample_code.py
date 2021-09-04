from sqlalchemy import (create_engine, text, insert, select, bindparam,
                        literal_column, and_, or_, func, union_all, update)
from sqlalchemy.orm import Session, registry, relationship, aliased
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey

# Any SQLAlchemy application is started by creating an Engine object.
# It is the main source to get connections from.
engine = create_engine('sqlite+pysqlite:///:memory:', echo=False, future=True)

# working with transactions and the DBAPI
# By calling connect method on and Engine object, a Connection object is
# created which can be used as a context manager.
# A Connection provides an execution method called execute.
# Execution methods are capable of executing Executable objects.
# Engine.connect returns a core level connection.
with engine.connect() as conn:
    result = conn.execute(text('SELECT \'hellow, world!\''))
    print('- - - - - - - - - -')
    print(result.all())

# When executing DDL, changes need to be commited by calling commit method on
# the Connection object.
with engine.connect() as conn:
    conn.execute(text('CREATE TABLE some_table (x int, y int)'))
    conn.execute(text('INSERT INTO some_table (x, y) VALUES (:x, :y)'),
                 [{'x': 1, 'y': 1}, {'x': 2, 'y': 2}])
    conn.commit()
    result = conn.execute(text('SELECT * FROM some_table'))
    print('- - - - - - - - - -')
    print(result.all())

# In order to avoid having to commit changes when executing DDL, a context
# manager can be provided by calling begin method on the Engine object which
# commits changes automatically after it ends.
with engine.begin() as conn:
    conn.execute(text('INSERT INTO some_table (x, y) VALUES (:x, :y)'),
                 [{'x': 6, 'y': 8}, {'x': 9, 'y': 10}])

# The return value from execution methods are in the form of Result objects,
# which are filled with Row objects which are filled with either mapped class
# objects, elements or both.
with engine.connect() as conn:
    result = conn.execute(text('SELECT x, y FROM some_table'))
    for row in result:
        print('- - - - - - - - - -')
        print(row)
    result = conn.execute(text('SELECT x, y FROM some_table'))
    for row in result:
        print('- - - - - - - - - -')
        print(f'x: {row.x}, y: {row.y}')
    result = conn.execute(text('SELECT x, y FROM some_table'))
    for row in result:
        print('- - - - - - - - - -')
        print(f'x: {row[0]}, y: {row[1]}')
    result = conn.execute(text('SELECT x, y FROM some_table'))
    for x, y in result:
        print('- - - - - - - - - -')
        print(f'x: {x}, y: {y}')
    result = conn.execute(text('SELECT x, y FROM some_table'))
    for dict_row in result.mappings():
        print('- - - - - - - - - -')
        print(f'x: {dict_row["x"]}, y: {dict_row["y"]}')

# A list of dictionaries made of single key value pairs can be passed to an
# execution method in order to pass multiple sets of parameters to an
# Executable object.
# A single dictonary can be passed to an execution method in order to pass the
# Executable object a single set of parameters.
with engine.connect() as conn:
    result = conn.execute(text('SELECT x, y FROM some_table WHERE y > :y'),
                          {'y': 2})
    for row in result:
        print('- - - - - - - - - -')
        print(f'x: {row.x}, y: {row.y}')

# bindparams method can be called on Executable objects to pass them a set of
# parameters.
with engine.connect() as conn:
    result = conn.execute(text('SELECT x, y FROM some_table WHERE y > :y ORDER'
                               ' BY x, y').bindparams(y=6))
    for row in result:
        print('- - - - - - - - - -')
        print(f'x: {row.x}, y: {row.y}')

# The interactive object in ORM level is the Session object.
# A Session object is an ORM level connection and provides an ORM level
# execution method.
with Session(engine) as sess:
    result = sess.execute(text('SELECT x, y FROM some_table WHERE y > :y ORDER'
                               ' BY x, y').bindparams(y=6))
    for row in result:
        print('- - - - - - - - - -')
        print(f'x: {row.x}, y: {row.y}')

# Like a core level connection, after executing DDL, commit method should be
# called on the Session object.
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
    conn.execute(text('INSERT INTO some_table (x, y) VALUES (:x, :y)'),
                 [{'x': 1, 'y': 1}, {'x': 2, 'y': 2}])
    conn.commit()

# In order to reflect a table from an existing database, a Table object is
# created with the same name and the engine is passed to it as a named
# argument called autoaload_with.
some_table = Table('some_table', metadata, autoload_with=engine)

# working with data
# In order to execute anything, we need an Executable object.
# An Executable object can be achived by calling functions like insert, select
# or text.
# Eeach Executable object can represent an SQL statement.
# In order to specify a set of values for Executable and ValueBased objects,
# like an insert Executable object, we can call values method on them.
insert_statement_with_values = insert(user_table).values(
        name='spongebob', fullname='Spongebob Squarepants')

# All Executable objects can be compiled to turn into raw SQL query string.
compiled = insert_statement_with_values.compile()

with engine.connect() as conn:
    result = conn.execute(insert_statement_with_values)
    conn.commit()
    # Information about the last excuted insert Executable object
    # can be accessed turough inserted_primary_key and lastrowid attributes of
    # the returned Result object.
    print('- - - - - - - - - -')
    print(result.inserted_primary_key)
    print('- - - - - - - - - -')
    print(result.lastrowid)

with engine.connect() as conn:
    result = conn.execute(insert(user_table),
                          [{'name': 'sandy', 'fullname': 'Sandy Cheeks'},
                           {'name': 'patrick', 'fullname': 'Patrick Star'}])
    conn.commit()

# bindparam function can be used in order to put dynamic parameters inside an
# Executable object.
# scalar_subquery method can be called on a select Executable object to get an
# scalar subquery.
# A scalar subquery is a subquery that returns exactly zero or one row and
# exactly one column.
scalar_subquery = select(user_table.c.id).where(
        user_table.c.name == bindparam('name')).scalar_subquery()

# In some cases, two or more Executable objects can be combined together.
# When multiple Executable objects are combined together, their parameters
# will be combined too.
with engine.connect() as conn:
    result = conn.execute(insert(address_table).values(
        user_id=scalar_subquery),
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
insert_statement = insert(address_table).from_select(
        ['user_id', 'email_address'], select_statement)


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
    print('- - - - - - - - - -')
    print(result.all()[0])

# ORM level Executable objects should be executed by an ORM level execution
# method.
# An ORM level execution method returns Result objects filled with Row objects
# which are filled with mapped class objects.
# ( Supposing that the Executable object queries something and gets some rows
# back)
orm_level_statement = select(User).where(User.name == 'spongebob')
with Session(engine) as sess:
    result = sess.execute(orm_level_statement)
    print('- - - - - - - - - -')
    print(result.all()[0])

# The from clause for a select Executable object will be generated based on
# the Table objects passed to select function in core level.
print('- - - - - - - - - -')
print(select(user_table))

# Indivisual columns to query are specified by passing Column objects into
# select function in core level.
print('- - - - - - - - - -')
print(select(user_table.c.name, user_table.c.fullname))

# The from clause for a select Executable object will be generated based on
# the mapped classes passed to select function in ORM level.
print('- - - - - - - - - -')
print(select(User))

# When an ORM level select Executable object is executed against a full
# entity, entity itself is returned within each Row object.
with Session(engine) as sess:
    result = sess.execute(select(User)).first()
    print('- - - - - - - - - -')
    print(result)

# Indivisual columns to query are specified by passing mapped class attributes
# to select function in orm level.
print('- - - - - - - - - -')
print(select(User.name, User.fullname))

# When an ORM level select Executable object is executed against
# indivisual columns of an entity, Row objects are returned filled with
# elements.
with Session(engine) as sess:
    result = sess.execute(select(User.name, User.fullname)).first()
    print('- - - - - - - - - -')
    print(result)


# Row objects can be returned filled with a mix of elements and mapped class
# objects.
with Session(engine) as sess:
    result = sess.execute(select(User.name, Address).where(
        User.id == Address.user_id).order_by(Address.id))
    print('- - - - - - - - - -')
    print(result.all())

# In order to specify as clause in a select Executable object, label method
# can be called on the Column objects passed to it.
# label method also exists on mapped class attributes referring to the columns.
# Labels will be presented as attributes in the returned Row objects by
# executing Executable objects with labeled Column objects.
labeled_select_statement = select(user_table.c.name.label('username'),
                                  user_table.c.id.label('userid'))
print('- - - - - - - - - -')
print(labeled_select_statement)
with engine.connect() as conn:
    result = conn.execute(labeled_select_statement)
    for row in result:
        print('- - - - - - - - - -')
        print(row.userid, row.username)

# A text construct can be embeded with a select Executable object in order to
# inject raw and hard coded SQL to it.
injected_select_stetement = select(text('"sample SQL"'), user_table.c.name)
print('- - - - - - - - - -')
print(injected_select_stetement)

# literal_column function is a constructor like text function but it
# explicitly represents a single Column which can be labeled.
select_statement_with_literal_column = select(literal_column(
    '"sample SQL"').label('literal column'), user_table.c.name)

# Using python operators in conjunction with a Column object generates an SQL
# expression instead of a boolean.
print('- - - - - - - - - -')
print(user_table.c.name == 'squidward')

# In order to specify where clause in a supported Executable object, a python
# expression can be passed to a method of it, called where.
print('- - - - - - - - - -')
print(select(user_table).where(user_table.c.name == 'squidward'))

# In order to produce multiple SQL expressions joined by and, where method can
# be called any number of times.
print('- - - - - - - - - -')
print(select(address_table.c.email_address).where(
        user_table.c.name == 'squidward').where(
            address_table.c.user_id == user_table.c.id))

# A single call of where method with multiple expression passed returns the
# same result.
print('- - - - - - - - - -')
print(select(address_table.c.email_address).where(
        user_table.c.name == 'squidward',
        address_table.c.user_id == user_table.c.id))

# and and or conjunctions can be used directly using and_ and or_ functions.
print('- - - - - - - - - -')
print(select(Address.email_address).where(and_(or_(
    User.name == 'squidward', User.name == 'sandy'),
    Address.user_id == User.id)))

# In order to specify where clause when querying against a single entity,
# filter_by method can be called on supported Executable objects.
# filter_by method acceptes keyword argument that match to column keys or
# mapped class attributes.
print('- - - - - - - - - -')
print(select(User).filter_by(name='spongebob',
                             fullname='Spongebob Squarepants'))

# In order to join two tables together, either join or join_from method can be
# called on supported Executable objects.
# Using join_from method, left and right side of the join can be specified
# while by using join method, the left side in inferred.
print('- - - - - - - - - -')
print(select(user_table.c.name, address_table.c.email_address).join_from(
        user_table, address_table))
print('- - - - - - - - - -')
print(select(user_table.c.name, address_table.c.email_address).join(
    address_table))

# Although from clause usally is inferred, select_from can be used on select
# Executable objects to explicitly specify from clause.
print('- - - - - - - - - -')
print(select(address_table.c.email_address).select_from(user_table).join(
    address_table))
# When the column clause of a select Executable object doesn't have enough
# information to provide from clause, select_from method can be called on it
# to specify from clause.
print('- - - - - - - - - -')
print(select(func.count('*')).select_from(user_table))

# The select construct can produce on clause to join two Table objects if
# there is a ForeignKeyConstraint definition in them.
# If there is no ForeignKeyConstraint or there are multiple definitions of
# them, it is required to specify the on clause directly.
# To do so, join and join_from methods can be called on select Executable
# objects.
print('- - - - - - - - - -')
print(select(address_table.c.email_address).select_from(user_table).join(
    address_table,
    user_table.c.id == address_table.c.user_id))

# In order to do a left outer join, isouter argument can be used in join
# method.
# In order to do a full outer join, full argument can be used in join method.
print('- - - - - - - - - -')
print(select(user_table).join(address_table, isouter=True))
print('- - - - - - - - - -')
print(select(user_table).join(address_table, full=True))
# outerjoin can be called on select Executable objects to achive the same
# result.

# In order to specify order by clause, order_by method can be called on the
# select Executable object.
print('- - - - - - - - - -')
print(select(user_table).order_by(user_table.c.name))

# asc and desc methods can be called on Column objects passed to order_by
# method in order to user ascending and descending in ordering.
print('- - - - - - - - - -')
print(select(user_table).order_by(user_table.c.name.desc()))
print('- - - - - - - - - -')
print(select(User).order_by(User.fullname.asc()))

# In order to use SQL functions, a namespace exists in sqlalchemy called func,
# which contains SQL functions and arguments can be passed to those functions.
print('- - - - - - - - - -')
print(func.count(user_table.c.id))

# In order to specify group by or having clauses, group_by and having methods
# can be called on select Executable objects.
print('- - - - - - - - - -')
print(select(User.name, func.count(Address.id).label('count')).join(
    Address).group_by(User.name).having(func.count(Address.id) > 1))

# alias method can be called on Table objects in order to get Table objects
# similar to themselves but can be used as an alias when querying in core
# level.
user_alias_1 = user_table.alias()
user_alias_2 = user_table.alias()
print('- - - - - - - - - -')
print(select(user_alias_1.c.name, user_alias_2.c.name).join_from(
    user_alias_1, user_alias_2, user_alias_1.c.id > user_alias_2.c.id))

# In order to use aliases in ORM level, aliased function can be used to get an
# Alias object.
address_alias_1 = aliased(Address)
address_alias_2 = aliased(Address)
print('- - - - - - - - - -')
print(select(User).join_from(User, address_alias_1).where(
    address_alias_1.email_address == 'patrick@sqlalchemy.org').join_from(
        User, address_alias_2).where(
            address_alias_2.email_address == 'patrick@gmail.com'))

# In order to use a select Executable object as a subquery, subquery method
# can be called on it to achive a Subqery object.
sample_subquery = select(func.count(address_table.c.id).label('count'),
                         address_table.c.user_id).group_by(
                                 address_table.c.user_id).subquery()
print('- - - - - - - - - -')
print(sample_subquery)

# Subqery objects behave like Table objects including a c attribute for the
# columns which it selects.
print('- - - - - - - - - -')
print(select(sample_subquery.c.user_id, sample_subquery.c.count))

# A Subqery object can be joined to another select Executable object.
print('- - - - - - - - - -')
print(select(user_table.c.name, user_table.c.fullname,
             sample_subquery.c.count).join_from(user_table, sample_subquery))

# CTE objects can be used just like Subqery objects, but with the ability of
# begine used in recursive style.

# union_all function can be used to merge multiple select Executable objects
# together.
print('- - - - - - - - - -')
print(union_all(select(user_table).where(user_table.c.name == 'sandy'),
                select(user_table).where(user_table.c.name == 'patrick')))

# In order to create an update Executable object, update function can be used.
# In order to specify where clause in an update Executable object, where
# method can be called on it.
# In order to specify values clause in an update Executable object, values
# method can be called on it.
print('- - - - - - - - - -')
print(update(user_table).where(user_table.c.name == 'patrick').values(
    fullname='Patrick The Star'))
