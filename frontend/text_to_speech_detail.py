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

import os

import streamlit as st

from backend.database import connect_to_colibri_db, fetch_all_document_parts, create_document_part_audio
import backend.constants as const
from backend.openai import text_to_speech


def textToSpeech(details, snippet_selection, parts_keyword_string):
    audio_created = 0
    with details:
        st.subheader("Document parts:")
        if len(snippet_selection["Id"].values) > 0:
            with (st.spinner('Converting content...')):
                conn = connect_to_colibri_db()
                try:
                    parts_rows = fetch_all_document_parts(conn, snippet_selection["Id"].values, parts_keyword_string)
                finally:
                    conn.close()
                for row in parts_rows:
                    snippet_type = row[2]
                    snippet_content = row[4]
                    snippet_id = row[0]
                    snippet_part_id = row[1]
                    if snippet_content is not None and snippet_type == const.PART_SUMMARY_BRIEF:
                        voice = const.OPENAI_DFLT_SPEECH_VOICE
                        model = const.OPENAI_DFLT_SPEECH_MODEL
                        audio_path =  text_to_speech(snippet_content, voice)
                        try:
                            in_file = open(audio_path, "rb")
                            try:
                                audio_data = in_file.read()
                            finally:
                                in_file.close()
                            snippet_part_audio = (snippet_id, snippet_part_id, const.OPENAI_DFLT_SPEECH_MODEL, voice, audio_data, len(audio_data), const.MIMETYPE_MP3)
                            conn = connect_to_colibri_db()
                            try:
                                create_document_part_audio(conn, snippet_part_audio)
                                audio_created += 1
                            finally:
                                conn.close()
                        finally:
                            os.remove(audio_path)
        else:
            st.write("(No document selected)")
    return audio_created
