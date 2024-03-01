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

from backend.db_changelogs import apply_db_changelogs
from backend.sqlite import create_connection
import backend.constants as const

DATABASE = r"colibri_database.db"


db_checked = False

def connect_to_colibri_db():
    """ connect to the database and initialize it, if necessary
    :return: Connection object or None
    """
    conn = create_connection(DATABASE)
    try:
        global db_checked
        if not db_checked:
            db_checked = True
            apply_db_changelogs(conn)
    except:
        conn.close()
        return None
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

def fetch_all_snippets(conn, keyword_string):
    """
    Fetch all snippets from the snippet table
    :param conn:
    :param project:
    :return: snippets
    """
    keyword_array = split_keywords_into_like_expressions(keyword_string)
    sql = ''' SELECT id, creation_date, caption FROM snippets 
              WHERE caption is not null
              {keywords}       
              order by id desc '''.format(
        keywords = ' '.join('and lower(caption) like ?' for _ in keyword_array))
    cursor = conn.cursor()
    cursor.execute(sql, keyword_array)
    return cursor.fetchall()

def fetch_all_snippet_parts(conn, snippet_ids, keyword_string):
    """
    Fetch all snippets from the snippet table
    :param conn:
    :param project:
    :return: snippets
    """
    conv_ids = [str(i) for i in snippet_ids]
    keyword_array = split_keywords_into_like_expressions(keyword_string)
    sql = ''' SELECT snippet_id, id, snippet_type, language_id, text_content, filename, mime_type FROM snippet_parts 
       where snippet_id in ({ids})
       {keywords} 
       order by snippet_id desc, id '''.format(
        ids=','.join('?' for _ in conv_ids),
        keywords = ' '.join('and lower(text_content) like ?' for _ in keyword_array)
    )
    cursor = conn.cursor()
    params = conv_ids + keyword_array
    cursor.execute(sql, params)
    return cursor.fetchall()

def split_keywords_into_like_expressions(keywords):
    if keywords is None:
        return []
    filtered_array =  list(filter(None, keywords.split(' ')))
    return list(map(lambda x: '%' +  x.lower() + '%', filtered_array))

def fetch_all_snippet_summary_parts(conn, snippet_ids, keyword_string):
    """
    Fetch all summary snippets from the snippet table
    :param conn:
    :param project:
    :return: snippets
    """
    conv_ids = [str(i) for i in snippet_ids]
    keyword_array = split_keywords_into_like_expressions(keyword_string)

    sql = ''' SELECT snippet_id, id, snippet_type, language_id, text_content, filename, mime_type FROM snippet_parts 
       where snippet_id in ({ids}) and snippet_type in (?,?) 
       {keywords}
       order by snippet_id desc, snippet_type, id '''.format(
          ids = ', '.join('?' for _ in conv_ids),
          keywords = ' '.join('and lower(text_content) like ?' for _ in keyword_array))

    print("SQL", sql)
    cursor = conn.cursor()
    params = conv_ids + [const.PART_SUMMARY_BRIEF, const.PART_SUMMARY_COMPREHENSIVE] + keyword_array
    print("PARAMS", params)
    cursor.execute(sql, params)
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



