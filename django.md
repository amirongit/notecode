# Django
## Django Documentation
[*source*](https://docs.djangoproject.com/en/6.1/)
### The Model Layer
#### Models
models are the definitive source of information about relational data, inheriting `django.db.models.Model`.<br>
usually, each model represents a table, & its attributes correspond to database columns.<br>
`django.db.models.Model` provides an automatically generated database access API.<br>
each model's table name is derived from its metadata.

django generates SQL based on project settings, keeping models database-agnostic.<br>
to register models for use & migration, their app must be in `INSTALLED_APPS`.<br>
> django looks for models in each app's `models` module, so define or import them there

model fields must subclass `django.db.models.Field`.<br>
each field accepts a specific set of arguments, plus optional common arguments shared by all types.<br>
primary key values are read-only; modifying them creates new rows.

each model requires a primary key field.<br>
if none is defined, django adds an auto-incrementing `id` field (`django.db.models.IntegerField`) by default.<br>
this can be configured globally via `DEFAULT_AUTO_FIELD` or per-app via `AppConfig.default_auto_field`.

many-to-one relationships use `django.db.models.ForeignKey`.<br>
this creates a `<field>_id` column on the associated table.

many-to-many relationships use `django.db.models.ManyToManyField`.<br>
this creates an intermediary table.<br>
define the relationship in only one participating model.<br>
`symmetrical` determines whether recursive relationships have a reverse entry.<br>
`through` specifies a custom intermediary model.

one-to-one relationships use `django.db.models.OneToOneField`.

lazy relationships reference models by name as strings. they can be
- recursive: `"self"`
- relative: by name within the same app
- absolute: `"<app>.<model>"` for another app

all relational fields expect the concrete model or a lazy reference as their first positional argument.

field names must not conflict with the database access API, Python keywords, contain consecutive underscores, or end with an underscore.

a nested `Meta` class within a model provides metadata (anything that is not a field).

`Manager` provides database query operations to models.<br>
a default instance is assigned to `objects` unless a custom manager is defined.<br>
it is accessible only through model classes, not instances.

row-level behaviour is defined via instance methods & properties.<br>
predefined instance methods can be overridden, including
- `__str__`
- `save`
- `delete`

model inheritance shares common attributes via abstract models.<br>
abstract models set `Meta.abstract = True`, have no table & no instances.<br>
inherited fields from abstract models can be overridden or removed by assigning `None`.<br>
if `related_name` is not specified on abstract relationship fields, the reverse name becomes `<subclass>_set`.

subclasses inherit metadata from their parent if they do not declare their own.<br>
metadata is available as an attribute & can be extended.<br>
inherited `Meta.abstract` is automatically set to `False`; explicitly set it to `True` to form an abstract hierarchy.<br>
due to MRO, only the first parent's metadata is inherited in multiple inheritance; a model can explicitly inherit from multiple `Meta` classes.<br>
some metadata attributes (e.g. `db_table`) are removed by default from subclasses to avoid inconsistencies.

concrete model inheritance defines weak entities.<br>
when inheriting a concrete model
- a `django.db.models.OneToOneField` is automatically added to the subclass; define it explicitly with `parent_link=True`
- parent fields are accessible through the subclass, but data remains in the parent's table

most concrete model metadata attributes are not inherited, except a few like `ordering` & `get_latest_by`.

proxy models encapsulate, extend, manipulate, or modify code-level behaviour of concrete models, including
- metadata attributes
- managers
- methods

they set `Meta.proxy = True` & inherit one non-abstract model or multiple proxy models sharing the same parent.<br>
proxy models can inherit abstract models as long as they define no fields.

inheriting multiple concrete models with the same `id` field fails; `django.db.models.AutoField` explicitly defines the primary key.<br>
overriding reverse relationship attributes or `django.db.models.Field` attributes on concrete models is not allowed.

[*Field types*](https://docs.djangoproject.com/en/6.1/ref/models/fields/)

setting `primary_key=True` on more than one field is not allowed.<br>
composite primary keys use `django.db.models.CompositePrimaryKey`.

arithmetic on `django.db.models.DateField` with `datetime.timedelta` may return `datetime.datetime` instead of `date` on some RDBMSs.<br>
`django.db.models.GeneratedField` defines database-level computed fields.<br>
`JSONField.decoder` customizes deserialization of values from the database.

[*Indexes*](https://docs.djangoproject.com/en/6.1/ref/models/indexes/ )

[*Meta options*](https://docs.djangoproject.com/en/6.1/ref/models/options/ )

`Meta.get_latest_by` implements `Manager.latest` & `Manager.earliest`.<br>
`Meta.managed` determines whether Django migrations manage the model's lifecycle.<br>
`Meta.indexes` defines database indexes.<br>
`Meta.constraints` defines database constraints.

each model has a `DoesNotExist` exception (subclass of `django.core.exceptions.ObjectDoesNotExist`).<br>
it is raised when an expected result is not found.

each model has a `MultipleObjectsReturned` exception (subclass of `django.core.exceptions.MultipleObjectsReturned`).<br>
it is raised when multiple results match the lookups.

each model has a `NotUpdated` exception (subclass of `django.core.exceptions.NotUpdated`).<br>
it is raised when forcing an update affects no rows.

#### QuerySets
a model class & instance represent a table & a row, respectively.<br>
`<model-instance>.save` saves or updates instances.

`ForeignKey` fields can be updated with a related instance or its primary key via `<field>_id`.<br>
`ManyToManyField` fields are updated via `ManyToManyField.[add, remove]`.

model classes have at least one `Manager` on `objects` by default.<br>
`Manager`s are accessible only through model classes & construct `QuerySet`s.<br>
`[Manager, QuerySet].all` returns all rows.<br>
`[Manager, QuerySet].[filter, exclude]` refine a `QuerySet`.<br>
`[Manager, QuerySet].get` retrieves a single object.

`QuerySet`s represent row collections & may have any number of filters.<br>
construction does not trigger DB I/O until evaluation.<br>
python-like slicing (except negative indexes) adds offsets & limits.<br>
sliced `QuerySet`s cannot be further refined.<br>
python-like indexing retrieves individual results.

field lookups build SQL `WHERE` clauses via `[Manager, QuerySet].[filter, exclude, get]`.<br>
format: `<model-attribute>__lookuptype=<value>`.<br>
lookups can span related models: `<related-object>__<model-attribute>__lookuptype=<value>`.

for multi-valued relationships, `[Manager, QuerySet].filter` requires all conditions to match the same related instance.<br>
chained calls allow different related instances to satisfy each condition.<br>
`[Manager, QuerySet].exclude` does not require all conditions to match the same related instance.

`F` expressions reference aliases, model field values, their components, or operations in queries.

`QuerySet`s are cached upon evaluation, avoiding DB I/O on re-evaluation.<br>
partial evaluation (slicing, random access) does not populate the cache.

`KT` expressions reference text values of keys, indexes, or paths within `JSONField`s.

`Q` objects construct complex conditions using `&`, `|`, & `^`.

`[QuerySet, <model-instance>].delete` deletes instances.

`[QuerySet, Manager].update` updates instances.

instances with defined relationships can access related instances.<br>
related instances can access instances that relate to them.<br>
`QuerySet.[select_related, prefetch_related]` prefetch related instances on evaluation.<br>
`QuerySet.fetch_mode` sets behaviour for loading related instances.

[*QuerySet method reference*](https://docs.djangoproject.com/en/6.1/ref/models/querysets/)

`QuerySet`s are evaluated by iteration, slicing with a step, pickling, caching, or calling `[repr, len, list, bool]`.

`[QuerySet, Manager].annotate` annotates instances with
- values
- `F` expressions
- `Q` objects (boolean)
- aggregates

`[QuerySet, Manager].alias` is like `annotate`, but used only for query refinement; its computed attribute is not accessible in results.

`[QuerySet, Manager].[values, values_list]` specify returned field values or expressions.

`QuerySet.all` re-evaluates `QuerySet`s.

`[QuerySet, Manager].defer` avoids loading certain fields; accessing them triggers DB I/O.<br>
`[QuerySet, Manager].only` specifies which fields to load; accessing unloaded fields triggers DB I/O.

common aggregation function parameters
- `expressions`: model fields on which the aggregation is applied
- `output_field`: `django.db.models.Field` instance specifying the return type
- `filter`: `Q` object to filter rows
- `default`: value used when there are no rows
- `extra`: extra context

[*Lookup expressions*](https://docs.djangoproject.com/en/6.1/ref/models/lookups/)
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
