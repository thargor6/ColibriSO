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

# Language Constants
APP_NAME = "ColibriSO"


LANGUAGE_EN = 'en'
LANGUAGE_FA = 'fa'
LANGUAGE_DE = 'de'
LANGUAGE_FR = 'fr'

PART_URL = 'url'
PART_CONTENT = 'content'
PART_SUMMARY = 'summary'

METADATA_TITLE = 'title'
METADATA_LANGUAGE = 'language'

SESSION_USER_ID = "user_id"
SESSION_USER_EMAIL = "user_email"
SESSION_USER_OPEN_AI_API_KEY = "user_open_ai_api_key"

def getLanguageName(language_id):
    if language_id == LANGUAGE_EN:
        return "English"
    if language_id == LANGUAGE_FA:
        return "Farsi"
    if language_id == LANGUAGE_DE:
        return "German"
    if language_id == LANGUAGE_FR:
        return "French"
    return "Unknown"
