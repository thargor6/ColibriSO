from app_sqlite import create_connection, create_table
from sqlite3 import Error

DATABASE = r"colibri_database.db"

SQL_CREATE_SNIPPETS_TABLE = """ CREATE TABLE IF NOT EXISTS snippets (
                                        id integer PRIMARY KEY,
                                        begin_date text,
                                        caption text NOT NULL
                                    ); """

SQL_CREATE_SNIPPET_PARTS_TABLE = """ CREATE TABLE IF NOT EXISTS snippet_parts (
                                        id integer PRIMARY KEY,
                                        snippet_id integer NOT NULL,
                                        snippet_type text NOT NULL,
                                        language_id text NOT NULL,
                                        content text NOT NULL
                                    ); """

def connect_to_colibri_db():
    """ connect to the database and initilize it, if necessary
    :return: Connection object or None
    """
    conn = create_connection(DATABASE)
    # create tables
    if conn is not None:
        create_table(conn, SQL_CREATE_SNIPPETS_TABLE)
        create_table(conn, SQL_CREATE_SNIPPET_PARTS_TABLE)
    else:
        print("Error! cannot create the database connection.")
    return conn