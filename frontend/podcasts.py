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

from backend.database import connect_to_colibri_db, fetch_all_podcasts, create_podcast, delete_podcast, \
    fetch_all_document_parts_with_audio, fetch_podcast_parts, fetch_audio_data, update_podcast_parts_listened_status
import pandas as pd
import backend.constants as const
from datetime import datetime
from frontend.utils import dataframe_with_selections


def load_view():
    st.title('Podcasts')
    st.subheader('Create a new podcast')
    caption = st.text_input('podcast title')
    language = st.selectbox('select a language', [const.LANGUAGE_DE, const.LANGUAGE_FA, const.LANGUAGE_EN, const.LANGUAGE_FR], index=0)
    model = st.selectbox('model', [const.OPENAI_DFLT_SPEECH_MODEL_SPEED, const.OPENAI_DFLT_SPEECH_MODEL_QUALITY], index=1)
    voice = st.selectbox('voice', [const.SPEECH_VOICE_ALLOY, const.SPEECH_VOICE_ECHO, const.SPEECH_VOICE_FABLE, const.SPEECH_VOICE_ONYX, const.SPEECH_VOICE_NOVA, const.SPEECH_VOICE_SHIMMER], index=5)
    if st.button('create podcast'):
        conn = connect_to_colibri_db()
        try:
            try:
                podcast = (datetime.now(), caption, language, model, voice);
                podcast_id = create_podcast(conn, podcast)
            except:
                conn.rollback()
                raise
            conn.commit()
        finally:
            conn.close()

    st.subheader('Search for podcasts')
    podcast_keyword_string = st.text_input('Podcast keywords', value="")
    only_not_listened = st.checkbox('Not listened', value=True)
    conn = connect_to_colibri_db()
    try:
        podcasts_rows = fetch_all_podcasts(conn, podcast_keyword_string, only_not_listened)
    finally:
        conn.close()
    if st.button('Refresh'):
        st.write('Refreshing...')
        st.rerun()

    # more about data frames: # https://docs.streamlit.io/library/api-reference/data/st.dataframe
    podcasts_df = pd.DataFrame(podcasts_rows, columns=["Id", "Creation date", "Caption", "Language", "Model", "Voice"])
    podcasts_selection = dataframe_with_selections(podcasts_df)

    st.title('Podcast parts')
    col1, col2 = st.columns(2)
    with col1:
        showContentButton = st.button('Show content')
    with col2:
        deleteButton = st.button('Delete podcasts')
        confirmDelete = st.checkbox("Confirm delete")


    if deleteButton and confirmDelete:
        if len(podcasts_selection["Id"].values) > 0:
            with st.spinner('Deleting podcasts ...'):
                conn = connect_to_colibri_db()
                try:
                    delete_podcast(conn, podcasts_selection["Id"].values)
                finally:
                    conn.close()
            st.success("Documents successfully deleted")
            st.rerun()


    if showContentButton:
        st.subheader("Audio content:")
        if len(podcasts_selection["Id"].values) > 0:
            with st.spinner('Loading audio content ...'):
                conn = connect_to_colibri_db()
                try:
                  parts_rows = fetch_podcast_parts(conn, podcasts_selection["Id"].values, only_not_listened)
                  for row in parts_rows:
                        podcast_part_id = row[0]
                        podcast_id = row[1]
                        audio_part_id = row[2]
                        last_listened = row[3]
                        caption = row[4]
                        st.header(caption)
                        # st.subheader("Podcast " + str(podcast_id) + " Part " + str(podcast_part_id))
                        # st.subheader("Audio " + str(audio_part_id))
                        audio_data = fetch_audio_data(conn, audio_part_id)
                        st.audio(audio_data, format='audio/mp3')
                        col1, col2, col3 = st.columns([1, 1, 5])
                        with col3:
                            st.button("Mark as listened" if last_listened is None else "Mark as listened (again)", key="Mark as listened " + str(podcast_part_id),
                                         on_click=update_listened_status, args=[podcast_part_id])

                finally:
                    conn.close()
        else:
            st.write("(No document selected)")

def update_listened_status(podcast_part_id):
    conn = connect_to_colibri_db()
    try:
        try:
            update_podcast_parts_listened_status(conn, podcast_part_id)
        except:
            conn.rollback()
            raise
        conn.commit()
    finally:
        conn.close()
    st.success("Podcast Status successfully updated")
