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

from backend.database import connect_to_colibri_db, create_document, create_document_part_with_text_content
from datetime import datetime

from langchain_community.document_loaders import NewsURLLoader
from backend import constants as const


def load_view():
    url = st.text_input('enter your url',  value="https://medium.com/enrique-dans/the-time-has-come-to-ban-robocalls-using-ai-generated-voices-d4b0ea3d665e")

    if st.button('add url'):
        urls = [
            url,
        ]

        with st.spinner('Loading document...'):
            loader = NewsURLLoader(urls=urls)
            documents = loader.load()
        data = documents[0]

        if data.page_content is None:
            data.page_content = ""
        title = data.metadata[const.METADATA_TITLE]
        if title is None:
            title = ""
        if data.metadata is None:
            data.metadata = ""

        conn = connect_to_colibri_db()
        try:
            snippet = (title, datetime.now());
            snippet_id = create_document(conn, snippet)

            snippet_part_url = (snippet_id, const.PART_URL, None, url);
            create_document_part_with_text_content(conn, snippet_part_url)

            content_language = data.metadata[const.METADATA_LANGUAGE]
            if content_language is None:
                content_language = const.LANGUAGE_EN
            snippet_part_content = (snippet_id, const.PART_CONTENT, content_language, data.page_content);
            create_document_part_with_text_content(conn, snippet_part_content)

            st.header("Metadata")
            st.write(data.metadata)
            st.header("Content")
            st.write(data.page_content)
            print(data.page_content)
        finally:
            conn.close()


