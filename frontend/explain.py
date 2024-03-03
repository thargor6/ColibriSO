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
from backend.database import connect_to_colibri_db, create_snippet, create_snippet_part_with_text_content, create_snippet_part_with_binary_content
from backend.openai import simple_summary, simple_explanation
from datetime import datetime
#from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
from backend import constants as const


def load_view():
    prompt = st.text_input('enter your word')
    explanation_language = st.selectbox('select a language', [const.LANGUAGE_FA, const.LANGUAGE_DE, const.LANGUAGE_EN, const.LANGUAGE_FR])
    if st.button('Explain'):
        with st.spinner('Thinking...'):
            conn = connect_to_colibri_db()
            try:
                explanation = simple_explanation(prompt, const.getLanguageName(explanation_language))
                st.write(explanation)
                #snippet = (title, datetime.now());
                #snippet_id = create_snippet(conn, snippet)

                #snippet_part_pdf = (snippet_id, const.PART_PRIMARY, uploaded_file.name, uploaded_file.getvalue(), const.MIMETYPE_PDF)
                #create_snippet_part_with_binary_content(conn, snippet_part_pdf)

                #content_language = const.LANGUAGE_EN
                #snippet_part_content = (snippet_id, const.PART_CONTENT, content_language, document_content)
                #create_snippet_part_with_text_content(conn, snippet_part_content)

            finally:
                conn.close()
