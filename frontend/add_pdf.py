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
from backend.database import connect_to_colibri_db, create_document, create_document_part_with_text_content, create_document_part_with_binary_content
from datetime import datetime
from langchain_community.document_loaders import NewsURLLoader
from PyPDF2 import PdfReader
from backend import constants as const


def load_view():
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    url = st.text_input('original url (optional)')
    uploaded_url_file = st.file_uploader("Upload a TXT file for url (optional)", type="txt")

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
            if ((url is None) or (url == "")) and uploaded_url_file is not None:
                url = uploaded_url_file.getvalue().decode("utf-8")

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
                snippet_id = create_document(conn, snippet)

                if url is not None and url != "":
                  snippet_part_url = (snippet_id, const.PART_URL, None, url);
                  create_document_part_with_text_content(conn, snippet_part_url)

                bytes_data = uploaded_file.getvalue()
                snippet_part_pdf = (snippet_id, const.PART_PRIMARY, uploaded_file.name, bytes_data, len(bytes_data), const.MIMETYPE_PDF)
                create_document_part_with_binary_content(conn, snippet_part_pdf)

                snippet_part_content = (snippet_id, const.PART_CONTENT, content_language, document_content)
                create_document_part_with_text_content(conn, snippet_part_content)

                metadata = ""
                metadata += "Filename: " + uploaded_file.name + "\n"
                metadata += "Author: " + str(meta.author) + "\n"
                metadata += "Creator: " + str(meta.creator) + "\n"
                metadata += "Producer: " + str(meta.producer) + "\n"
                metadata += "Subject: " + str(meta.subject) + "\n"
                metadata += "Title: " + str(meta.title) + "\n"
                st.text_area("Metadata", value=metadata, height=120, max_chars=const.UI_DEFAULT_TEXT_AREA_MAX_CHARS, key=None)
                st.text_area("Content", value=document_content, height=400, max_chars=const.UI_DEFAULT_TEXT_AREA_MAX_CHARS, key=None)
            finally:
                conn.close()
