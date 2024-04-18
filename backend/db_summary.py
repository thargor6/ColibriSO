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

from backend.database import create_document_part_with_text_content
from backend.openai import simple_summary
import backend.constants as const

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
    return True


def split_text(document_content):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = const.OPENAI_DFLT_SUMMARY_CHUNKSIZE,
        chunk_overlap  = 50,
        length_function = len,
    )
    splitted_texts = text_splitter.split_text(document_content)
    return splitted_texts


def create_chunked_summary(brief_summary, document_content, summary_language_id, progress_bar, chunk_count):
    splitted_texts = split_text(document_content)
    if len(splitted_texts) == 1:
        summary = simple_summary(const.getLanguageCaption(summary_language_id), document_content, brief_summary)
        if progress_bar is not None:
            progress_bar.progress(1.0)
    else:
        chunk_summaries = ""
        counter = 0
        for chunk_content in splitted_texts:
            chunk_summary = simple_summary(const.getLanguageCaption(summary_language_id), chunk_content, brief_summary)
            chunk_summaries += chunk_summary + " "
            if progress_bar is not None:
                counter += 1
                progress_bar.progress((counter + 1) / (chunk_count+1))
        summary = create_chunked_summary(brief_summary, chunk_summaries, summary_language_id,None, None)
    return summary

