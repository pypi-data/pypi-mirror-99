"""
An opinionated Pythonic SQLite interface.

SQLite is a relational database management system contained in a C
programming library. In contrast to many other database management
systems, SQLite is not a client–server database engine. Rather, it
is embedded into the end program.

"""

# TODO when a new table is created, ask to import from table no longer in use
#      -- deprecate no longer used tables if no longer needed

import contextlib
import datetime
import functools
import json
import os
import pathlib

import pendulum
try:
    from pysqlite3 import dbapi2 as sqlite3
except ImportError:
    print("falling back to sqlite3 in the standard library")  # TODO warning
    import sqlite3

from understory import solarized

__all__ = ["db"]


# TODO register and handle JSON type

def from_datetime(val):
    if isinstance(val, datetime.datetime):
        return pendulum.instance(val)
    val = val.decode("utf-8")
    # remove timezone column
    if val[-6] in "-+":
        val = "".join(val.rpartition(":")[::2])
    date = "YYYY-MM-DD"
    time = "HH:mm:ss"
    try:
        dt = pendulum.from_format(val, f"{date} {time}.SSSSSSZ")
    except ValueError:
        try:
            dt = pendulum.from_format(val, f"{date} {time}.SSSSSS")
        except ValueError:
            try:
                dt = pendulum.from_format(val, f"{date} {time}Z")
            except ValueError:
                try:
                    dt = pendulum.from_format(val, f"{date} {time}")
                except ValueError:
                    dt = pendulum.from_format(val, date)
    return dt


sqlite3.register_converter("DATETIME", from_datetime)
sqlite3.register_adapter(pendulum.DateTime, lambda val: val.isoformat(" "))


def from_json(val):
    def f(dct):
        def upgrade_date(key):
            try:
                val = dct[key]
            except KeyError:
                return
            if isinstance(val, list):
                val = val[0]
            if val[-6] in "-+":
                val = "".join(val.rpartition(":")[::2])
            datetime = "YYYY-MM-DDTHH:mm:ss"
            try:
                dct[key] = pendulum.from_format(val, f"{datetime}.SSSSSSZ")
            except ValueError:
                try:
                    dct[key] = pendulum.from_format(val, f"{datetime}Z")
                except ValueError:
                    pass
        # TODO FIND WHEN NESTED
        upgrade_date("published")
        upgrade_date("updated")
        return dct
    return json.loads(val, object_hook=f)


class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


sqlite3.register_converter("JSON", from_json)
sqlite3.register_adapter(dict, lambda val: JSONEncoder(indent=2).encode(val))


def ors(item, values, fuzzy=False):
    template = "{} LIKE '{}%'" if fuzzy else "{} = '{}'"
    return " OR ".join(template.format(item, v) for v in values)


def adapt(x):
    return x


def get_icu():
    current_dir = pathlib.Path(__file__).parent
    icuext_path = current_dir / "libsqliteicu.so"
    if not icuext_path.exists():
        icuext_source_path = current_dir / "icu.c"
        os.system(f"gcc -fPIC -shared {icuext_source_path} "
                  f"`pkg-config --libs icu-i18n` -o {icuext_path}")
    return icuext_path


class Database:
    """"""

    IntegrityError = sqlite3.IntegrityError
    OperationalError = sqlite3.OperationalError
    ProgrammingError = sqlite3.ProgrammingError

    def __init__(self, path):
        self.path = path
        for command in ("create", "alter", "drop", "insert", "replace",
                        "select", "update", "delete", "columns"):
            def single_statement_cursor(command):
                @functools.wraps(getattr(Cursor, command))
                def proxy(_self, *args, **kwargs):
                    with self.transaction as cur:
                        return getattr(cur, command)(_self, *args, **kwargs)
                return proxy
            setattr(self, command, single_statement_cursor(command))

        conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
        # TODO conn.cursor().execute("PRAGMA foreign_keys = ON;")
        try:
            conn.enable_load_extension(True)
        except AttributeError:
            pass
        else:
            icuext_path = get_icu()
            conn.load_extension(str(icuext_path))
            conn.enable_load_extension(False)
            conn.execute("SELECT icu_load_collation('en_US', 'UNICODE');")
        conn.row_factory = sqlite3.Row
        self.conn = conn

        self.debug = False

    def define(self, **table_schemas):
        """
        define multiple tables at once migrating them if necessary

        """
        # TODO bump version a la "PRAGMA user_version = 1;" and store change
        # TODO store backups
        while table_schemas:
            for table, schema in list(table_schemas.items()):
                table_schemas.pop(table)
                new_table = "new_{}".format(table)
                self.create(table, schema)
                self.create(new_table, schema)
                with self.transaction as cur:
                    old_columns = cur.columns(table)
                    new_columns = cur.columns(new_table)
                    if old_columns == new_columns:
                        cur.drop(new_table)
                        continue
                    old_names = {col[0] for col in old_columns}
                    new_names = {col[0] for col in new_columns}
                    cols = list(old_names.intersection(new_names))
                    print("Migrating table `{}`..".format(table), end=" ")
                    for row in cur.select(table, what=", ".join(cols)):
                        cur.insert(new_table, dict(zip(cols, list(row))))
                    cur.drop(table)
                    cur.cur.execute(f"""ALTER TABLE {new_table}
                                        RENAME TO {table}""")
                print("success")

    @property
    def tables(self):
        return [r[0] for r in self.select("sqlite_master", what="name",
                                          where="type='table'")]

    @property
    @contextlib.contextmanager
    def transaction(self):
        """
        enter a transaction context and return its `Cursor`

            >>> with Database().transaction as cur:  # doctest: +SKIP
            ...    cur.insert(...)
            ...    cur.insert(...)
            ...    cur.select(...)
            ...    cur.insert(...)

        """
        # TODO log transaction begin, complete, etc..
        with self.conn:
            cursor = Cursor(self.conn.cursor())
            cursor.debug = self.debug
            yield cursor
        # with sqlite3.connect(self.path,
        #                      detect_types=sqlite3.PARSE_DECLTYPES) as conn:
        #     # conn.cursor().execute("PRAGMA foreign_keys = ON;")
        #     conn.enable_load_extension(True)
        #     icuext_path = pathlib.Path(__file__).parent / "libsqliteicu"
        #     conn.load_extension(str(icuext_path))
        #     conn.enable_load_extension(False)
        #     conn.execute("SELECT icu_load_collation('en_US', 'UNICODE');")
        #     conn.row_factory = sqlite3.Row
        #     cursor = Cursor(conn.cursor())
        #     cursor.debug = self.debug
        #     yield cursor

    def destroy(self):
        pathlib.Path(self.path).unlink()


def db(path=None, **table_schemas) -> Database:
    """
    return a connection to a `SQLite` database

    Database supplied by given `path` or in environment variable `$SQLDB`.

    Note: `table_schemas` should not include a table (dict key) named "path".

    """
    if not path:
        path = os.environ.get("SQLDB", None)
    if path:
        dbi = Database(path)
        dbi.define(**table_schemas)
        return dbi


class Cursor:

    """

    """

    IntegrityError = sqlite3.IntegrityError
    OperationalError = sqlite3.OperationalError

    def __init__(self, cur):
        self.cur = cur
        self.debug = False

    def create(self, table, schema):
        """
        create a table with given column schema

        """
        schema, _, fts = schema.partition(";")
        if fts.strip().lower() == "fts":
            sql = ("CREATE VIRTUAL TABLE IF NOT EXISTS {} "
                   "USING fts5 ({})".format(table, schema))
        else:
            sql = "CREATE TABLE IF NOT EXISTS {} ({})".format(table, schema)
        self.cur.execute(sql)

    def alter(self, table):
        """
        alert a table

        """

    def drop(self, *tables):
        """
        drop one or more tables

        """
        for table in tables:
            sql = "DROP TABLE {}".format(table)
            self.cur.execute(sql)

    def insert(self, table, *records, _force=False, **record):
        return self._insert("insert", table, *records, _force=False, **record)

    def replace(self, table, *records, _force=False, **record):
        return self._insert("replace", table, *records, _force=False, **record)

    def _insert(self, operation, table, *records, _force=False, **record):
        """Insert one or more records into given table."""
        if record:
            if records:
                raise TypeError("use `record` *or* `records` not both")
            records = (record,)  # XXX += (record,)
        values = []
        for record in records:
            for column, val in record.items():
                if isinstance(val, dict):
                    record[column] = JSONEncoder().encode(val)
            columns, vals = zip(*record.items())
            values.append(vals)
        sql = ("{} INTO {}({})".format(operation.upper(), table,
                                       ", ".join(columns)) +
               " VALUES ({})".format(", ".join("?" * len(vals))))
        if self.debug:
            print(sql)
        try:
            if len(values) == 1:
                self.cur.execute(sql, vals)
                self.cur.execute("SELECT last_insert_rowid()")
                return self.cur.fetchone()[0]
            else:
                self.cur.executemany(sql, values)
        except sqlite3.IntegrityError as err:
            if not _force:
                raise err

    def select(self, table, what="*", where=None, order=None, group=None,
               join=None, limit=None, offset=None, vals=None):
        """
        select records from one or more tables

        """
        sql = self._select_sql(table, what=what, where=where, order=order,
                               group=group, join=join, limit=limit,
                               offset=offset, vals=vals)[1:-1]
        if self.debug:
            print(sql)
            if vals:
                print(" ", vals)
        if vals:
            self.cur.execute(sql, vals)
        else:
            self.cur.execute(sql)

        class Results:

            def __init__(innerself, results):
                innerself.results = list(results)

            def __getitem__(innerself, index):
                return innerself.results[index]

            def __len__(innerself):
                return len(innerself.results)

            def _repr_html_(innerself):
                results = "<tr>"
                types = {}
                for column in self.columns(table):
                    types[column[0]] = column[1]
                    results += (f"<td>{column[0]} "
                                f"<small>{column[1]}</small></td>")
                results += "</tr>"
                for result in innerself.results:
                    results += "<tr>"
                    for key, value in dict(result).items():
                        if types[key] == "JSON":
                            encoded_json = JSONEncoder(indent=2).encode(value)
                            value = solarized.highlight(encoded_json, ".json")
                        results += f"<td>{value}</td>"
                    results += "</tr>"
                return f"<table>{results}</table>"
        return Results(self.cur.fetchall())

    def _select_sql(self, table, what="*", where=None, order=None, group=None,
                    join=None, limit=None, offset=None, vals=None, suffix=""):
        sql_parts = ["SELECT {}".format(what), "FROM {}".format(table)]
        if join:
            if not isinstance(join, (list, tuple)):
                join = [join]
            for join_statement in join:
                sql_parts.append("LEFT JOIN {}".format(join_statement))
        if where:
            # if vals:
            #     where = where.format(*[str(adapt(v)) for v in vals])
            sql_parts.append("WHERE {}".format(where))
        if order:
            sql_parts.append("ORDER BY {}".format(order))
        if group:
            sql_parts.append("GROUP BY {}".format(group))
        if limit:
            limitsql = "LIMIT {}".format(limit)
            if offset:
                limitsql += " {}".format(offset)
            sql_parts.append(limitsql)
        return "({}) {}".format("\n".join(sql_parts), suffix).rstrip()

    def update(self, table, what=None, where=None, vals=None, **record):
        """
        update one or more records

        Use `what` *or* `record`.

        """
        sql_parts = ["UPDATE {}".format(table)]
        if what:
            what_sql = what
        else:
            keys, values = zip(*record.items())
            what_sql = ", ".join("{}=?".format(key) for key in keys)
            if vals is None:
                vals = []
            vals = list(values) + vals
        sql_parts.append("SET {}".format(what_sql))
        if where:
            sql_parts.append("WHERE {}".format(where))
        sql = "\n".join(sql_parts)
        if self.debug:
            print(sql)
        if vals:
            self.cur.execute(sql, vals)
            print(vals)
        else:
            self.cur.execute(sql)

    def delete(self, table, where=None, vals=None):
        """
        delete one or more records

        """
        sql_parts = ["DELETE FROM {}".format(table)]
        if where:
            sql_parts.append("WHERE {}".format(where))
        sql = "\n".join(sql_parts)
        if vals:
            self.cur.execute(sql, vals)
        else:
            self.cur.execute(sql)

    def columns(self, table):
        """
        return columns for given table

        """
        return [list(column)[1:] for column in
                self.cur.execute("PRAGMA table_info({})".format(table))]
