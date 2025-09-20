from contextlib import contextmanager
import mysql.connector
import os

@contextmanager
def get_db_cursor(commit=False):
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME"),
            autocommit=False
        )
        cursor = connection.cursor(dictionary=True)

        yield cursor

        if commit:
            connection.commit()

    except Exception as e:
        if connection:
            connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()