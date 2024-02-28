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

from backend.database import connect_to_colibri_db, create_snippet, create_snippet_part_with_text_content
from backend.openai import simple_summary
from datetime import datetime

from langchain_community.document_loaders import NewsURLLoader
from backend import constants as const


def load_view():
    url = st.text_input('enter your url',  value="https://medium.com/enrique-dans/the-time-has-come-to-ban-robocalls-using-ai-generated-voices-d4b0ea3d665e")

    with_summary = st.checkbox('create summary', value=True)
    if with_summary:
      summary_language = st.selectbox('select a language', [const.LANGUAGE_DE, const.LANGUAGE_FA, const.LANGUAGE_EN, const.LANGUAGE_FR])

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
            snippet_id = create_snippet(conn, snippet)

            snippet_part_url = (snippet_id, const.PART_URL, None, url);
            create_snippet_part_with_text_content(conn, snippet_part_url)

            content_language = data.metadata[const.METADATA_LANGUAGE]
            if content_language is None:
                content_language = const.LANGUAGE_EN
            snippet_part_content = (snippet_id, const.PART_CONTENT, content_language, data.page_content);
            create_snippet_part_with_text_content(conn, snippet_part_content)

            st.header("Metadata")
            st.write(data.metadata)
            st.header("Content")
            st.write(data.page_content)
            print(data.page_content)

            if with_summary:
              with st.spinner('Creating brief summary...'):
                  brief_summary = simple_summary(const.getLanguageName(summary_language), data.page_content, True)
                  snippet_part_brief_summary = (snippet_id, const.PART_SUMMARY_BRIEF, summary_language, brief_summary);
                  create_snippet_part_with_text_content(conn, snippet_part_brief_summary)

                  st.header("Brief Summary")
                  st.write(brief_summary)
              with st.spinner('Creating comprehensive summary...'):
                  comprehensive_summary = simple_summary(const.getLanguageName(summary_language), data.page_content, False)
                  snippet_part_comprehensive_summary = (snippet_id, const.PART_SUMMARY_COMPREHENSIVE, summary_language, brief_summary);
                  create_snippet_part_with_text_content(conn, snippet_part_comprehensive_summary)

                  st.header("Comphrehensive Summary")
                  st.write(comprehensive_summary)
        finally:
            conn.close()


