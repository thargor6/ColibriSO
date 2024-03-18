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
from langchain.text_splitter import RecursiveCharacterTextSplitter

from backend.db_changelogs import apply_db_changelogs
from backend.openai import text_to_speech, simple_summary
from backend.sqlite import create_connection
import backend.constants as const
import os
from datetime import datetime

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
    return cur.lastrowid

def create_document(conn, document):
    sql = ''' INSERT INTO documents(caption, creation_date)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, document)
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
    conv_ids = [int(str(i)) for i in document_ids]
    keyword_array = split_keywords_into_like_expressions(keyword_string)
    sql = ''' SELECT document_id, id, document_type, language_id, text_content, filename, mime_type FROM document_parts 
       where document_id in ({ids})
       {keywords} 
       and exists (select 1 from document_parts_audio where document_parts_audio.document_id = document_parts.document_id and document_parts_audio.document_part_id = document_parts.id)
       order by document_id desc, id '''.format(
        ids=','.join('?' for _ in conv_ids),
        keywords = ' '.join('and lower(text_content) like ?' for _ in keyword_array)
    )
    cursor = conn.cursor()
    params = conv_ids + keyword_array
    cursor.execute(sql, params)
    return cursor.fetchall()

def fetch_all_audio_parts(conn, document_id, document_part_id):
    sql = ''' SELECT id, document_id, document_part_id, model_id, voice_id, audio_size, mime_type  FROM document_parts_audio 
       where document_id=? and document_part_id=?
       order by id desc '''
    cursor = conn.cursor()
    params = (document_id, document_part_id)
    cursor.execute(sql, params)
    return cursor.fetchall()

def fetch_audio_data(conn, audio_id):
    sql = ''' SELECT audio_content FROM document_parts_audio 
       where id=?'''
    cursor = conn.cursor()
    params = (audio_id, )
    cursor.execute(sql, params)
    audio = cursor.fetchone()
    return audio[0] if audio is not None else None

def fetch_podcast_parts(conn, podcast_ids, only_not_listened):
    conv_ids = [int(str(i)) for i in podcast_ids]
    sql = ''' SELECT id, podcast_id, audio_part_id, last_listened_time FROM podcast_parts 
       where podcast_id in ({ids})
       {listen_status}        
       order by podcast_id desc, id '''.format(
        ids = ', '.join('?' for _ in conv_ids),
        listen_status = "and last_listened_time is NULL" if only_not_listened else "")
    cursor = conn.cursor()
    cursor.execute(sql, conv_ids)
    return cursor.fetchall()

def update_podcast_parts_listened_status(conn, podcast_ids):
    conv_ids = [int(str(i)) for i in podcast_ids]
    sql = ''' UPDATE podcast_parts set last_listened_time = ? where id in ({ids}) '''.format(
        ids = ', '.join('?' for _ in conv_ids))
    cursor = conn.cursor()
    cursor.execute(sql, [datetime.now()] + conv_ids)

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
    return cur.lastrowid

def create_document_part_with_binary_content(conn, document_part):
    sql = ''' INSERT INTO document_parts(document_id, document_type, filename, blob_content, blob_size, mime_type)
              VALUES(?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, document_part)
    return cur.lastrowid

def create_document_part_audio(conn, document_part_audio):
    sql = ''' INSERT INTO document_parts_audio(document_id, document_part_id, model_id, voice_id, audio_content, audio_size, mime_type, creation_date, chunk_id, chunk_content)
              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, document_part_audio)
    return cur.lastrowid

def delete_document(conn, document_ids):
    conv_ids = [str(i) for i in document_ids]

    cursor = conn.cursor()

    del_document_parts_audio_sql = ''' DELETE FROM document_parts_audio where document_id in ({ids}) '''.format(
        ids=','.join('?' for _ in conv_ids))
    cursor.execute(del_document_parts_audio_sql, conv_ids)

    del_document_part_sql = ''' DELETE FROM document_parts where document_id in ({ids}) '''.format(
        ids=','.join('?' for _ in conv_ids))
    cursor.execute(del_document_part_sql, conv_ids)

    del_document_sql = ''' DELETE FROM documents where id in ({ids}) '''.format(
        ids=','.join('?' for _ in conv_ids))
    cursor.execute(del_document_sql, conv_ids)

    return cursor.fetchall()


def fetch_all_podcasts(conn, keyword_string, only_not_listened):
    keyword_array = split_keywords_into_like_expressions(keyword_string)
    sql = ''' SELECT id, creation_date, caption, language_id, model_id, voice_id FROM podcasts 
              WHERE caption is not null
              {keywords}       
              {listen_status}
              order by id desc '''.format(
        keywords = ' '.join('and lower(caption) like ?' for _ in keyword_array),
        listen_status = "and exists (select 1 from podcast_parts where podcast_parts.podcast_id = podcasts.id and last_listened_time is NULL) or not exists (select 1 from podcast_parts where podcast_parts.podcast_id = podcasts.id)" if only_not_listened else "")
    cursor = conn.cursor()
    cursor.execute(sql, keyword_array)
    return cursor.fetchall()


def create_podcast(conn, podcast):
    sql = ''' INSERT INTO podcasts(creation_date, caption, language_id, model_id, voice_id)
              VALUES(?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, podcast)
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

    return cursor.fetchall()


def add_document_to_podcast(conn, podcast_id, doc_id):
    # check if document already exists in podcast
    parts_exists_sql = ''' SELECT 1 FROM podcast_parts, document_parts_audio where podcast_id = ?
              and podcast_parts.audio_part_id = document_parts_audio.id 
              and document_parts_audio.document_id = ? 
          '''
    cursor = conn.cursor()
    try:
        cursor.execute(parts_exists_sql, (int(podcast_id), int(doc_id)))
        parts_exists = cursor.fetchone()
    finally:
        cursor.close()
    if not parts_exists is None:
        return False

    # select desired podcast data
    select_podcast_sql = ''' SELECT caption, language_id, model_id, voice_id FROM podcasts 
                        WHERE id=?'''
    cursor = conn.cursor()
    try:
        cursor.execute(select_podcast_sql, (int(podcast_id),))
        podcast_info = cursor.fetchone()
        if podcast_info is None:
            return False
    finally:
        cursor.close()
    voice = podcast_info[3]
    model = podcast_info[2]

    # select document parts
    parts_rows = fetch_all_document_parts(conn, (doc_id,), "")

    # iterate over parts and add comprehensive summary to podcast, if available
    for row in parts_rows:
        document_type = row[2]
        document_content = row[4]
        document_id = row[0]
        document_part_id = row[1]
        if document_content is not None and document_type == const.PART_SUMMARY_COMPREHENSIVE:
            add_podcast_part(conn, document_content, document_id, document_part_id, model, podcast_id,
                             voice)
            return True

    # iterate over parts and add brief summary to podcast, if available
    for row in parts_rows:
        document_type = row[2]
        document_content = row[4]
        document_id = row[0]
        document_part_id = row[1]
        if document_content is not None and document_type == const.PART_SUMMARY_BRIEF:
            add_podcast_part(conn, document_content, document_id, document_part_id, model, podcast_id,
                             voice)
            return True
    # no valid part found, nothing added
    return False

def add_podcast_part(conn, document_content, document_id, document_part_id, model, podcast_id, voice):
    # check if audio part exists
    audio_parts_exists_sql = ''' SELECT id FROM document_parts_audio where document_part_id = ? order by id'''
    cursor = conn.cursor()

    try:
      cursor.execute(audio_parts_exists_sql, (int(document_id),))
      audio_part_ids = cursor.fetchall()
    finally:
      cursor.close()

    # create audio if not exists
    if len(audio_part_ids) == 0:
        audio_part_ids = []

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = const.OPENAI_DFLT_SPEECH_CHUNKSIZE,
            chunk_overlap  = 0,
            length_function = len,
        )
        splitted_texts = text_splitter.split_text(document_content)


        chunk_id = 1
        for chunk_content in splitted_texts:
            audio_path = text_to_speech(chunk_content, voice, model)
            try:
                in_file = open(audio_path, "rb")
                try:
                    audio_data = in_file.read()
                finally:
                    in_file.close()
                audio_part = (int(document_id), int(document_part_id), model, voice, audio_data, len(audio_data), const.MIMETYPE_MP3, datetime.now(), chunk_id, chunk_content)
                new_audio_part = create_document_part_audio(conn, audio_part)
                audio_part_ids.append(new_audio_part)
                chunk_id += 1
            finally:
                os.remove(audio_path)

    for audio_part_id in audio_part_ids:
        podcast_part = (int(podcast_id), int(audio_part_id))
        podcast_insert_sql = ''' INSERT INTO podcast_parts(podcast_id, audio_part_id)
                              VALUES(?, ?) '''
        cur = conn.cursor()
        cur.execute(podcast_insert_sql, podcast_part)

def create_summary_for_document(conn, document_id, summary_type, summary_language_id, overwrite = False):
    if overwrite:
        # delete existing summary
        del_summary_sql = ''' DELETE FROM document_parts where document_id = ? and document_type=? and language_id=?'''
        cursor = conn.cursor()
        try:
            cursor.execute(del_summary_sql, (int(document_id), summary_type, summary_language_id))
        finally:
            cursor.close()
    # check if document already has summary
    parts_exists_sql = '''SELECT 1 FROM document_parts where document_id = ?
              and document_type = ? and language_id = ?'''
    cursor = conn.cursor()
    try:
        cursor.execute(parts_exists_sql, (int(document_id), summary_type, summary_language_id))
        parts_exists = cursor.fetchone()
    finally:
        cursor.close()
    if not parts_exists is None:
        return False

    # select document content
    select_content_sql = '''SELECT text_content FROM document_parts where document_id = ?
              and document_type = ?'''
    cursor = conn.cursor()
    try:
        cursor.execute(select_content_sql, (int(document_id), const.PART_CONTENT))
        content_data = cursor.fetchone()
    finally:
        cursor.close()
    if content_data is None:
        return False

    brief_summary = summary_type == const.PART_SUMMARY_BRIEF

    document_content = content_data[0]
    summary = create_chunked_summary(brief_summary, document_content, summary_language_id)

    document_part_summary = (int(document_id), summary_type, summary_language_id, summary)
    create_document_part_with_text_content(conn, document_part_summary)


def create_chunked_summary(brief_summary, document_content, summary_language_id):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = const.OPENAI_DFLT_SUMMARY_CHUNKSIZE,
        chunk_overlap  = 50,
        length_function = len,
    )
    splitted_texts = text_splitter.split_text(document_content)
    if len(splitted_texts) == 1:
        summary = simple_summary(const.getLanguageCaption(summary_language_id), document_content, brief_summary)
    else:
        chunk_summaries = ""
        for chunk_content in splitted_texts:
            chunk_summary = simple_summary(const.getLanguageCaption(summary_language_id), chunk_content, brief_summary)
            chunk_summaries += chunk_summary + " "
        summary = create_chunked_summary(brief_summary, chunk_summaries, summary_language_id)
    return summary

