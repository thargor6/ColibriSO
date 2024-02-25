# MIT License
#
# ColibriSO - a tool for organizing information of all kinds, written in Python and Streamlit.
# Copyright (C) 2022-2024 Andreas Maschke
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from app_sqlite import create_connection, create_table
from datetime import datetime

DATABASE = r"colibri_database.db"

SQL_CREATE_SNIPPETS_TABLE = """ CREATE TABLE IF NOT EXISTS snippets (
                                        id integer PRIMARY KEY,
                                        creation_date text,
                                        caption text NOT NULL
                                    ); """

SQL_CREATE_SNIPPET_PARTS_TABLE = """ CREATE TABLE IF NOT EXISTS snippet_parts (
                                        id integer PRIMARY KEY,
                                        snippet_id integer NOT NULL,
                                        snippet_type text NOT NULL,
                                        language_id text NULL,
                                        text_content text NULL,
                                        filename text NULL,
                                        blob_content blob NULL,
                                        mime_type text NULL
                                    ); """

SQL_CREATE_USERS_TABLE = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        creation_time text NOT NULL,
                                        user_name text NOT NULL,
                                        pw_hash text NOT NULL,
                                        email text NOT NULL,
                                        open_ai_api_key text NULL                                                                                
                                    ); """

SQL_CREATE_USER_SESSIONS_TABLE = """ CREATE TABLE IF NOT EXISTS user_sessions (
                                        id integer PRIMARY KEY,
                                        creation_time text NOT NULL,
                                        user_id integer NOT NULL,
                                        session_id text NOT NULL                                        
                                    ); """

def populate_users_table(conn):
    rowsQuery = "SELECT Count() FROM users"
    cursor = conn.cursor()
    cursor.execute(rowsQuery)
    numberOfRows = cursor.fetchone()[0]
    if numberOfRows == 0:
      create_user(conn, (datetime.now(), 'thargor6', encrypt_password('software1'), "thargor6@googlemail.com"))

def connect_to_colibri_db():
    """ connect to the database and initialize it, if necessary
    :return: Connection object or None
    """
    conn = create_connection(DATABASE)
    # create tables
    if conn is not None:
        create_table(conn, SQL_CREATE_SNIPPETS_TABLE)
        create_table(conn, SQL_CREATE_SNIPPET_PARTS_TABLE)
        create_table(conn, SQL_CREATE_USERS_TABLE)
        populate_users_table(conn)
        create_table(conn, SQL_CREATE_USER_SESSIONS_TABLE)
    else:
        print("Error! cannot create the database connection.")
    return conn

def create_user(conn, user):
    """
    Create a new user into the users table
    :param conn:
    :param project:
    :return: user id
    """
    sql = ''' INSERT INTO users(creation_time, user_name, pw_hash, email)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

def update_user(conn, user_id, open_ai_api_key):
    """
    Update a user in the users table
    :param conn:
    :param project:
    :return: user id
    """
    sql = ''' UPDATE users set open_ai_api_key = ? where id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (open_ai_api_key, user_id))
    conn.commit()

def select_user_by_user_name(conn, user_id):
    """
    Query user by user_id
    :param conn: the Connection object
    :param user_id:
    :return:
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_name=?", (user_id,))
    return cursor.fetchone()

def select_user_by_user_id(conn, user_id):
    """
    Query user by user_id
    :param conn: the Connection object
    :param user_id:
    :return:
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    return cursor.fetchone()

def select_session_by_session_id(conn, session_id):
    """
    Query session by session_id
    :param conn: the Connection object
    :param session_id:
    :return:
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_sessions WHERE session_id=?", (session_id,))
    return cursor.fetchone()

def create_session(conn, session):
    """
    Create a new session into the sessions table
    :param conn:
    :param session
    :return: session id
    """
    sql = ''' INSERT INTO user_sessions(creation_time,user_id, session_id)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, session)
    conn.commit()
    return cur.lastrowid

def create_snippet(conn, snippet):
    """
    Create a new snippet into the snippet table
    :param conn:
    :param project:
    :return: snippet id
    """
    sql = ''' INSERT INTO snippets(caption, creation_date)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, snippet)
    conn.commit()
    return cur.lastrowid

def fetch_all_snippets(conn):
    """
    Fetch all snippets from the snippet table
    :param conn:
    :param project:
    :return: snippets
    """
    sql = ''' SELECT id, creation_date, caption FROM snippets order by id desc '''
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def fetch_all_snippet_parts(conn, snippet_ids):
    """
    Fetch all snippets from the snippet table
    :param conn:
    :param project:
    :return: snippets
    """
    conv_ids = [str(i) for i in snippet_ids]
    sql = ''' SELECT snippet_id, id, snippet_type, language_id, text_content, filename, mime_type FROM snippet_parts 
       where snippet_id in ({}) order by snippet_id desc, id '''.format(','.join('?' for _ in conv_ids))
    cursor = conn.cursor()
    cursor.execute(sql, conv_ids)
    return cursor.fetchall()

def create_snippet_part_with_text_content(conn, snippet_part):
    """
    Create a new snippet into the snippet table
    :param conn:
    :param project:
    :return: snippet id
    """
    sql = ''' INSERT INTO snippet_parts(snippet_id, snippet_type, language_id, text_content)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, snippet_part)
    conn.commit()
    return cur.lastrowid

def create_snippet_part_with_binary_content(conn, snippet_part):
    """
    Create a new snippet into the snippet table
    :param conn:
    :param project:
    :return: snippet id
    """
    sql = ''' INSERT INTO snippet_parts(snippet_id, snippet_type, filename, blob_content, mime_type)
              VALUES(?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, snippet_part)
    conn.commit()
    return cur.lastrowid

def encrypt_password(password):
    import hashlib
    import hmac
    key = "b1963175-a4be-4096-8d38-53bf19ec"
    byte_key = key.encode("UTF-8")
    message = password.encode()
    h = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
    return h

def compare_password_hash(password, ref_hash):
    return ref_hash == encrypt_password(password)

