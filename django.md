# Django
## Django Documentation
[*source*](https://docs.djangoproject.com/en/6.1/)
### The Model Layer
#### Models
models are the definitive source of information about relational data, inheriting `django.db.models.Model`.<br>
usually, each model represents a table & its attributes correspond to DB columns.<br>
`django.db.models.Model` provides an automatically generated DB access API.<br>
each model's table name is derived from its metadata.

django generates SQL based on project settings, keeping models DB-agnostic.<br>
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
the relationship should be defined on just one of the participating models.<br>
`symmetrical` determines whether recursive relationships have a reverse entry.<br>
`through` specifies a custom intermediary model.

one-to-one relationships use `django.db.models.OneToOneField`.

lazy relationships reference models by name as strings; they can be
- recursive: `"self"`
- relative: by name within the same app
- absolute: `"<app>.<model>"` for another app

all relational fields expect the concrete model or a lazy reference as their first positional argument.

field names must not conflict with the DB access API, Python keywords, contain consecutive underscores or end with an underscore.

a nested `Meta` class within a model provides metadata (anything that is not a field).

`Manager`s are interfaces through which database query operations are provided on models.<br>
a default instance is assigned to `objects` attribute of models unless custom ones are defined.<br>
if custom managers are defined on models, the first one is picked as the default manager.<br>
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

proxy models encapsulate, extend, manipulate or modify code-level behaviour of concrete models, including
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
`django.db.models.GeneratedField` defines DB-level computed fields.<br>
`JSONField.decoder` customizes deserialization of values from the DB.

[*Indexes*](https://docs.djangoproject.com/en/6.1/ref/models/indexes/ )

[*Meta options*](https://docs.djangoproject.com/en/6.1/ref/models/options/ )

`Meta.get_latest_by` implements `Manager.latest` & `Manager.earliest`.<br>
`Meta.managed` determines whether Django migrations manage the model's lifecycle.<br>
`Meta.indexes` defines DB indexes.<br>
`Meta.constraints` defines DB constraints.

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
lookups can span related models: `<related-object>__<model-attribute>__...=<value>`.

for multi-valued relationships, `[Manager, QuerySet].filter` requires all conditions to match the same related instance.<br>
chained calls allow different related instances to satisfy each condition.<br>
`[Manager, QuerySet].exclude` does not require all conditions to match the same related instance.

`F` expressions describe values or computations usable to update, create, filter, order by, annotate or aggregate.

`QuerySet`s are cached upon evaluation, avoiding DB I/O on re-evaluation.<br>
partial evaluation (slicing, random access) does not populate the cache.

`KT` expressions reference text values of keys, indexes or paths within `JSONField`s.

`Q` objects construct complex conditions using `&`, `|` & `^`.

`[QuerySet, <model-instance>].delete` deletes instances.

`[Manager, QuerySet].update` updates instances.

instances with defined relationships can access related instances.<br>
related instances can access instances that relate to them.<br>
`QuerySet.[select_related, prefetch_related]` prefetch related instances on evaluation.<br>
`QuerySet.fetch_mode` sets behaviour for loading related instances.

[*QuerySet method reference*](https://docs.djangoproject.com/en/6.1/ref/models/querysets/)

`QuerySet`s are evaluated by iteration, slicing with a step, pickling, caching or calling `[repr, len, list, bool]`.

`[Manager, QuerySet].annotate` annotates results with
- values
- `F` expressions
- `Q` objects (boolean)
- aggregations

`[Manager, QuerySet].alias` is like `annotate`, but used only for query refinement; its computed attribute will not accessible in results.

`[Manager, QuerySet].[values, values_list]` specify returned field values or expressions.

`QuerySet.all` re-evaluates `QuerySet`s.

`[Manager, QuerySet].defer` avoids loading certain fields; accessing them triggers DB I/O.<br>
`[Manager, QuerySet].only` specifies which fields to load; accessing unloaded fields triggers DB I/O.

common aggregation function arguments
- `expressions`: model fields on which the aggregation is applied
- `output_field`: `django.db.models.Field` instance specifying the return type
- `filter`: `Q` object to filter rows
- `default`: value used when there are no rows
- `extra`: extra context

[*Lookup expressions*](https://docs.djangoproject.com/en/6.1/ref/models/lookups/)
#### Model Instances
`<model-instance>.refresh_from_db` reloads model fields from DB.

`[force_insert, force_update]` arguments of `<model-instance>.save` enforce inserts or updates only.<br>
`update_fields` argument of `<model-instance>.save` enforces an update & specifies which fields to save.

[*Accessing related objects*](https://docs.djangoproject.com/en/6.1/ref/models/relations/)
#### Migrations
migrations propagate model modifications into the DB.<br>
commands to interact with migrations
- `migrate`: applies migrations
- `makemigrations`: creates new migrations based on modifications
- `sqlmigrate`: displays SQL statements for a migration
- `showmigrations`: lists migrations & their status
- `squashmigrations`: squashes migrations

migrations are deterministic.<br>
migrations are subclasses of `django.db.migrations.Migration` named `Migration`.<br>
`<migration>.dependencies` specifies dependees.<br>
`<migration>.operations` contains declarative schema-change instructions as subclasses of `django.db.migrations.operations.base.Operation`.

`<migration>.initial` determines if a migration is initial.<br>
initial migrations define the whole DB schema at creation time.<br>
`--fake-initial` option of `migrate` command avoids creating tables that already exist but are defined in initial migrations.<br>
this is used when introducing django to existing projects.

data migrations alter data.<br>
`RunPython` operation runs python code in migrations.<br>
`django.apps.registry.Apps` returns a historical model version that remains relevant to the migration.

squashing is the act of reducing multiple migrations into one.

[*Operations reference*](https://docs.djangoproject.com/en/6.1/ref/migration-operations/)

[*SchemaEditor*](https://docs.djangoproject.com/en/6.1/ref/schema-editor/)

[*Writing migrations*](https://docs.djangoproject.com/en/6.1/howto/writing-migrations/)
#### Advanced
[*Managers*](https://docs.djangoproject.com/en/6.1/topics/db/managers/)

associated models are accessible via the `model` attribute of `Manager`s.<br>
`Manager.get_queryset` returns the base `QuerySet` on which further refinements are applied.

`Meta.default_manager_name` specifies the default manager.

base `Manager`s access related fields.<br>
`Meta.base_manager_name` specifies the base manager.<br>
they usually bypass default manager limitations & filters.

`QuerySet.as_manager` returns a `Manager` with the same base `QuerySet`.<br>
`Manager.from_queryset` returns a `Manager` with the given `QuerySet` as its base.<br>
custom `Manager`s should be shallow-copyable.

[*Raw SQL*](https://docs.djangoproject.com/en/6.1/topics/db/sql/)

[*Transactions*](https://docs.djangoproject.com/en/6.1/topics/db/transactions/)

by default, each statement is immediately committed unless a transaction is active.

`django.db.transaction.atomic` makes DB operations atomic by decorating callables or as a context manager.<br>
save points are markers within transactions which allow rolling back partially.<br>
nested atomic blocks are possible & will become implicit save points.<br>
transactions are committed upon completion & rolled back on raised exceptions.

[*Aggregation*](https://docs.djangoproject.com/en/6.1/topics/db/aggregation/)

`[Manager, QuerySet].aggregate` applies aggregations over all contained items.

[*Search*](https://docs.djangoproject.com/en/6.1/topics/db/search/)

[*Custom fields*](https://docs.djangoproject.com/en/6.1/howto/custom-model-fields/)

[*Multiple databases*](https://docs.djangoproject.com/en/6.1/topics/db/multi-db/)

[*Custom lookups*](https://docs.djangoproject.com/en/6.1/howto/custom-lookups/)

[*Query Expressions*](https://docs.djangoproject.com/en/6.1/ref/models/expressions/)

[*Conditional Expressions*](https://docs.djangoproject.com/en/6.1/ref/models/conditional-expressions/)

[*Database Functions*](https://docs.djangoproject.com/en/6.1/ref/models/database-functions/)
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
