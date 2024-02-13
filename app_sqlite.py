import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)



def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid


def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid


def create_snippet(conn, snippet):
    """
    Create a new snippet into the snippet table
    :param conn:
    :param project:
    :return: snippet id
    """
    sql = ''' INSERT INTO snippets(caption, begin_date)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, snippet)
    conn.commit()
    return cur.lastrowid

def create_snippet_part(conn, snippet_part):
    """
    Create a new snippet into the snippet table
    :param conn:
    :param project:
    :return: snippet id
    """
    sql = ''' INSERT INTO snippet_parts(snippet_id, snippet_type, language_id, content)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, snippet_part)
    conn.commit()
    return cur.lastrowid
