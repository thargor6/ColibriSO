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

import streamlit as st
from backend.database import connect_to_colibri_db, create_document, create_document_part_with_text_content, \
    create_document_part_with_binary_content, fetch_all_notes
from datetime import datetime
from backend import constants as const
from backend.db_tags import fetch_all_tags, create_document_tag
import pandas as pd

from frontend.utils import dataframe_with_selections


def load_view():
    st.title('Notes')
    st.subheader('Create a new note')

    conn = connect_to_colibri_db()
    try:
        tag_rows = fetch_all_tags(conn)
        all_tags = [tag[2] for tag in tag_rows]
    finally:
        conn.close()

    col1, col2, col3 = st.columns(3)
    with col1:
      tag1 = st.selectbox('select a tag', all_tags, key='tag1', index=None)
    with col2:
      tag2 = st.selectbox('select a tag', all_tags, key='tag2', index=None)
    with col3:
      tag3 = st.selectbox('select a tag', all_tags, key='tag3', index=None)

    title = st.text_input('Title')
    note =  st.text_area("Note", height=120)

    if st.button('add note'):
        conn = connect_to_colibri_db()
        try:
            try:
                document = (title, datetime.now());
                document_id = create_document(conn, document)

                document_part_url = (document_id, const.PART_NOTE, None, note);
                create_document_part_with_text_content(conn, document_part_url)

                if tag1 is not None:
                    tag1_id = [tag[0] for tag in tag_rows if tag[2] == tag1][0]
                    print(document_id, tag1_id)
                    create_document_tag(conn, document_id, tag1_id)
                if tag2 is not None:
                    tag2_id = [tag[0] for tag in tag_rows if tag[2] == tag2][0]
                    create_document_tag(conn, document_id, tag2_id)
                if tag3 is not None:
                    tag3_id = [tag[0] for tag in tag_rows if tag[2] == tag3][0]
                    create_document_tag(conn, document_id, tag3_id)
            except:
                conn.rollback()
                raise
            conn.commit()
            st.success("Note successfully added")
        finally:
            conn.close()

    conn = connect_to_colibri_db()
    try:
        notes_rows = fetch_all_notes(conn, '')
    finally:
        conn.close()
    if st.button('Refresh'):
        st.write('Refreshing...')
        st.rerun()

    # more about data frames: # https://docs.streamlit.io/library/api-reference/data/st.dataframe
    notes_df = pd.DataFrame(notes_rows, columns=["Id", "Creation date", "Caption"])
    notes_selection = dataframe_with_selections(notes_df)
