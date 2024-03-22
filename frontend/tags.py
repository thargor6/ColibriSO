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
from backend.database import connect_to_colibri_db
from backend.db_tags import fetch_all_tags, delete_tags, create_tag
from frontend.utils import dataframe_with_selections
import pandas as pd
from datetime import datetime

def load_view():
    st.title('Tags')
    st.subheader('Create a new tag')
    tag_name = st.text_input('tag name')
    if st.button('create tag'):
        conn = connect_to_colibri_db()
        try:
            try:
                tag = (datetime.now(), tag_name);
                tag_id = create_tag(conn, tag)
            except:
                conn.rollback()
                raise
            conn.commit()
        finally:
            conn.close()

    conn = connect_to_colibri_db()
    try:
        tag_rows = fetch_all_tags(conn)
    finally:
        conn.close()
    if st.button('Refresh'):
        st.write('Refreshing...')
        st.rerun()

    # more about data frames: # https://docs.streamlit.io/library/api-reference/data/st.dataframe
    tags_df = pd.DataFrame(tag_rows, columns=["Id", "Creation date", "Tag name"])
    tags_selection = dataframe_with_selections(tags_df)

    col1, col2 = st.columns(2)
    with col2:
        deleteButton = st.button('Delete tags')
        confirmDelete = st.checkbox("Confirm delete")


    if deleteButton and confirmDelete:
        if len(tags_selection["Id"].values) > 0:
            with st.spinner('Deleting podcasts ...'):
                conn = connect_to_colibri_db()
                try:
                    delete_tags(conn, tags_selection["Id"].values)
                    conn.commit()
                finally:
                    conn.close()
            st.success("Documents successfully deleted")
            st.rerun()
