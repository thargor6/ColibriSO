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
from langchain.text_splitter import RecursiveCharacterTextSplitter

from backend.database import connect_to_colibri_db, create_document, create_document_part_with_text_content, create_document_part_with_binary_content
from datetime import datetime
from langchain_community.document_loaders import NewsURLLoader
from PyPDF2 import PdfReader
from backend import constants as const
from backend.db_summary import create_summary_for_document, create_chunked_summary
from backend.openai import text_to_speech
import os


def load_view():
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    url = st.text_input('original url (alternative)')
    #uploaded_url_file = st.file_uploader("Upload a TXT file for url (optional)", type="txt")

    summary_type = st.selectbox('type', [const.PART_SUMMARY_BRIEF, const.PART_SUMMARY_COMPREHENSIVE], index=1)
    summary_language = st.selectbox('language', [const.LANGUAGE_EN_CAPTION, const.LANGUAGE_DE_CAPTION, const.LANGUAGE_FR_CAPTION, const.LANGUAGE_FA_CAPTION], index=1)
    voice = st.selectbox('voice', [const.SPEECH_VOICE_ALLOY, const.SPEECH_VOICE_ECHO, const.SPEECH_VOICE_FABLE, const.SPEECH_VOICE_ONYX, const.SPEECH_VOICE_NOVA, const.SPEECH_VOICE_SHIMMER], index=4)
    if st.button('create summary'):
        st.subheader('Content')
        with st.spinner('Loading document...'):
            if uploaded_file is not None:
                reader = PdfReader(uploaded_file)
                num_pages = len(reader.pages)

                document_content = ""
                for page_number in range(num_pages):
                    page = reader.pages[page_number]
                    page_text = page.extract_text()
                    document_content += page_text
            else:
                document_content = ""
            st.text_area("Content", height=120, value=document_content)

        if document_content is not None and document_content != "":
            st.subheader('Summary')
            brief_summary = summary_type == const.PART_SUMMARY_BRIEF
            with st.spinner('Creating summary...'):
                summary = summary = create_chunked_summary(brief_summary, document_content, const.getLanguageId(summary_language))
                st.text_area("Summary", height=120, value=summary)

            if summary is not None and summary != "":
                with st.spinner('Creating audio...'):
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size = const.OPENAI_DFLT_SPEECH_CHUNKSIZE,
                        chunk_overlap  = 0,
                        length_function = len,
                    )
                    splitted_texts = text_splitter.split_text(summary)

                    for chunk_content in splitted_texts:
                        audio_path = text_to_speech(chunk_content, voice, const.OPENAI_DFLT_SPEECH_MODEL_QUALITY)
                        try:
                            in_file = open(audio_path, "rb")
                            try:
                                audio_data = in_file.read()
                                st.audio(audio_data, format='audio/mp3')
                            finally:
                                in_file.close()
                        finally:
                            os.remove(audio_path)



