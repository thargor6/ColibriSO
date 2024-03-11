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

from backend.database import connect_to_colibri_db, fetch_all_documents, delete_document, fetch_all_document_parts, \
    create_document_part_audio, fetch_all_podcasts
import pandas as pd

from frontend.show_audio_content_detail import showAudioContent
from frontend.show_content_detail import showContent
from frontend.show_details_detail import showDetails
from frontend.show_summary_detail import showSummary
from frontend.text_to_speech_detail import textToSpeech
from frontend.utils import dataframe_with_selections


def load_view():
    st.title('Podcasts')
    podcast_keyword_string = st.text_input('Podcast keywords', value="")
    conn = connect_to_colibri_db()
    try:
        podcasts_rows = fetch_all_podcasts(conn, podcast_keyword_string)
    finally:
        conn.close()
    if st.button('Refresh'):
        st.write('Refreshing...')
        st.rerun()

    # more about data frames: # https://docs.streamlit.io/library/api-reference/data/st.dataframe
    podcasts_df = pd.DataFrame(podcasts_rows, columns=["Id", "Creation date", "Caption", "Language", "Model", "Voice"])
    podcasts_selection = dataframe_with_selections(podcasts_df)
