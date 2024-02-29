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

from backend.database import fetch_all_snippet_parts, connect_to_colibri_db
import pandas as pd

def showDetails(details, snippet_selection):
  with details:
      st.subheader("Document parts:")
      if len(snippet_selection["Id"].values) > 0:
          with st.spinner('Loading parts...'):
              conn = connect_to_colibri_db()
              try:
                 parts_rows = fetch_all_snippet_parts(conn, snippet_selection["Id"].values)
              finally:
                 conn.close()
              parts_df = pd.DataFrame(parts_rows, columns=["Snippet Id", "Id", "Snippet type", "Language", "Content", "Filename", "Mime type"])
              st.dataframe(parts_df)
      else:
          st.write("(No document selected)")

