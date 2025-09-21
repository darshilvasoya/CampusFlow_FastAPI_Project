from contextlib import contextmanager
import psycopg2
from psycopg2 import Error
import psycopg2.extras
import os

@contextmanager
def get_db_cursor(commit=False):
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "postgres"),
            password=os.environ.get("DB_PASSWORD", "password"),
            database=os.environ.get("DB_NAME", "student_database")
        )
        connection.autocommit = False
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        yield cursor

        if commit:
            connection.commit()

    except Error as e:
        if connection:
            connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
