import os

from contextlib import contextmanager

try:
    import psycopg2cffi as psycopg2
except ImportError:
    import psycopg2

import queries

DB_CONNECT = os.getenv('NHLDB_CONNECT')


@contextmanager
def session(connect=None, pool_size=10, is_tornado=False):
    if connect is None:
        connect = DB_CONNECT
    if connect is None:
        raise Exception('Please provide a connection string or set the NHLDB_CONNECT env. variable')
    if is_tornado:
        s = queries.TornadoSession(connect, pool_max_size=pool_size)
    else:
        s = queries.Session(connect, pool_max_size=pool_size)
    try:
        yield s
    finally:
        s.close()


def _insert_dict(s, table_name, values):
    vals = [values[col] for col in values]
    s.execute('INSERT INTO {table_name} ({cols}) VALUES ({vals})'.format(table_name=table_name,
                                                                         cols=','.join(["%s"] * len(vals)),
                                                                         vals=','.join(vals)))


class Query(object):
    def __init__(self, table, select=None):
        if hasattr(table, '__table_name'):
            self.table = table.__table_name
        else:
            self.table = table
        self.select = select
        self._where = []

    def where(self, clause):
        self._where.append(clause)
        return self

    def __str__(self):
        sel = '*'
        if self.select is not None:
            sel = ', '.join(self.select)
        sql = ['''
        SELECT {selects}
        FROM {table}
        '''.format(selects=sel, table=self.table)]
        for i, where in enumerate(self._where):
            if i == 0:
                sql.append('WHERE')
            else :
                sql.append('AND')
            sql.append(where)
        return ' '.join(sql)
