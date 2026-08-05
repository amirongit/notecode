# Django
## Django Documentation
- [source](https://docs.djangoproject.com/en/6.0)
### The Model Layer
#### Models
definitive source of information about relational data, inheriting `django.db.models.Model`.<br>
usually, each model represents a table & its attributes correspond to database columns.<br>
the parent class provides an automatically generated database access API.<br>
the concrete name of the associated table for each model is derived from its metadata.

django generates the required SQL expressions based on project settings in order to keep models database agnostic.<br>
in order to register models for usage & migration, their django app needs to be added to the `INSTALLED_APPS` setting.<br>
> django will be looking for the models within the `models` module under each app, so the they should be defined or imported there

fields of a model must be subclasses of `django.db.models.Field`.<br>
each field object expects its own specific set of arguments, plus a set of common arguments shared by all field types, which are all optional.<br>
the values of primary key fields are read only & modifying them will cause new rows to be created.

each model requires exactly one field as its primary key.<br>
if a model definition lacks one, an auto-incremented primary key of type `django.db.models.IntegerField` named `id` is added by default.<br>
this behaviour can be configured through the `DEFAULT_AUTO_FIELD` setting globally or `AppConfig.default_auto_field` per application.

one-to-many relationships can be defined using `django.db.models.ForeignKey`.<br>
its second positional argument (`on_delete`) determines what happens in case of deletion of a referred row.

many-to-many relationships can be defined using `django.db.models.ManyToManyField`.<br>
this field should be put in just one of the models engaged in the relationship, not both.<br>
its `through` argument can be used to specify the intermediary model if needed.<br>
the intermediary model should define both foreign keys explicitly.<br>
the intermediary model should contain exactly one foreign key to the source model; otherwise, `through_fields` of the `django.db.models.ManyToManyField` should be used to specify the foreign key used for the many-to-many relationship.<br>
in case of recursive many-to-many relationships, the intermediary model should have exactly two foreign keys to the source model; otherwise, the above solution applies.

one-to-one relationships can be defined using `django.db.models.OneToOneField`.

all relational fields expect the referred model as their first positional argument.

field name should not conflict with the database access API; there are restrictions to prevent names which conflict with python keywords (`id` violates this!) or have consecutive underscores or trailing underscores.

a nested class named `Meta` can be defined within the body of models to give them metadata (anything that's not a field).

`Manager` is the interface through which database query operations are provided to models.<br>
a default instance of it is set as the `objects` attribute on each model if a custom one is not assigned.<br>
it is only accessible through model classes themselves & not their instances.

it is possible to define row-level behaviour in the form of instance methods & properties on models.<br>
there will be a number of predefined instance methods on each model, all of which can be customized through overriding, for example
- `__str__`
- `save`
- `delete`

model inheritance can be used to share common attributes among subclasses, which is done through abstract models.<br>
abstract models have the `abstract` attribute in their metadata set to `True`, are not associated with any tables & do not have managers or instances of their own.<br>
inherited fields from abstract models can be overridden or removed by being assigned `None`.

subclasses of models inherit metadata from their parent if they do not declare their own.<br>
metadata of a model is available as one of its attributes & can be extended.<br>
the `abstract` attribute of metadata of abstract models is automatically set to `False` when inherited; it can be explicitly set to `True` to form a hierarchy of abstract models.<br>
due to the MRO, in case of multiple model inheritance, only the first parent's metadata is inherited; it can be explicitly declared to inherit from multiple `Meta` classes.<br>
some metadata attributes such as `db_table` would cause inconsistencies if inherited.
<!-- https://docs.djangoproject.com/en/6.0/topics/db/models/#be-careful-with-related-name-and-related-query-name -->
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
