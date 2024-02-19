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
import utils as utl
from app_auth import get_session_id, clear_cache, check_password_db
from views import home,about,analysis,options,configuration, add_url

st.set_page_config(layout="wide", page_title='Navbar sample')
st.set_option('deprecation.showPyplotGlobalUse', False)

utl.inject_custom_css()
utl.navbar_component()

def navigation():
    route = utl.get_current_route()
    if route == "home":
      home.load_view()
    elif route == "about":
      about.load_view()
    elif route == "analysis":
      analysis.load_view()
    elif route == "options":
      options.load_view()
    elif route == "configuration":
      configuration.load_view()
    elif route == "add_url":
      add_url.load_view()
    elif route == None:
      home.load_view()

if st.button("Log out"):
    clear_cache()
    st.session_state.password_correct = False

if check_password_db():
  navigation()
