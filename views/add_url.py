
import streamlit as st

from app_database import connect_to_colibri_db
from app_openai import simple_chat, simple_summary
from datetime import datetime

from langchain_community.document_loaders import NewsURLLoader
#from langchain_community.document_loaders import PyPDFLoader
#from PyPDF2 import PdfReader

from app_sqlite import create_snippet, create_snippet_part

import app_constants as const

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
        snippet = (title, datetime.now());
        snippet_id = create_snippet(conn, snippet)

        snippet_part_url = (snippet_id, const.PART_URL, const.LANGUAGE_DE, url);
        create_snippet_part(conn, snippet_part_url)

        content_language = data.metadata[const.METADATA_LANGUAGE]
        if content_language is None:
            content_language = const.LANGUAGE_EN
        snippet_part_content = (snippet_id, const.PART_CONTENT, content_language, data.page_content);
        create_snippet_part(conn, snippet_part_content)

        st.header("Metadata")
        st.write(data.metadata)
        st.header("Content")
        st.write(data.page_content)
        print(data.page_content)

        if with_summary:
          with st.spinner('Creating summary...'):
              summary = simple_summary(const.getLanguageName(summary_language), data.page_content)
              snippet_part_summary = (snippet_id, const.PART_SUMMARY, summary_language, summary);
              create_snippet_part(conn, snippet_part_summary)

              st.header("Summary")
              st.write(summary)


