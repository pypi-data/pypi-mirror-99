import sqlite3 as lite
import re
from enum import Enum
import logging
log = logging.getLogger(__name__)

sqlite_keyword_list = ["ABORT",
                       "ACTION",
                       "ADD",
                       "AFTER",
                       "ALL",
                       "ALTER",
                       "ALWAYS",
                       "ANALYZE",
                       "AND",
                       "AS",
                       "ASC",
                       "ATTACH",
                       "AUTOINCREMENT",
                       "BEFORE",
                       "BEGIN",
                       "BETWEEN",
                       "BY",
                       "CASCADE",
                       "CASE",
                       "CAST",
                       "CHECK",
                       "COLLATE",
                       "COLUMN",
                       "COMMIT",
                       "CONFLICT",
                       "CONSTRAINT",
                       "CREATE",
                       "CROSS",
                       "CURRENT",
                       "CURRENT_DATE",
                       "CURRENT_TIME",
                       "CURRENT_TIMESTAMP",
                       "DATABASE",
                       "DEFAULT",
                       "DEFERRABLE",
                       "DEFERRED",
                       "DELETE",
                       "DESC",
                       "DETACH",
                       "DISTINCT",
                       "DO",
                       "DROP",
                       "EACH",
                       "ELSE",
                       "END",
                       "ESCAPE",
                       "EXCEPT",
                       "EXCLUDE",
                       "EXCLUSIVE",
                       "EXISTS",
                       "EXPLAIN",
                       "FAIL",
                       "FILTER",
                       "FIRST",
                       "FOLLOWING",
                       "FOR",
                       "FOREIGN",
                       "FROM",
                       "FULL",
                       "GENERATED",
                       "GLOB",
                       "GROUP",
                       "GROUPS",
                       "HAVING",
                       "IF",
                       "IGNORE",
                       "IMMEDIATE",
                       "IN",
                       "INDEX",
                       "INDEXED",
                       "INITIALLY",
                       "INNER",
                       "INSERT",
                       "INSTEAD",
                       "INTERSECT",
                       "INTO",
                       "IS",
                       "ISNULL",
                       "JOIN",
                       "KEY",
                       "LAST",
                       "LEFT",
                       "LIKE",
                       "LIMIT",
                       "MATCH",
                       "NATURAL",
                       "NO",
                       "NOT",
                       "NOTHING",
                       "NOTNULL",
                       "NULL",
                       "NULLS",
                       "OF",
                       "OFFSET",
                       "ON",
                       "OR",
                       "ORDER",
                       "OTHERS",
                       "OUTER",
                       "OVER",
                       "PARTITION",
                       "PLAN",
                       "PRAGMA",
                       "PRECEDING",
                       "PRIMARY",
                       "QUERY",
                       "RAISE",
                       "RANGE",
                       "RECURSIVE",
                       "REFERENCES",
                       "REGEXP",
                       "REINDEX",
                       "RELEASE",
                       "RENAME",
                       "REPLACE",
                       "RESTRICT",
                       "RIGHT",
                       "ROLLBACK",
                       "ROW",
                       "ROWS",
                       "SAVEPOINT",
                       "SELECT",
                       "SET",
                       "TABLE",
                       "TEMP",
                       "TEMPORARY",
                       "THEN",
                       "TIES",
                       "TO",
                       "TRANSACTION",
                       "TRIGGER",
                       "UNBOUNDED",
                       "UNION",
                       "UNIQUE",
                       "UPDATE",
                       "USING",
                       "VACUUM",
                       "VALUES",
                       "VIEW",
                       "VIRTUAL",
                       "WHEN",
                       "WHERE",
                       "WINDOW",
                       "WITH",
                       "WITHOUT"]


class StoreTSResult(Enum):
    SUCCESS=0
    DUPLICATE_EXISTS=1
    FAILED_TO_REPLACE=2
    FAILED_TO_INSERT=3


class SqliteDeviceDataStore:
    """ Class for managing saving and loading time-series and key-value store data in a sqlite database.

    For time series, required field "ts" (timestamp) is the primary key and is an INTEGER to minimize storage
    For key value tables, the default value type is INTEGER
    """

    def __init__(self, dbname):
        self.dbname = dbname
        self.con = lite.connect(dbname)
        self.cursor = self.con.cursor()

    def store_new_tsdata(self, table_name, ts, data_dict):
        """ Stores a new time-series record in a sqlite3 database.
        If a record already exists with the same timestamp, replace it.
        Args:
            table_name (str): name of the table to save to
            ts (float, int): timestamp - to ensure it is provided
            data_dict (dict): dictionary of data to write
        """
        result = StoreTSResult.SUCCESS

        log.debug(f"Logging time series record to {self.dbname}, table {table_name}")
        log.debug(f"Data: {data_dict}")
        data_dict = data_dict.copy()
        data_dict['ts'] = ts
        data_dict = sqlite_friendly(data_dict)

        try:
            self.cursor.execute('SELECT * FROM [{}];'.format(table_name))
        except lite.OperationalError:
            # table did not exist - create it
            self.cursor.execute('CREATE TABLE [{}] (ts INT PRIMARY KEY);'.format(table_name))
            self.con.commit()
        self.add_columns(table_name, data_dict)

        # check if timestamp already exists
        existingdatarecord_dict = self.get_ts(table_name, data_dict['ts'])
        if existingdatarecord_dict is not None:
            result = StoreTSResult.DUPLICATE_EXISTS
            log.error('Timestamp {} already stored. Replacing.'.format(data_dict['ts']))
            columns = ', '.join(data_dict.keys())
            placeholders = ', '.join('?' * len(data_dict))
            sql = 'REPLACE INTO [{}] ({}) VALUES ({})'.format(table_name, columns, placeholders)
            try:
                self.cursor.execute(sql, list(data_dict.values()))
            except lite.IntegrityError:
                log.error('Failed to add record at timestamp {}'.format(data_dict['ts']))
                result=StoreTSResult.FAILED_TO_REPLACE
            else:
                self.con.commit()
        else:
            # add a data row
            columns = ', '.join(data_dict.keys())
            placeholders = ', '.join('?' * len(data_dict))
            sql = "INSERT INTO [{}] ({}) VALUES ({})".format(table_name, columns, placeholders)
            try:
                self.cursor.execute(sql, list(data_dict.values()))
            except lite.IntegrityError:
                result = StoreTSResult.FAILED_TO_INSERT
                log.error('Failed to add record at timestamp {}'.format(data_dict['ts']))
            else:
                self.con.commit()
        return result

    def store_new_kvdata(self, table_name, data_dict):
        """ Stores a new key-value data in a sqlite3 database in a multi-platform friendly way
        (e.g. accessible with C++)
        Args:
            table_name (str): name of the table to save to
            data_dict (dict): dictionary of data to write
        """
        log.debug("Logging key-value data to {}, table {}".format(self.dbname, table_name))
        data_dict = data_dict.copy()
        data_dict = sqlite_friendly(data_dict)

        try:
            self.cursor.execute("SELECT * FROM [{}];".format(table_name))
        except lite.OperationalError:
            # table did not exist - create it
            self.cursor.execute("CREATE TABLE [{}] ('key' TEXT PRIMARY KEY, 'value' INTEGER);".format(table_name))
            self.con.commit()

        # Loop through each new value and replace it
        for key, val in data_dict.items():
            if isinstance(val, str):
                sql = "REPLACE INTO [{}] (key, value) VALUES ('{}', '{}');".format(table_name, key, val)
            else:
                sql = "REPLACE INTO [{}] (key, value) VALUES ('{}', {});".format(table_name, key, val)
            try:
                self.cursor.execute(sql)
            except lite.IntegrityError:
                print('Error replacing record with key {} and value {}'.format(key, val))
            else:
                self.con.commit()

    def get_ts_oldest(self, table_name):
        """
        Get the oldest record from a time series table
        Args:
            table_name: name of the table

        Returns:
            The oldest record as a dictionary
        """
        try:
            self.cursor.execute('SELECT * FROM [{tn}] WHERE ts = (SELECT MIN(ts) FROM {tn});'.format(tn=table_name))
        except lite.OperationalError:
            pass
        else:
            row = self.cursor.fetchone()
            if row:
                row_dict = dict_factory(self.cursor, row)
                ts = row_dict.pop('ts')
                return ts, row_dict
            else:
                return None, None

    def get_ts_newest(self, table_name):
        """
        Get the newest record from a time series table
        Args:
            table_name: name of the table

        Returns:
            The newest record as a dictionary
        """
        try:
            self.cursor.execute('SELECT * FROM [{tn}] WHERE ts = (SELECT MAX(ts) FROM {tn});'.format(tn=table_name))
        except lite.OperationalError:
            pass
        else:
            row = self.cursor.fetchone()
            if row:
                row_dict = dict_factory(self.cursor, row)
                ts = row_dict.pop('ts')
                return ts, row_dict
            else:
                return None, None

    def get_ts(self, table_name, ts):
        """
        Get a record from a time-series table
        Args:
            table_name (str): name of the table
            ts: timestamp

        Returns:
            The value or None if the key does not exist
        """
        self.cursor.execute("SELECT * FROM [{}] WHERE ts='{}';".format(table_name, ts))
        row = self.cursor.fetchone()
        if row:
            return dict_factory(self.cursor, row)
        else:
            return None

    def get_kv(self, table_name, key):
        """
        Get a value from a key-value pair table
        Args:
            table_name (str): name of the table
            key (str): name of the key

        Returns:
            The value or None if the key does not exist
        """
        try:
            self.cursor.execute("SELECT value FROM [{}] WHERE key='{}';".format(table_name, key))
        except lite.OperationalError:
            pass
        else:
            row = self.cursor.fetchone()
            if row:
                row_dict = dict_factory(self.cursor, row)
                value = row_dict.pop('value')
                return value
            else:
                return None

    def close(self):
        self.con.close()

    def ts_exists(self, table_name, ts):
        self.cursor.execute("SELECT * FROM [{}] WHERE ts='{}';".format(table_name, ts))
        id_exists = self.cursor.fetchone()
        if id_exists:
            return True
        else:
            return False

    def add_columns(self, table_name, data_dict):
        # make sure we have sqlite-friendly column names
        data_dict = sqlite_friendly(data_dict)

        column_type = 'NUMERIC'
        self.cursor.execute('PRAGMA TABLE_INFO([{}])'.format(table_name))
        column_names = [tup[1] for tup in self.cursor.fetchall()]
        for key in data_dict.keys():
            if key not in column_names:
                # add new data column
                self.cursor.execute("ALTER TABLE [{tn}] ADD COLUMN '{cn}' {ct}" \
                                    .format(tn=table_name, cn=key, ct=column_type))
        self.con.commit()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def sqlite_friendly_converter(non_sqlite_friendly_name):
    cured = non_sqlite_friendly_name.strip()
    cured = re.sub('[^0-9a-zA-Z]+', '_', cured)
    if cured.upper() in sqlite_keyword_list:
        cured = '_' + cured
    return cured


def sqlite_friendly(non_sqlite_friendly_name):
    if isinstance(non_sqlite_friendly_name, list):
        result = []
        for s in non_sqlite_friendly_name:
            result.append(sqlite_friendly_converter(s))
    else:
        if isinstance(non_sqlite_friendly_name, dict):
            result = {}
            for key in non_sqlite_friendly_name:
                new_key = sqlite_friendly_converter(key)
                result[new_key] = non_sqlite_friendly_name[key]
        else:
            result = sqlite_friendly_converter(non_sqlite_friendly_name)
    return result
