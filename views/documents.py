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

from app_database import connect_to_colibri_db, fetch_all_snippets, fetch_all_snippet_parts
from app_openai import simple_chat
import app_constants as const

import pandas as pd

def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)

def load_view():
    st.title('Documents overview')
    conn = connect_to_colibri_db()
    try:
        # more about data frames: # https://docs.streamlit.io/library/api-reference/data/st.dataframe
        snippet_rows = fetch_all_snippets(conn)
        snippet_df = pd.DataFrame(snippet_rows, columns=["Id", "Creation date", "Caption"])
        snippet_selection = dataframe_with_selections(snippet_df)

        #print(snippet_selection["Id"])
        #print(snippet_selection["Id"].values)
        #print(len(snippet_selection["Id"].values))

        st.subheader("Document parts:")
        if len(snippet_selection["Id"].values) > 0:
            with st.spinner('Loading parts...'):
                parts_rows = fetch_all_snippet_parts(conn, snippet_selection["Id"].values)
                parts_df = pd.DataFrame(parts_rows, columns=["Snippet Id", "Id", "Snippet type", "Language", "Content", "Filename", "Mime type"])
                st.dataframe(parts_df)
        else:
            st.write("(No document selected)")
    finally:
        conn.close()

"""
    language = st.selectbox('add a language', [const.LANGUAGE_DE, const.LANGUAGE_FA, const.LANGUAGE_EN, const.LANGUAGE_FR])

    prompt = st.text_input('enter your prompt')

    if st.button('Generate'):
      result = simple_chat(prompt, const.getLanguageName(language))
      st.write(result)

      return True
"""