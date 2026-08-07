# Django
## Django Documentation
- [source](https://docs.djangoproject.com/en/6.1/)
### The Model Layer
#### Models
models are the definitive source of information about relational data, inheriting `django.db.models.Model`.<br>
usually, each model represents a table, & its attributes correspond to database columns.<br>
the `django.db.models.Model` class provides an automatically generated database access API.<br>
the concrete name of each model's table is derived from its metadata.

django generates the required SQL expressions based on project settings, keeping models database agnostic.<br>
to register models for use & migration, their django app must be added to the `INSTALLED_APPS` setting.<br>
> django looks for models in the `models` module of each app, so they should be defined or imported there

model fields must be subclasses of `django.db.models.Field`.<br>
each field object accepts a specific set of arguments, along with optional common arguments shared by all field types.<br>
primary key values are read-only; modifying them causes new rows to be created.

each model requires a primary key field.<br>
if a model definition lacks one, django adds an auto-incrementing primary key named `id`, with the type `django.db.models.IntegerField`, by default.<br>
this behaviour can be configured globally through the `DEFAULT_AUTO_FIELD` setting or per application through `AppConfig.default_auto_field`.

many-to-one relationships can be defined using `django.db.models.ForeignKey`.<br>
this creates a column named `<field>_id` on the associated table as its database representation.

many-to-many relationships can be defined using `django.db.models.ManyToManyField`.<br>
this creates an intermediary table as its database representation.<br>
the relationship should be defined in one of the participating models, not both.<br>
the `symmetrical` argument determines whether each row in the intermediary table for a recursive relationship has a corresponding reverse relationship.<br>
the `through` argument can specify a custom intermediary model.

one-to-one relationships can be defined using `django.db.models.OneToOneField`.

lazy relationships can reference models by name in string format. they can be
- recursive: references the containing model using `"self"`
- relative: references a model within the same application by name
- absolute: references a model in another application using the `"<app>.<model>"` format

all relational fields expect the concrete referred model or a lazy reference to it as their first positional argument.

field names must not conflict with the database access API. they must not conflict with Python keywords, contain consecutive underscores, or end with an underscore.

a nested class named `Meta` can be defined within a model's body to provide metadata, including anything that is not a field.

`Manager` is the interface through which database query operations are provided to models.<br>
a default instance is assigned to each model's `objects` attribute unless a custom manager is defined.<br>
it is accessible only through model classes, not their instances.

row-level behaviour can be defined through instance methods & properties on models.<br>
each model also has predefined instance methods that can be customized by overriding them, including
- `__str__`
- `save`
- `delete`

model inheritance can share common attributes among subclasses, specifically through abstract models.<br>
abstract models have their metadata's `abstract` attribute set to `True`, are not associated with tables & do not have instances of their own.<br>
inherited fields from abstract models can be overridden or removed by assigning `None` to them.<br>
when `related_name` is not specified for relationship fields on abstract models, the reverse name becomes `<subclass>_set` when inherited.

subclasses inherit metadata from their parent if they do not declare their own.<br>
a model's metadata is available as one of its attributes & can be extended.<br>
the `abstract` attribute of an abstract model's metadata is automatically set to `False` when inherited; it can be explicitly set to `True` to form a hierarchy of abstract models.<br>
due to the MRO, only the first parent's metadata is inherited in multiple model inheritance; a model can explicitly inherit from multiple `Meta` classes.<br>
some metadata attributes, such as `db_table`, would cause inconsistencies if inherited & are therefore removed by default from subclasses.

concrete model inheritance can define weak entities.<br>
when inheriting a concrete model
- a field of type `django.db.models.OneToOneField` is automatically set on the subclass; it can be defined explicitly by passing `True` to the `parent_link` argument
- the parent model's fields are accessible through the subclass, while their data remains in the parent's table

most concrete model metadata attributes are not inherited by subclasses, except for a few, such as `ordering` & `get_latest_by`.

proxy models can encapsulate, extend, manipulate, or modify the code-level behaviour of concrete models, including
- metadata attributes
- managers
- methods

they have their metadata's `proxy` attribute set to `True` & can be created by inheriting one non-abstract model or multiple proxy models sharing the same parent.<br>
proxy models can inherit abstract models as long as they do not define fields.

inheriting multiple concrete models with the same `id` field will fail; `django.db.models.AutoField` can be used to explicitly define the primary key field.<br>
overriding reverse relationship attributes or attributes of type `django.db.models.Field` on concrete models is not allowed by django.

[**field types**](https://docs.djangoproject.com/en/6.1/ref/models/fields/)

setting the `primary_key` argument to `True` on more than one field is not allowed.<br>
composite primary keys can be defined using `django.db.models.CompositePrimaryKey`.

arithmetic operations on `django.db.models.DateField` using `datetime.timedelta` might return `datetime.datetime` instances instead of `date` on some RDBMSs.<br>
`django.db.models.GeneratedField` can define database-level computed fields on models.<br>
the `decoder` argument of `django.db.models.JSONField` can customize the deserialization of values retrieved from the database.

[**indexes**](https://docs.djangoproject.com/en/6.1/ref/models/indexes/ )

[**meta options**](https://docs.djangoproject.com/en/6.1/ref/models/options/ )

metadata's `get_latest_by` attribute is used by managers to implement the `latest` & `earliest` methods.<br>
metadata's `managed` attribute determines whether the model's lifecycle is managed by Django migrations.<br>
metadata's `indexes` attribute can be used to define database indexes.<br>
metadata's `constraints` attribute can be used to define database constraints.

a subclass of `django.core.exceptions.ObjectDoesNotExist` is provided for each model as its `DoesNotExist` attribute.<br>
it is raised when an expected object is not found.

a subclass of `django.core.exceptions.MultipleObjectsReturned` is provided for each model as its `MultipleObjectsReturned` attribute.<br>
it is raised when multiple objects are found for the given lookups.

a subclass of `django.core.exceptions.NotUpdated` is provided for each model as its `NotUpdated` attribute.<br>
it is raised when forcing a model update does not affect any rows.
#### QuerySets
#### Migrations
#### Advanced
#### Other
### The Development Process
#### Settings
#### Applications
#### Exceptions
#### `manage.py`
### Security
### Performance & Optimization
### Common Web Application Tools
### Other Core Functionalities
## Django Rest Framework Documentation
