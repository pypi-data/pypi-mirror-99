Simple SQL based tagging
and the associated `sqltags` command line script,
supporting both tagged named objects and tagged timestamped log entries.

*Latest release 20210321*:
Drop logic now merged with cs.sqlalchemy_utils, use the new default session stuff.

Compared to `cs.fstags` and its associated `fstags` command,
this is oriented towards large numbers of items
not naturally associated with filesystem objects.
My initial use case is an activity log,
but I'm probably going to use it for ontologies as well.

Many basic tasks can be performed with the `sqltags` command line utility,
documented under the `SQLTagsCommand` class below.

## Class `BaseSQLTagsCommand(cs.cmdutils.BaseCommand,cs.tagset.TagsCommandMixin)`

Common features for commands oriented around an `SQLTags` database.

### `BaseSQLTagsCommand.TAGSETS_CLASS`

### `BaseSQLTagsCommand.TAGSET_CRITERION_CLASS`

### `BaseSQLTagsCommand.TAG_BASED_TEST_CLASS`

### Method `BaseSQLTagsCommand.apply_defaults(self)`

Set up the default values in `options`.

### Method `BaseSQLTagsCommand.apply_opt(self, opt, val)`

Apply a command line option.

### Method `BaseSQLTagsCommand.cmd_edit(self, argv)`

Usage: edit criteria...
Edit the entities specified by criteria.

### Method `BaseSQLTagsCommand.cmd_export(self, argv)`

Usage: {cmd} {{tag[=value]|-tag}}...
Export entities matching all the constraints.
The output format is CSV data with the following columns:
* `unixtime`: the entity unixtime, a float
* `id`: the entity database row id, an integer
* `name`: the entity name
* `tags`: a column per `Tag`

### Method `BaseSQLTagsCommand.cmd_find(self, argv)`

Usage: {cmd} [-o output_format] {{tag[=value]|-tag}}...
List entities matching all the constraints.
-o output_format
            Use output_format as a Python format string to lay out
            the listing.
            Default: {FIND_OUTPUT_FORMAT_DEFAULT}

### Method `BaseSQLTagsCommand.cmd_import(self, argv)`

Usage: {cmd} [{{-u|--update}}] {{-|srcpath}}...
  Import CSV data in the format emitted by "export".
  Each argument is a file path or "-", indicating standard input.
  -u, --update  If a named entity already exists then update its tags.
                Otherwise this will be seen as a conflict
                and the import aborted.

TODO: should this be a transaction so that an import is all or nothing?

### Method `BaseSQLTagsCommand.cmd_init(self, argv)`

Usage: {cmd}
Initialise the database.
This includes defining the schema and making the root metanode.

### Method `BaseSQLTagsCommand.cmd_log(self, argv)`

Record a log entry.

Usage: {cmd} [-c category,...] [-d when] [-D strptime] {{-|headline}} [tags...]
  Record entries into the database.
  If headline is '-', read headlines from standard input.
  -c categories
    Specify the categories for this log entry.
    The default is to recognise a leading CAT,CAT,...: prefix.
  -d when
    Use when, an ISO8601 date, as the log entry timestamp.
  -D strptime
    Read the time from the start of the headline
    according to the provided strptime specification.

### Method `BaseSQLTagsCommand.cmd_tag(self, argv)`

Usage: {cmd} {{-|entity-name}} {{tag[=value]|-tag}}...
Tag an entity with multiple tags.
With the form "-tag", remove that tag from the direct tags.
A entity-name named "-" indicates that entity-names should
be read from the standard input.

### Method `BaseSQLTagsCommand.parse_tagset_criterion(arg, tag_based_test_class=None)`

Parse tag criteria from `argv`.

The criteria may be either:
* an integer specifying a `Tag` id
* a sequence of tag criteria

### Method `BaseSQLTagsCommand.run_context(self)`

Prepare the `SQLTags` around each command invocation.

## Function `glob2like(glob: str) -> str`

Convert a filename glob to an SQL LIKE pattern.

## Function `main(argv=None)`

Command line mode.

## Function `prefix2like(prefix: str, esc='\\') -> str`

Convert a prefix string to an SQL LIKE pattern.

## Class `SQLParameters(SQLParameters,builtins.tuple)`

The parameters required for constructing queries
or extending queries with JOINs.

Attributes:
* `criterion`: the source criterion, usually an `SQTCriterion` subinstance
* `alias`: an alias of the source table for use in queries
* `entity_id_column`: the `entities` id column,
  `alias.id` if the alias is of `entities`,
  `alias.entity_id` if the alias is of `tags`
* `constraint`: a filter query based on `alias`

## Class `SQLTagBasedTest(cs.tagset.TagBasedTest,cs.tagset.TagBasedTest,builtins.tuple,SQTCriterion,cs.tagset.TagSetCriterion)`

A `cs.tagset.TagBasedTest` extended with a `.sql_parameters` method.

### Method `SQLTagBasedTest.match_tagged_entity(self, te: cs.tagset.TagSet) -> bool`

Match this criterion against `te`.

## Class `SQLTagProxies`

A proxy for the tags supporting Python comparison => `SQLParameters`.

Example:

    sqltags.tags.dotted.name.here == 'foo'

## Class `SQLTagProxy`

An object based on a `Tag` name
which produces an `SQLParameters` when compared with some value.

Example:

    >>> sqltags = SQLTags('sqlite://')
    >>> sqltags.init()
    >>> # make a SQLParameters for testing the tag 'name.thing'==5
    >>> sqlp = sqltags.tags.name.thing == 5
    >>> str(sqlp.constraint)
    'tags_1.name = :name_1 AND tags_1.float_value = :float_value_1'
    >>> sqlp = sqltags.tags.name.thing == 'foo'
    >>> str(sqlp.constraint)
    'tags_1.name = :name_1 AND tags_1.string_value = :string_value_1'

### Method `SQLTagProxy.__eq__(self, other, alias=None) -> cs.sqltags.SQLParameters`

Return an SQL `=` test `SQLParameters`.

Example:

    >>> sqlp = SQLTags('sqlite://').tags.name.thing == 'foo'
    >>> str(sqlp.constraint)
    'tags_1.name = :name_1 AND tags_1.string_value = :string_value_1'

### Method `SQLTagProxy.__ge__(self, other)`

Return an SQL `>=` test `SQLParameters`.

Example:

    >>> sqlp = SQLTags('sqlite://').tags.name.thing >= 'foo'
    >>> str(sqlp.constraint)
    'tags_1.name = :name_1 AND tags_1.string_value >= :string_value_1'

### Method `SQLTagProxy.__getattr__(self, sub_tag_name)`

Magic access to dotted tag names: produce a new `SQLTagProxy` from ourself.

### Method `SQLTagProxy.__gt__(self, other)`

Return an SQL `>` test `SQLParameters`.

Example:

    >>> sqlp = SQLTags('sqlite://').tags.name.thing > 'foo'
    >>> str(sqlp.constraint)
    'tags_1.name = :name_1 AND tags_1.string_value > :string_value_1'

### Method `SQLTagProxy.__le__(self, other)`

Return an SQL `<=` test `SQLParameters`.

Example:

    >>> sqlp = SQLTags('sqlite://').tags.name.thing <= 'foo'
    >>> str(sqlp.constraint)
    'tags_1.name = :name_1 AND tags_1.string_value <= :string_value_1'

### Method `SQLTagProxy.__lt__(self, other)`

Return an SQL `<` test `SQLParameters`.

Example:

    >>> sqlp = SQLTags('sqlite://').tags.name.thing < 'foo'
    >>> str(sqlp.constraint)
    'tags_1.name = :name_1 AND tags_1.string_value < :string_value_1'

### Method `SQLTagProxy.__ne__(self, other, alias=None) -> cs.sqltags.SQLParameters`

Return an SQL `<>` test `SQLParameters`.

Example:

    >>> sqlp = SQLTags('sqlite://').tags.name.thing != 'foo'
    >>> str(sqlp.constraint)
    'tags_1.name = :name_1 AND tags_1.string_value != :string_value_1'

### Method `SQLTagProxy.by_op_text(self, op_text, other, alias=None)`

Return an `SQLParameters` based on the comparison's text representation.

Parameters:
* `op_text`: the comparsion operation text, one of:
  `'='`, `'<='`, `'<'`, `'>='`, `'>'`, `'~'`.
* `other`: the other value for the comparison,
  used to infer the SQL column name
  and kept to provide the SQL value parameter
* `alias`: optional SQLAlchemy table alias

### Method `SQLTagProxy.likeglob(self, globptn: str) -> cs.sqltags.SQLParameters`

Return an SQL LIKE test approximating a glob as an `SQLParameters`.

Example:

    >>> sqlp = SQLTags('sqlite://').tags.name.thing.likeglob('foo*')
    >>> str(sqlp.constraint)
    "tags_1.name = :name_1 AND tags_1.string_value LIKE :string_value_1 ESCAPE '\\'"

### Method `SQLTagProxy.startswith(self, prefix: str) -> cs.sqltags.SQLParameters`

Return an SQL LIKE prefix test `SQLParameters`.

Example:

    >>> sqlp = SQLTags('sqlite://').tags.name.thing.startswith('foo')
    >>> str(sqlp.constraint)
    "tags_1.name = :name_1 AND tags_1.string_value LIKE :string_value_1 ESCAPE '\\'"

## Class `SQLTags(cs.tagset.TagSets,cs.resources.MultiOpenMixin)`

A class using an SQL database to store its `TagSet`s.

### `SQLTags.TagSetClass`

### Method `SQLTags.__getitem__(self, *a, **kw)`

Return an `SQLTagSet` for `index` (an `int` or `str`).

### Method `SQLTags.__setitem__(self, *a, **kw)`

Dummy `__setitem__` which checks `te` against the db by type
because the factory inserts it into the database.

### Method `SQLTags.db_entity(self, index)`

Return the `Entities` instance for `index` or `None`.

### Method `SQLTags.db_session(self, *, new=False, session=None)`

Context manager to obtain a db session if required,
just a shim for `self.orm.session()`.

### Property `SQLTags.default_db_session`

The current per-`Thread` SQLAlchemy Session.

### Method `SQLTags.default_factory(self, name: [<class 'str'>, None], *, unixtime=None, tags=None)`

Fetch or create an `SQLTagSet` for `name`.

Note that `name` may be `None` to create a new "log" entry.

### Method `SQLTags.find(self, criteria)`

Generate and run a query derived from `criteria`
yielding `SQLTagSet` instances.

Parameters:
* `criteria`: an iterable of search criteria
  which should be `SQTCriterion`s
  or a `str` suitable for `SQTCriterion.from_str`.
  A string may also be supplied, suitable for `SQTCriterion.from_str`.

### Method `SQLTags.flush(self)`

Flush the current session state to the database.

### Method `SQLTags.get(self, index, default=None)`

Return an `SQLTagSet` matching `index`, or `None` if there is no such entity.

### Method `SQLTags.import_csv_file(self, f, *, update_mode=False)`

Import CSV data from the file `f`.

If `update_mode` is true
named records which already exist will update from the data,
otherwise the conflict will raise a `ValueError`.

### Method `SQLTags.import_tagged_entity(self, te, *, update_mode=False) -> None`

Import the `TagSet` `te`.

This updates the database with the contents of the supplied `TagSet`,
which has no inherent relationship to the database.

If `update_mode` is true
named records which already exist will update from `te`,
otherwise the conflict will raise a `ValueError`.

### Method `SQLTags.infer_db_url(envvar=None, default_path=None)`

Infer the database URL.

Parameters:
* `envvar`: environment variable to specify a default,
  default from `DBURL_ENVVAR` (`SQLTAGS_DBURL`).

### Method `SQLTags.init(self)`

Initialise the database.

### Method `SQLTags.items(self, *, prefix=None)`

Return an iterable of `(tagset_name,TagSet)`.
Excludes unnamed `TagSet`s.

Constrain the names to those starting with `prefix`
if not `None`.

### Method `SQLTags.keys(self, *, prefix=None)`

Yield all the nonNULL names.

Constrain the names to those starting with `prefix`
if not `None`.

### Property `SQLTags.metanode`

The metadata node.

### Method `SQLTags.values(self, *, prefix=None)`

Return an iterable of the named `TagSet`s.
Excludes unnamed `TagSet`s.

Constrain the names to those starting with `prefix`
if not `None`.

## Class `SQLTagsCommand(BaseSQLTagsCommand,cs.cmdutils.BaseCommand,cs.tagset.TagsCommandMixin)`

`sqltags` main command line utility.


Command line usage:

    Usage: SQLTagsCommand [-f db_url] subcommand [...]
      -f db_url SQLAlchemy database URL or filename.
                Default from $SQLTAGS_DBURL (default '~/var/sqltags.sqlite').
      Subcommands:
        edit criteria...
          Edit the entities specified by criteria.
        export {tag[=value]|-tag}...
          Export entities matching all the constraints.
          The output format is CSV data with the following columns:
          * `unixtime`: the entity unixtime, a float
          * `id`: the entity database row id, an integer
          * `name`: the entity name
          * `tags`: a column per `Tag`
        find [-o output_format] {tag[=value]|-tag}...
          List entities matching all the constraints.
          -o output_format
                      Use output_format as a Python format string to lay out
                      the listing.
                      Default: {entity.isodatetime} {headline}
        help [subcommand-names...]
          Print the help for the named subcommands,
          or for all subcommands if no names are specified.
        import [{-u|--update}] {-|srcpath}...
          Import CSV data in the format emitted by "export".
          Each argument is a file path or "-", indicating standard input.
          -u, --update  If a named entity already exists then update its tags.
                        Otherwise this will be seen as a conflict
                        and the import aborted.
        init
          Initialise the database.
          This includes defining the schema and making the root metanode.
        log [-c category,...] [-d when] [-D strptime] {-|headline} [tags...]
          Record entries into the database.
          If headline is '-', read headlines from standard input.
          -c categories
            Specify the categories for this log entry.
            The default is to recognise a leading CAT,CAT,...: prefix.
          -d when
            Use when, an ISO8601 date, as the log entry timestamp.
          -D strptime
            Read the time from the start of the headline
            according to the provided strptime specification.
        ns entity-names...
          List entities and their tags.
        tag {-|entity-name} {tag[=value]|-tag}...
          Tag an entity with multiple tags.
          With the form "-tag", remove that tag from the direct tags.
          A entity-name named "-" indicates that entity-names should
          be read from the standard input.

### Method `SQLTagsCommand.cmd_ns(self, argv)`

Usage: {cmd} entity-names...
List entities and their tags.

## Class `SQLTagSet(cs.obj.SingletonMixin,cs.tagset.TagSet,builtins.dict,cs.lex.FormatableMixin,cs.mappings.AttrableMappingMixin)`

A singleton `TagSet` attached to an `SQLTags` instance.

### Method `SQLTagSet.add_db_tag(self, *a, **kw)`

Add a tag to the database.

### Method `SQLTagSet.child_tagsets(self, tag_name='parent')`

Return the child `TagSet`s as defined by their parent `Tag`,
by default the `Tag` named `'parent'`.

### Method `SQLTagSet.db_session(self, *, session=None)`

Context manager to obtain a new session if required,
just a shim for `self.sqltags.db_session`.

### Method `SQLTagSet.discard(self, name, value=None, *a, **kw)`

pylint: disable=keyword-arg-before-vararg

### Method `SQLTagSet.discard_db_tag(self, tag_name, value=None)`

Discard a tag from the database.

### Property `SQLTagSet.name`

Return the `.name`.

### Method `SQLTagSet.parent_tagset(self, tag_name='parent')`

Return the parent `TagSet` as defined by a `Tag`,
by default the `Tag` named `'parent'`.

### Method `SQLTagSet.set(self, name, value=None, *a, **kw)`

pylint: disable=keyword-arg-before-vararg

## Class `SQLTagsORM(cs.sqlalchemy_utils.ORM,cs.resources.MultiOpenMixin,cs.dateutils.UNIXTimeMixin)`

The ORM for an `SQLTags`.

### Method `SQLTagsORM.declare_schema(self)`

Define the database schema / ORM mapping.

### Method `SQLTagsORM.define_schema(self)`

Instantiate the schema and define the root metanode.

### Method `SQLTagsORM.prepare_metanode(self, *, session)`

Ensure row id 0, the metanode, exists.

### Method `SQLTagsORM.search(self, *a, **kw)`

Construct a query to match `Entity` rows
matching the supplied `criteria` iterable.
Return an SQLAlchemy `Query`.

The `mode` parameter has the following values:
* `'id'`: the query only yields entity ids
* `'entity'`: (default) the query yields entities without tags
* `'tagged'`: (default) the query yields entities left
outer joined with their matching tags

Note that the `'tagged'` result produces multiple rows for any
entity with multiple tags, and that this requires the caller to
fold entities with multiple tags together.

*Note*:
due to implementation limitations
the SQL query itself may not apply all the criteria,
so every criterion must still be applied
to the results
using its `.match_entity` method.

If `name` is omitted or `None` the query will match log entities
otherwise the entity with the specified `name`.

The `criteria` should be an iterable of `SQTCriterion` instances
used to construct the query.

## Class `SQTCriterion(cs.tagset.TagSetCriterion)`

Subclass of `TagSetCriterion` requiring an `.sql_parameters` method
which returns an `SQLParameters` providing the information required
to construct an sqlalchemy query.
It also resets `.CRITERION_PARSE_CLASSES`, which will pick up
the SQL capable criterion classes below.

### `SQTCriterion.TAG_BASED_TEST_CLASS`

### Method `SQTCriterion.match_tagged_entity(self, te: cs.tagset.TagSet) -> bool`

Perform the criterion test on the Python object directly.
This is used at the end of a query to implement tests which
cannot be sufficiently implemented in SQL.
If `self.SQL_COMPLETE` it is not necessary to call this method.

### Method `SQTCriterion.sql_parameters(self, orm) -> cs.sqltags.SQLParameters`

Subclasses must return am `SQLParameters` instance
parameterising the SQL queries that follow.

## Class `SQTEntityIdTest(SQTCriterion,cs.tagset.TagSetCriterion)`

A test on `entity.id`.

### Method `SQTEntityIdTest.match_tagged_entity(self, te: cs.tagset.TagSet) -> bool`

Test the `TagSet` `te` against `self.entity_ids`.

### Method `SQTEntityIdTest.parse(s, offset=0, delim=None)`

Parse a decimal entity id from `s`.

## Function `verbose(msg, *a)`

Emit message if in verbose mode.

# Release Log



*Release 20210321*:
Drop logic now merged with cs.sqlalchemy_utils, use the new default session stuff.

*Release 20210306.1*:
Docstring updates.

*Release 20210306*:
Initial release.
