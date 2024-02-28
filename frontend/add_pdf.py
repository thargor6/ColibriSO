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
from backend.openai import simple_summary
from datetime import datetime
#from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
from backend import constants as const


def load_view():
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    with_summary = st.checkbox('create summary', value=True)
    if with_summary:
        summary_language = st.selectbox('select a language', [const.LANGUAGE_DE, const.LANGUAGE_FA, const.LANGUAGE_EN, const.LANGUAGE_FR])

    if st.button('add pdf'):
        with st.spinner('Loading document...'):
            reader = PdfReader(uploaded_file)
            num_pages = len(reader.pages)

            meta = reader.metadata

            print(len(reader.pages))

            document_content = ""
            for page_number in range(num_pages):
                page = reader.pages[page_number]
                page_text = page.extract_text()
                document_content += page_text
            title = meta.title
            if title is None or title == "":
                title = uploaded_file.name
            if title is None:
                title = ""



            conn = connect_to_colibri_db()
            try:
                snippet = (title, datetime.now());
                snippet_id = create_snippet(conn, snippet)

                snippet_part_pdf = (snippet_id, const.PART_PRIMARY, uploaded_file.name, uploaded_file.getvalue(), const.MIMETYPE_PDF)
                create_snippet_part_with_binary_content(conn, snippet_part_pdf)

                content_language = const.LANGUAGE_EN
                snippet_part_content = (snippet_id, const.PART_CONTENT, content_language, document_content)
                create_snippet_part_with_text_content(conn, snippet_part_content)

                st.header("Metadata")
                st.write("Filename: ", uploaded_file.name)
                st.write("Author: ", meta.author)
                st.write("Creator: ", meta.creator)
                st.write("Producer: ", meta.producer)
                st.write("Subject: ", meta.subject)
                st.write("Title: ", meta.title)

                st.header("Content")
                st.write(document_content)
                print(document_content)

                if with_summary:
                    with st.spinner('Creating brief summary...'):
                        brief_summary = simple_summary(const.getLanguageName(summary_language), document_content, True)
                        snippet_part_brief_summary = (snippet_id, const.PART_SUMMARY_BRIEF, summary_language, brief_summary);
                        create_snippet_part_with_text_content(conn, snippet_part_brief_summary)

                        st.header("Brief Summary")
                        st.write(brief_summary)
                    with st.spinner('Creating comprehensive summary...'):
                        comprehensive_summary = simple_summary(const.getLanguageName(summary_language), document_content, False)
                        snippet_part_comprehensive_summary = (snippet_id, const.PART_SUMMARY_COMPREHENSIVE, summary_language, brief_summary);
                        create_snippet_part_with_text_content(conn, snippet_part_comprehensive_summary)

                        st.header("Comphrehensive Summary")
                        st.write(comprehensive_summary)
            finally:
                conn.close()
