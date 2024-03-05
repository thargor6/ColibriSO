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
from langchain_community.document_loaders import NewsURLLoader
from PyPDF2 import PdfReader
from backend import constants as const


def load_view():
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    url = st.text_input('original url (optional)')

    with_summary = st.checkbox('create summary', value=True)
    if with_summary:
        summary_language = st.selectbox('select a language', [const.LANGUAGE_DE, const.LANGUAGE_FA, const.LANGUAGE_EN, const.LANGUAGE_FR])

    if st.button('add pdf'):
        with st.spinner('Loading document...'):
            reader = PdfReader(uploaded_file)
            num_pages = len(reader.pages)

            meta = reader.metadata

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

            # best 'guess' for language so far
            content_language = const.LANGUAGE_EN


            if url is not None and url != "":
                with st.spinner('Loading document...'):
                    urls = [
                        url,
                    ]
                    news_loader = NewsURLLoader(urls=urls)
                    news_documents = news_loader.load()
                    news_data = news_documents[0]
                    news_title = news_data.metadata[const.METADATA_TITLE]
                    if news_title is None:
                       title = news_title
                    news_content_language = news_data.metadata[const.METADATA_LANGUAGE]
                    if news_content_language is None:
                       content_language = news_content_language

            conn = connect_to_colibri_db()
            try:
                snippet = (title, datetime.now());
                snippet_id = create_snippet(conn, snippet)

                if url is not None and url != "":
                  snippet_part_url = (snippet_id, const.PART_URL, None, url);
                  create_snippet_part_with_text_content(conn, snippet_part_url)

                snippet_part_pdf = (snippet_id, const.PART_PRIMARY, uploaded_file.name, uploaded_file.getvalue(), const.MIMETYPE_PDF)
                create_snippet_part_with_binary_content(conn, snippet_part_pdf)

                snippet_part_content = (snippet_id, const.PART_CONTENT, content_language, document_content)
                create_snippet_part_with_text_content(conn, snippet_part_content)

                metadata = ""
                metadata += "Filename: " + uploaded_file.name + "\n"
                metadata += "Author: " + str(meta.author) + "\n"
                metadata += "Creator: " + str(meta.creator) + "\n"
                metadata += "Producer: " + str(meta.producer) + "\n"
                metadata += "Subject: " + str(meta.subject) + "\n"
                metadata += "Title: " + str(meta.title) + "\n"
                st.text_area("Metadata", value=metadata, height=120, max_chars=const.UI_DEFAULT_TEXT_AREA_MAX_CHARS, key=None)

                st.text_area("Content", value=document_content, height=400, max_chars=const.UI_DEFAULT_TEXT_AREA_MAX_CHARS, key=None)

                if with_summary:
                    with st.spinner('Creating brief summary...'):
                        brief_summary = simple_summary(const.getLanguageCaption(summary_language), document_content, True)
                        snippet_part_brief_summary = (snippet_id, const.PART_SUMMARY_BRIEF, summary_language, brief_summary);
                        create_snippet_part_with_text_content(conn, snippet_part_brief_summary)
                        st.text_area("Brief Summary", value=brief_summary, height=160, max_chars=const.UI_DEFAULT_TEXT_AREA_MAX_CHARS, key=None)
                    with st.spinner('Creating comprehensive summary...'):
                        comprehensive_summary = simple_summary(const.getLanguageCaption(summary_language), document_content, False)
                        snippet_part_comprehensive_summary = (snippet_id, const.PART_SUMMARY_COMPREHENSIVE, summary_language, comprehensive_summary);
                        create_snippet_part_with_text_content(conn, snippet_part_comprehensive_summary)
                        st.text_area("Comprehensive Summary", value=comprehensive_summary, height=240, max_chars=const.UI_DEFAULT_TEXT_AREA_MAX_CHARS, key=None)
            finally:
                conn.close()
