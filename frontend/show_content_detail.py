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

from backend.database import fetch_all_document_parts, connect_to_colibri_db

def showContent(details, snippet_selection, keyword_string):
  with details:
      st.subheader("Content parts:")
      if len(snippet_selection["Id"].values) > 0:
          with st.spinner('Loading content...'):
              conn = connect_to_colibri_db()
              try:
                 parts_rows = fetch_all_document_parts(conn, snippet_selection["Id"].values, keyword_string)
              finally:
                 conn.close()
              for row in parts_rows:
                if row[4] is not None:
                    st.subheader("Document " + str(row[0]) + " Part " + str(row[1]))
                    st.write(row[4])
      else:
          st.write("(No document selected)")

