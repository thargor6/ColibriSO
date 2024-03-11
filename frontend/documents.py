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

# https://docs.streamlit.io/library/api-reference/layout

from backend.database import connect_to_colibri_db, fetch_all_documents, delete_document
import pandas as pd

from frontend.show_audio_content_detail import showAudioContent
from frontend.show_content_detail import showContent
from frontend.show_details_detail import showDetails
from frontend.show_summary_detail import showSummary
from frontend.text_to_speech_detail import textToSpeech
from frontend.utils import dataframe_with_selections


def load_view():
    st.title('Documents')
    documents_keyword_string = st.text_input('Document keywords', value="")
    conn = connect_to_colibri_db()
    try:
        snippet_rows = fetch_all_documents(conn, documents_keyword_string)
    finally:
        conn.close()
    if st.button('Refresh'):
        st.write('Refreshing...')
        st.rerun()

    # more about data frames: # https://docs.streamlit.io/library/api-reference/data/st.dataframe
    snippet_df = pd.DataFrame(snippet_rows, columns=["Id", "Creation date", "Caption"])
    snippet_selection = dataframe_with_selections(snippet_df)

    st.title('Document parts')
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        showSummaryButton = st.button('Show summary')
    with col2:
        listenAudioButton = st.button('Listen')
    with col3:
        showContentButton = st.button('Show content')
    with col4:
        showDetailsButton = st.button('Show details')
    with col5:
        deleteButton = st.button('Delete documents')
        confirmDelete = st.checkbox("Confirm delete")
    with col6:
        textToSpeechButton = st.button('TextToSpeech')

    #print(snippet_selection["Id"])
    #print(snippet_selection["Id"].values)
    #print(len(snippet_selection["Id"].values))

    parts_keyword_string = st.text_input('Content keywords', value="")
    details = st.expander("Details", expanded=True)

    if showSummaryButton:
        showSummary(details, snippet_selection, parts_keyword_string)
    if showDetailsButton:
        showDetails(details, snippet_selection, parts_keyword_string)
    if showContentButton:
        showContent(details, snippet_selection, parts_keyword_string)
    if deleteButton and confirmDelete:
        if len(snippet_selection["Id"].values) > 0:
            with st.spinner('Deleting documents ...'):
                conn = connect_to_colibri_db()
                try:
                    delete_document(conn, snippet_selection["Id"].values)
                finally:
                    conn.close()
            st.success("Documents successfully deleted")
            st.rerun()
    if textToSpeechButton:
        if textToSpeech(details, snippet_selection, parts_keyword_string) > 0:
            st.success("Text to speech successfully created")
            st.rerun()
    if listenAudioButton:
        showAudioContent(details, snippet_selection, parts_keyword_string)
        pass
