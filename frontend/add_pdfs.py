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
import os

def load_view():
    uploaded_files = st.file_uploader("Upload PDF-files (add optional TXT-files for urls)", type=['pdf', 'txt'], accept_multiple_files = True)
    if st.button('add pdfs') and len(uploaded_files) > 0:
        filtered_files = [uploaded_file for uploaded_file in uploaded_files if uploaded_file.name.lower().endswith("pdf")]
        if len(filtered_files) > 0:
            curr_pdf_counter = 0
            progressbar = st.progress(0.0, text="Processing PDF files...)")
            for uploaded_file in filtered_files:
                curr_pdf_counter += 1
                progressbar.progress(curr_pdf_counter / len(filtered_files))
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

                    url_file_name = os.path.splitext(uploaded_file.name)[0]+'.txt'
                    filtered_txt_files = [uploaded_file for uploaded_file in uploaded_files if uploaded_file.name == url_file_name]
                    if len(filtered_txt_files) != 1:
                        filtered_txt_files = [uploaded_file for uploaded_file in uploaded_files if uploaded_file.name.lower() == url_file_name.lower()]

                    if len(filtered_txt_files) == 1:
                       url = filtered_txt_files[0].getvalue().decode("utf-8")
                    else:
                       url = None

                    if url is not None and url != "":
                        with st.spinner('Loading document...'):
                            urls = [
                                url,
                            ]
                            news_loader = NewsURLLoader(urls=urls)
                            news_documents = news_loader.load()
                            news_data = news_documents[0]
                            news_title = news_data.metadata[const.METADATA_TITLE]
                            if news_title is not None:
                                title = news_title
                            news_content_language = news_data.metadata[const.METADATA_LANGUAGE]
                            if news_content_language is None:
                                content_language = news_content_language

                            conn = connect_to_colibri_db()
                            try:
                                try:
                                    document = (title, datetime.now());
                                    document_id = create_document(conn, document)

                                    if url is not None and url != "":
                                        document_part_url = (document_id, const.PART_URL, None, url);
                                        create_document_part_with_text_content(conn, document_part_url)

                                    bytes_data = uploaded_file.getvalue()
                                    document_part_pdf = (document_id, const.PART_PRIMARY, uploaded_file.name, bytes_data, len(bytes_data), const.MIMETYPE_PDF)
                                    create_document_part_with_binary_content(conn, document_part_pdf)

                                    document_part_content = (document_id, const.PART_CONTENT, content_language, document_content)
                                    create_document_part_with_text_content(conn, document_part_content)
                                except:
                                    conn.rollback()
                                    raise
                                conn.commit()
                            finally:
                                conn.close()
            if curr_pdf_counter == 1:
              st.info("PDF file successfully added")
            elif curr_pdf_counter >1:
             st.info("{count} PDF files successfully added".format(count=curr_pdf_counter))
        else:
            st.error("No PDF files uploaded.")
