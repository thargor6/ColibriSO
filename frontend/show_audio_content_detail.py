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

from backend.database import connect_to_colibri_db, fetch_all_document_summary_parts, fetch_all_document_parts_with_audio, \
    fetch_all_audio_parts, fetch_audio_data


def showAudioContent(details, snippet_selection, keyword_string):
  with details:
      st.subheader("Audio content:")
      if len(snippet_selection["Id"].values) > 0:
          with st.spinner('Loading audio content ...'):
              conn = connect_to_colibri_db()
              try:
                 parts_rows = fetch_all_document_parts_with_audio(conn, snippet_selection["Id"].values, keyword_string)
                 for row in parts_rows:
                      snippet_id = row[0]
                      snippet_part_id = row[1]
                      st.header("Document " + str(row[0]) + " Part " + str(row[1]))
                      st.write(row[4])
                      audio_parts = fetch_all_audio_parts(conn, snippet_id, snippet_part_id)
                      for audio_row in audio_parts:
                          st.subheader("Audio " + str(audio_row[0]))
                          audio_data = fetch_audio_data(conn, audio_row[0])
                          st.audio(audio_data, format='audio/mp3')
              finally:
                 conn.close()
      else:
          st.write("(No document selected)")

