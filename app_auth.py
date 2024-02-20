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
from datetime import datetime
import app_constants as const

from app_database import connect_to_colibri_db, select_session_by_session_id, create_session, select_user_by_user_name, \
    compare_password_hash, select_user_by_user_id

@st.cache_data
def get_session_id():
    """Retrieve unique session id. Uses caching in order to return the same id after refreshing the page or switching the tab"""
    from streamlit.runtime import get_instance
    from streamlit.runtime.scriptrunner import get_script_run_ctx
    runtime = get_instance()
    session_id = get_script_run_ctx().session_id
    return session_id

def clear_cache():
    """Clears the whole cache. Required for the current way to login/logout. Logout requires a new login with a new session id. The session id is cached (see above) and needs to be cleared."""
    st.cache_data.clear()

@st.cache_data
def get_session():
    from streamlit.runtime import get_instance
    from streamlit.runtime.scriptrunner import get_script_run_ctx
    runtime = get_instance()
    session_id = get_script_run_ctx().session_id
    session_info = runtime._session_mgr.get_session_info(session_id)
    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    return session_info.session

def check_password_db():
    """Returns `True` if the user had a correct password."""
    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        st.session_state["password_correct"] = False
        conn = connect_to_colibri_db()
        try:
            session_id = get_session_id()
            user_data = select_user_by_user_name(conn, st.session_state["username"])
            print("userdata", st.session_state["username"], user_data)
            if user_data is not None:
                pw_hash = user_data[3]
                user_id = user_data[0]
                if compare_password_hash(st.session_state["password"], pw_hash):
                    st.session_state["password_correct"] = True
                    session_data = (datetime.now(), user_id, session_id);
                    create_session(conn, session_data)
                    del st.session_state["password"]  # Don't store the username or password.
                    del st.session_state["username"]
                    st.session_state["password_correct"] = True
                    user_data_to_session(user_data)
        finally:
            conn.close()

    def user_data_to_session(user_data):
        st.session_state[const.SESSION_USER_ID] = user_data[0]
        st.session_state[const.SESSION_USER_EMAIL] = user_data[4]
        st.session_state[const.SESSION_USER_OPEN_AI_API_KEY] = user_data[5]

    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    conn = connect_to_colibri_db()
    try:
      session_id = get_session_id()
      session_data = select_session_by_session_id(conn, session_id)
      if session_data is not None:
        print('has session', session_data)
        user_data = select_user_by_user_id(conn, session_data[2])
        if user_data is not None:
          user_id = user_data[0]
          user_data_to_session(user_data)
        else:
          user_id = None
      else:
        user_id = None
    finally:
        conn.close()

    if user_id is None:
      login_form()
      if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
        return False
    else:

        print("user_id", st.session_state[const.SESSION_USER_ID])
        print("user_email", st.session_state[const.SESSION_USER_EMAIL])
        print("user_api_key", st.session_state[const.SESSION_USER_OPEN_AI_API_KEY])

        return True
