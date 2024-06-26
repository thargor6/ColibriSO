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

from backend import constants as const

NAVBAR_PATHS = {
    'DOCUMENTS': const.ROUTE_DOCUMENTS,
    'QUICK SUMMARY': const.ROUTE_QUICK_SUMMARY,
    'ADD NOTE': const.ROUTE_ADD_NOTE,
    'ADD PDFS': const.ROUTE_ADD_PDFS,
    'PODCASTS': const.ROUTE_PODCASTS,
    'EXPLAIN': const.ROUTE_EXPLAIN,
    'TRANSLATE': const.ROUTE_TRANSLATE
}

SETTINGS = {
    'ABOUT': const.ROUTE_ABOUT,
    'ADD URL': const.ROUTE_ADD_URL,
    'ADD PDF': const.ROUTE_ADD_PDF,
    'CHAT': const.ROUTE_CHAT,
    'CONFIGURATION': const.ROUTE_CONFIGURATION,
    'TAGS': const.ROUTE_TAGS,
    'LOGOUT': const.ROUTE_LOGOUT
}