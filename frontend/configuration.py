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
from backend import constants as const
from backend.database import connect_to_colibri_db, update_user
from backend.util import obscure_str


def load_view():
    st.title('Configuration Page')
    st.text_input('EMail',  value=st.session_state[const.SESSION_USER_EMAIL], disabled=True)

    open_ai_api_key = st.text_input('OpenAI API key',  value=st.session_state[const.SESSION_USER_OPEN_AI_API_KEY] if const.SESSION_USER_OPEN_AI_API_KEY in st.session_state else "", type="password")

    if st.button('save configuration'):
        conn = connect_to_colibri_db()
        try:
          try:
            update_user(conn, st.session_state[const.SESSION_USER_ID],  obscure_str( open_ai_api_key ) )
          except:
            conn.rollback()
            raise
          conn.commit()
        finally:
          conn.close()
        st.session_state[const.SESSION_USER_OPEN_AI_API_KEY] = open_ai_api_key
        st.success("Configuration saved successfully")
