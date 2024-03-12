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

def create_document(conn, document):
    sql = ''' INSERT INTO documents(caption, creation_date)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, document)
    conn.commit()
    return cur.lastrowid

def fetch_all_documents(conn, keyword_string):
    keyword_array = split_keywords_into_like_expressions(keyword_string)
    sql = ''' SELECT id, creation_date, caption FROM documents 
              WHERE caption is not null
              {keywords}       
              order by id desc '''.format(
        keywords = ' '.join('and lower(caption) like ?' for _ in keyword_array))
    cursor = conn.cursor()
    cursor.execute(sql, keyword_array)
    return cursor.fetchall()

def fetch_all_document_parts(conn, document_ids, keyword_string):
    conv_ids = [str(i) for i in document_ids]
    keyword_array = split_keywords_into_like_expressions(keyword_string)
    sql = ''' SELECT document_id, id, document_type, language_id, text_content, filename, mime_type FROM document_parts 
       where document_id in ({ids})
       {keywords} 
       order by document_id desc, id '''.format(
        ids=','.join('?' for _ in conv_ids),
        keywords = ' '.join('and lower(text_content) like ?' for _ in keyword_array)
    )
    cursor = conn.cursor()
    params = conv_ids + keyword_array
    cursor.execute(sql, params)
    return cursor.fetchall()

def fetch_all_document_parts_with_audio(conn, document_ids, keyword_string):
    conv_ids = [str(i) for i in document_ids]
    keyword_array = split_keywords_into_like_expressions(keyword_string)
    sql = ''' SELECT document_id, id, document_type, language_id, text_content, filename, mime_type FROM document_parts 
       where document_id in ({ids})
       {keywords} 
       and exists (select 1 from document_part_audio where document_part_audio.document_id = document_parts.document_id and document_part_audio.document_part_id = document_parts.id)
       order by document_id desc, id '''.format(
        ids=','.join('?' for _ in conv_ids),
        keywords = ' '.join('and lower(text_content) like ?' for _ in keyword_array)
    )
    cursor = conn.cursor()
    params = conv_ids + keyword_array
    cursor.execute(sql, params)
    return cursor.fetchall()

def fetch_all_audio_parts(conn, document_id, document_part_id):
    sql = ''' SELECT id, document_id, document_part_id, model_id, voice_id, audio_size, mime_type  FROM document_part_audio 
       where document_id=? and document_part_id=?
       order by id desc '''
    cursor = conn.cursor()
    params = (document_id, document_part_id)
    cursor.execute(sql, params)
    return cursor.fetchall()

def fetch_audio_data(conn, audio_id):
    sql = ''' SELECT audio_content FROM document_part_audio 
       where id=?'''
    cursor = conn.cursor()
    params = (audio_id, )
    cursor.execute(sql, params)
    audio = cursor.fetchone()
    return audio[0] if audio is not None else None

def split_keywords_into_like_expressions(keywords):
    if keywords is None:
        return []
    filtered_array =  list(filter(None, keywords.split(' ')))
    return list(map(lambda x: '%' +  x.lower() + '%', filtered_array))

def fetch_all_document_summary_parts(conn, document_ids, keyword_string):
    conv_ids = [str(i) for i in document_ids]
    keyword_array = split_keywords_into_like_expressions(keyword_string)

    sql = ''' SELECT document_id, id, document_type, language_id, text_content, filename, mime_type FROM document_parts 
       where document_id in ({ids}) and document_type in (?,?) 
       {keywords}
       order by document_id desc, document_type, id '''.format(
          ids = ', '.join('?' for _ in conv_ids),
          keywords = ' '.join('and lower(text_content) like ?' for _ in keyword_array))

    print("SQL", sql)
    cursor = conn.cursor()
    params = conv_ids + [const.PART_SUMMARY_BRIEF, const.PART_SUMMARY_COMPREHENSIVE] + keyword_array
    print("PARAMS", params)
    cursor.execute(sql, params)
    return cursor.fetchall()

def create_document_part_with_text_content(conn, document_part):
    sql = ''' INSERT INTO document_parts(document_id, document_type, language_id, text_content)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, document_part)
    conn.commit()
    return cur.lastrowid

def create_document_part_with_binary_content(conn, document_part):
    sql = ''' INSERT INTO document_parts(document_id, document_type, filename, blob_content, blob_size, mime_type)
              VALUES(?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, document_part)
    conn.commit()
    return cur.lastrowid

def create_document_part_audio(conn, document_part_audio):
    sql = ''' INSERT INTO document_parts_audio(document_id, document_part_id, model_id, voice_id, audio_content, audio_size, mime_type)
              VALUES(?, ?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, document_part_audio)
    conn.commit()
    return cur.lastrowid

def delete_document(conn, document_ids):
    conv_ids = [str(i) for i in document_ids]

    cursor = conn.cursor()

    del_document_part_audio_sql = ''' DELETE FROM document_parts_audio where document_id in ({ids}) '''.format(
        ids=','.join('?' for _ in conv_ids))
    cursor.execute(del_document_part_audio_sql, conv_ids)

    del_document_part_sql = ''' DELETE FROM document_parts where document_id in ({ids}) '''.format(
        ids=','.join('?' for _ in conv_ids))
    cursor.execute(del_document_part_sql, conv_ids)

    del_document_sql = ''' DELETE FROM documents where id in ({ids}) '''.format(
        ids=','.join('?' for _ in conv_ids))
    cursor.execute(del_document_sql, conv_ids)

    conn.commit()
    return cursor.fetchall()


def fetch_all_podcasts(conn, keyword_string):
    keyword_array = split_keywords_into_like_expressions(keyword_string)
    sql = ''' SELECT id, creation_date, caption, language_id, model_id, voice_id FROM podcasts 
              WHERE caption is not null
              {keywords}       
              order by id desc '''.format(
        keywords = ' '.join('and lower(caption) like ?' for _ in keyword_array))
    cursor = conn.cursor()
    cursor.execute(sql, keyword_array)
    return cursor.fetchall()


def create_podcast(conn, podcast):
    sql = ''' INSERT INTO podcasts(creation_date, caption, language_id, model_id, voice_id)
              VALUES(?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, podcast)
    conn.commit()
    return cur.lastrowid


def delete_podcast(conn, document_ids):
    conv_ids = [str(i) for i in document_ids]

    cursor = conn.cursor()

    del_podcast_part_sql = ''' DELETE FROM podcast_parts where podcast_id in ({ids}) '''.format(
        ids=','.join('?' for _ in conv_ids))
    cursor.execute(del_podcast_part_sql, conv_ids)

    del_podcast_sql = ''' DELETE FROM podcasts where id in ({ids}) '''.format(
        ids=','.join('?' for _ in conv_ids))
    cursor.execute(del_podcast_sql, conv_ids)

    conn.commit()
    return cursor.fetchall()