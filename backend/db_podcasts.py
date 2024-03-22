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

from backend.database import split_keywords_into_like_expressions, create_document_part_audio, fetch_all_document_parts
from backend.openai import text_to_speech
import backend.constants as const
import os
from datetime import datetime

def fetch_podcast_parts(conn, podcast_ids, only_not_listened):
    conv_ids = [int(str(i)) for i in podcast_ids]
    sql = ''' SELECT podcast_parts.id, podcast_parts.podcast_id, podcast_parts.audio_part_id, podcast_parts.last_listened_time, documents.caption
              FROM podcast_parts, document_parts_audio, documents 
       where podcast_id in ({ids})
       {listen_status}  
       and document_parts_audio.id = podcast_parts.audio_part_id
       and documents.id = document_parts_audio.document_id        
       order by podcast_parts.podcast_id desc, podcast_parts.id '''.format(
        ids = ', '.join('?' for _ in conv_ids),
        listen_status = "and podcast_parts.last_listened_time is NULL" if only_not_listened else "")
    cursor = conn.cursor()
    cursor.execute(sql, conv_ids)
    return cursor.fetchall()

def update_podcast_parts_listened_status(conn, podcast_id):
    sql = ''' UPDATE podcast_parts set last_listened_time = ? where id = ?'''
    cursor = conn.cursor()
    params = [datetime.now(), int(podcast_id)]
    print(params)
    cursor.execute(sql, params)

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
        cursor.execute(audio_parts_exists_sql, (int(document_part_id),))
        audio_part_ids = cursor.fetchall()
        # map from tuple to int, e.g. (1,) -> 1
        audio_part_ids = [audio_part_id[0] for audio_part_id in audio_part_ids]
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
