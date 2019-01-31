import psycopg2
import psycopg2.extras
import psycopg2.pool
from contextlib import contextmanager
from flask import current_app
from flask import g

def create_pool():
    if 'pool' not in g:
        g.pool = psycopg2.pool.SimpleConnectionPool(
            1,
            20,
            dsn=current_app.config['DATABASE_URI'],
            connection_factory=psycopg2.extras.RealDictConnection
        )

    return g.pool

@contextmanager
def get_db_connection():
    try:
        connection = g.pool.getconn()
        yield connection
    finally:
        g.pool.putconn(connection)

@contextmanager
def get_db_cursor(commit=True):
    create_pool() # ugly hack to make sure pool is really created
    with get_db_connection() as conn:
        cur = conn.cursor()
        try:
            yield cur
            if commit:
                conn.commit()
        finally:
            cur.close()

def db_query(query:str, params:dict=None, fetch_all:bool=False):
    """Get rows from database.

    :param query
    :param params
    :param fetch_all
    """
    with get_db_cursor() as cur:
        if (current_app.config['DEBUG'] and not current_app.config['TESTING']):
            current_app.logger.info(cur.mogrify(query, params))

        cur.execute(query, params)
        if fetch_all:
            result = cur.fetchall()
        else:
            result = cur.fetchone()

        return result

