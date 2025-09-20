from contextlib import contextmanager
import mysql.connector


@contextmanager
def get_db_cursor(commit=False):
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="campusflow.mysql.pythonanywhere-services.com",
            user="campusflow",
            password="czon@2510",
            database="campusflow$student_database",
            autocommit=False  # Important: handle transactions manually
        )
        cursor = connection.cursor(dictionary=True)

        yield cursor

        # Commit only if requested and no exceptions occurred
        if commit:
            connection.commit()

    except Exception as e:
        # If any error occurs, rollback the transaction
        if connection:
            connection.rollback()
        raise e  # Re-raise the exception
    finally:
        # Always close cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()