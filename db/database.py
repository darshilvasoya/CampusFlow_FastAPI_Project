from contextlib import contextmanager
import psycopg2 # Changed import
from psycopg2 import Error # Import Error for specific exception handling
import psycopg2.extras # For dictionary cursor
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
        connection.autocommit = False # Explicitly set autocommit for psycopg2
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) # Use RealDictCursor

        yield cursor

        if commit:
            connection.commit()

    except Error as e: # Changed exception type
        if connection:
            connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()