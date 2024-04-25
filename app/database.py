import psycopg2
import psycopg2.extras


def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database.

    Returns:
        psycopg2 connection object if successful, None otherwise.
    """
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='postgres',
            user='postgres',
            password='ratestask'
        )
        # Return the connection object
        return conn
    except psycopg2.Error as e:
        # Print error message if connection fails
        print("Unable to connect to the database:", str(e))
        # Return None if connection fails
        return None
