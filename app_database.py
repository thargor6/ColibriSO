from app_sqlite import create_connection, create_table
from sqlite3 import Error

DATABASE = r"colibri_database.db"

SQL_CREATE_LOOKUPS_TABLE = """ CREATE TABLE IF NOT EXISTS lookups (
                                        id integer PRIMARY KEY,
                                        lookup_id text NOT NULL
                                    ); """

SQL_CREATE_LOOKUP_TEXTS_TABLE = """ CREATE TABLE IF NOT EXISTS lookup_texts (
                                        id integer PRIMARY KEY,
                                        lookup_id text NOT NULL,
                                        lookup_text text NOT NULL
                                    ); """


SQL_CREATE_LANGUAGES_TABLE = """ CREATE TABLE IF NOT EXISTS languages (
                                        id integer PRIMARY KEY,
                                        language_code text NOT NULL
                                    ); """


SQL_CREATE_SNIPPETS_TABLE = """ CREATE TABLE IF NOT EXISTS snippets (
                                        id integer PRIMARY KEY,
                                        caption text NOT NULL
                                    ); """

SQL_CREATE_SNIPPET_PARTS_TABLE = """ CREATE TABLE IF NOT EXISTS snippet_parts (
                                        id integer PRIMARY KEY,
                                        snippet_id integer NOT NULL,
                                        language_id integer NOT NULL,
                                        content text NOT NULL
                                    ); """


SQL_CREATE_PROJECTS_TABLE = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

SQL_CREATE_TASKS_TABLE = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                     );"""

def populate_lookups(conn):
    """ created default lookups
    :param conn: Connection object
    :return:
    """
    try:
        c = conn.cursor()
        c.execute("select count(*) from lookups")
        count = c.fetchone()[0]
        if count == 0:
            c.execute("INSERT INTO lookups (lookup_id) VALUES ('de')")
            c.execute("INSERT INTO lookups (lookup_id) VALUES ('en')")
            c.execute("INSERT INTO lookups (lookup_id) VALUES ('fa')")
            conn.commit()
    except Error as e:
        print(e)

def populate_lookup_texts(conn):
    """ created default lookup texts
    :param conn: Connection object
    :return:
    """
    try:
        c = conn.cursor()
        c.execute("select count(*) from lookup_texts")
        count = c.fetchone()[0]
        if count == 0:
            c.execute("INSERT INTO lookup_texts (lookup_id, lookup_text) VALUES ('de', 'German')")
            c.execute("INSERT INTO lookup_texts (lookup_id, lookup_text) VALUES ('en', 'English')")
            c.execute("INSERT INTO lookup_texts (lookup_id, lookup_text) VALUES ('fa', 'Persian')")
            conn.commit()

    except Error as e:
        print(e)

def populate_languages(conn):
    """ created default lookup texts
    :param conn: Connection object
    :return:
    """
    try:
        c = conn.cursor()
        c.execute("select count(*) from languages")
        count = c.fetchone()[0]
        if count == 0:
            c.execute("INSERT INTO languages (language_code) VALUES ('de')")
            c.execute("INSERT INTO languages (language_code) VALUES ('en')")
            c.execute("INSERT INTO languages (language_code) VALUES ('fa')")
            conn.commit()

    except Error as e:
        print(e)

def connect_to_colibri_db():
    """ connect to the database and initilize it, if necessary
    :return: Connection object or None
    """
    conn = create_connection(DATABASE)
    # create tables
    if conn is not None:
        create_table(conn, SQL_CREATE_LOOKUPS_TABLE)
        populate_lookups(conn)
        create_table(conn, SQL_CREATE_LOOKUP_TEXTS_TABLE)
        populate_lookup_texts(conn)
        create_table(conn, SQL_CREATE_LANGUAGES_TABLE)
        populate_languages(conn)
        create_table(conn, SQL_CREATE_SNIPPETS_TABLE)
        create_table(conn, SQL_CREATE_SNIPPET_PARTS_TABLE)
        create_table(conn, SQL_CREATE_PROJECTS_TABLE)
        create_table(conn, SQL_CREATE_TASKS_TABLE)
    else:
        print("Error! cannot create the database connection.")
    return conn