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
from backend.database import connect_to_colibri_db
from backend.openai import simple_translate
from backend import constants as const


def load_view():
    input_text = st.text_area("Enter your text", height=160)
    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox('language', [const.LANGUAGE_FA_CAPTION, const.LANGUAGE_DE_CAPTION, const.LANGUAGE_EN_CAPTION, const.LANGUAGE_FR_CAPTION], index=0)
    with col2:
        back_translation_language = st.selectbox('back translation language', ["", const.LANGUAGE_FA_CAPTION, const.LANGUAGE_DE_CAPTION, const.LANGUAGE_EN_CAPTION, const.LANGUAGE_FR_CAPTION], index=2)

    if st.button('Translate'):
        with st.spinner('Translating...'):
            conn = connect_to_colibri_db()
            try:
                translation = simple_translate(input_text, language)
                st.text_area("Translation", value=translation, height=160)
                # st.write(explanation)
                #snippet = (title, datetime.now());
                #snippet_id = create_snippet(conn, snippet)

                #snippet_part_pdf = (snippet_id, const.PART_PRIMARY, uploaded_file.name, uploaded_file.getvalue(), const.MIMETYPE_PDF)
                #create_snippet_part_with_binary_content(conn, snippet_part_pdf)

                #content_language = const.LANGUAGE_EN
                #snippet_part_content = (snippet_id, const.PART_CONTENT, content_language, document_content)
                #create_snippet_part_with_text_content(conn, snippet_part_content)
            finally:
                conn.close()
            if translation is not None and back_translation_language != "":
                with st.spinner('Back translating...'):
                    back_translation = simple_translate(translation, back_translation_language)
                    st.text_area("Back translation", value=back_translation, height=160)
                # st.write(explanation)
                #snippet = (title, datetime.now());
                #snippet_id = create_snippet(conn, snippet)

                #snippet_part_pdf = (snippet_id, const.PART_PRIMARY, uploaded_file.name, uploaded_file.getvalue(), const.MIMETYPE_PDF)
                #create_snippet_part_with_binary_content(conn, snippet_part_pdf)

                #content_language = const.LANGUAGE_EN
                #snippet_part_content = (snippet_id, const.PART_CONTENT, content_language, document_content)
                #create_snippet_part_with_text_content(conn, snippet_part_content)





