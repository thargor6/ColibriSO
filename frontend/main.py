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

from backend.auth import check_password_db
from frontend import documents, about, add_pdf, add_pdfs, options, configuration, add_url, logout, chat, explain, translate, podcasts, utils as utl
from backend import constants as const

def navigation():
    route = utl.get_current_route()

    if route == const.ROUTE_ABOUT:
        about.load_view()
    elif route == const.ROUTE_ADD_PDF:
        add_pdf.load_view()
    elif route == const.ROUTE_ADD_PDFS:
        add_pdfs.load_view()
    elif route == const.ROUTE_ADD_URL:
        add_url.load_view()
    elif route == const.ROUTE_CHAT:
        chat.load_view()
    elif route == const.ROUTE_CONFIGURATION:
        configuration.load_view()
    elif route == const.ROUTE_DOCUMENTS:
        documents.load_view()
    elif route == const.ROUTE_EXPLAIN:
        explain.load_view()
    elif route == const.ROUTE_LOGOUT:
        logout.load_view()
    elif route == const.ROUTE_OPTIONS:
        options.load_view()
    elif route == const.ROUTE_PODCASTS:
        podcasts.load_view()
    elif route == const.ROUTE_TRANSLATE:
        translate.load_view()
    else:
        documents.load_view()

def load_view():
    if check_password_db():
        navigation()
